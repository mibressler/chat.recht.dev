from fastapi import FastAPI
from typing import *
import openai
import pinecone

app = FastAPI()

with open('.apikey', 'r') as f:
    lines = f.readlines()
    openai.api_key = lines[0].strip()
    pinecone.init(api_key=lines[1].strip())
    index = pinecone.Index('2019-02-19-oldp-cases')

@app.get("/reference")
async def get_reference(prompt: str):
    embedding = openai.Embedding.create(input = prompt, model="text-embedding-ada-002")
    print(embedding['usage'])
    res = index.query(vector = embedding['data'][0]['embedding'], namespace = 'content', top_k = 10, include_metadata = True)
    response_data = [{"id": x['id'], "score": x['score']} for x in res['matches']]
    print(response_data)
    return {
        "prompt": prompt,
        "data": response_data
    }
