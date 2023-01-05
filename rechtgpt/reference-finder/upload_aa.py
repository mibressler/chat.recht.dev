import pinecone
import os
import json

with open('.apikey', 'r') as f:
    pinecone.init(api_key=f.readlines()[3].strip())

BATCH_SIZE = 50

index = pinecone.Index('aleph-alpha')

def upload_batch(batch):
    print(f"Uploading {len(batch)} vectors")
    index.upsert(vectors=batch, namespace='content')
    batch.clear()

batch = []
for filename in os.listdir('output_aa'):
    f = os.path.join('output_aa', filename)
    with open(f, 'r') as f:
        id = filename.strip('.json')
        print(f"Batching {id}")
        all_data = json.load(f)
        data = all_data
        batch.append((id, data, {
            "id": id.split('_')[0]
        }))
    if len(batch) == BATCH_SIZE:
        upload_batch(batch)

if len(batch) > 0:
    upload_batch(batch)

print("Done!")
