from fastapi import Depends, FastAPI, HTTPException
from typing import *
import openai
import pinecone
import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import html
import re
import json
from fastapi.middleware.cors import CORSMiddleware
from aleph_alpha_client import AlephAlphaModel, SemanticEmbeddingRequest, SemanticRepresentation, Prompt

# TODO AI-generated summaries (plus have them in the DB)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080",
    "https://www.chat.recht.dev",
    "https://chat.recht.dev",
    "https://www.recht.dev",
    "https://recht.dev"
]

app.add_middleware(CORSMiddleware,
    allow_origins = origins,
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

with open('.apikey', 'r') as f:
    lines = f.readlines()
    openai.api_key = lines[0].strip()
    pinecone_apikey_openai = lines[1].strip()
    aam = AlephAlphaModel.from_model_name("luminous-base", lines[2].strip())
    pinecone_apikey_alephalpha = lines[3].strip()

@app.get("/reference")
async def get_reference(prompt: str, engine: int = 0, db: Session = Depends(get_db)):
    if engine == 0:
        pinecone.init(api_key=pinecone_apikey_openai)
        index = pinecone.Index('2019-02-19-oldp-cases')
        embedding = openai.Embedding.create(input = prompt, model="text-embedding-ada-002")
        print(embedding['usage'])
        res = index.query(vector = embedding['data'][0]['embedding'], namespace = 'content', top_k = 10, include_metadata = True)
    elif engine == 1:
        pinecone.init(api_key=pinecone_apikey_alephalpha)
        index = pinecone.Index('aleph-alpha')
        request = SemanticEmbeddingRequest(prompt=Prompt.from_text(prompt), representation=SemanticRepresentation.Query)
        embedding = aam.semantic_embed(request).embedding
        res = index.query(vector = embedding, namespace = 'content', top_k = 10, include_metadata = True)
        for elem in res['matches']:
            elem['id'] = elem['metadata']['id']
    else:
        raise HTTPException(status_code=400, detail="Invalid request")

    response_data = []
    for elem in res['matches']:
        ruling = models.get_ruling(db, elem['id'])
        with_tags = html.unescape(ruling.content)
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+", " ", with_whitespace)
        response_data.append({
            "id": elem['id'],
            "score": elem['score'],
            "summary": " ".join(text[:500].split()[:-1]),
            "metadata": json.loads(ruling.additional_data)
        })
    return {
        "prompt": prompt,
        "engine": engine,
        "data": response_data
    }

@app.get("/ruling")
async def get_ruling(id: str, db: Session = Depends(get_db)):
    ruling = models.get_ruling(db, id)
    if ruling is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "id": id,
        "content": ruling.content,
        "metadata": json.loads(ruling.additional_data)
    }
