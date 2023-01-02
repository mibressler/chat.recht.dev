import pinecone
import os
import json

with open('.apikey', 'r') as f:
    pinecone.init(api_key=f.readlines()[1].strip())

# TODO Batch uploads to speed up this process

index = pinecone.Index('2019-02-19-oldp-cases')
for filename in os.listdir('output'):
    f = os.path.join('output', filename)
    with open(f, 'r') as f:
        id = filename.strip('.json')
        print(f"Uploading {id}")
        all_data = json.load(f)
        data = all_data['data'][0]['embedding']
        index.upsert(vectors=[(id, data, all_data['usage'])], namespace='content')
