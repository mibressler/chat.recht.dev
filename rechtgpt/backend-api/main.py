from fastapi import Depends, FastAPI
from typing import *
import openai
import pinecone
import models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import html
import re
import json

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

with open('.apikey', 'r') as f:
    lines = f.readlines()
    openai.api_key = lines[0].strip()
    pinecone.init(api_key=lines[1].strip())
    index = pinecone.Index('2019-02-19-oldp-cases')

@app.get("/reference")
async def get_reference(prompt: str, db: Session = Depends(get_db)):
    embedding = openai.Embedding.create(input = prompt, model="text-embedding-ada-002")
    print(embedding['usage'])
    res = index.query(vector = embedding['data'][0]['embedding'], namespace = 'content', top_k = 10, include_metadata = True)

    response_data = []
    for elem in res['matches']:
        ruling = models.get_ruling(db, elem['id'])
        with_tags = html.unescape(ruling.content)
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+", " ", with_whitespace)
        response_data.append({
            "id": elem['id'],
            "score": elem['score'],
            "summary": text[:100],
            "metadata": json.loads(ruling.additional_data)
        })
    return {
        "prompt": prompt,
        "data": response_data
    }
