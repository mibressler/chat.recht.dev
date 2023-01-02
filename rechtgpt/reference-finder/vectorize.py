import json
import html
import re
import openai
import os
from time import sleep

with open('.apikey', 'r') as f:
    openai.api_key = f.readlines()[0].strip()

ids_too_many_tokens = []
with open('too_many_tokens.csv', 'r') as f:
    for id in f.readlines():
        try:
            ids_too_many_tokens.append(int(id.strip()))
        except ValueError as e:
            print(f"Could not load errored ID: {e}, skipping")

with open('2019-02-19_oldp_cases.json', 'r') as f, open('too_many_tokens.csv', 'a') as tmt_lst:
    for i, line in enumerate(f.readlines()):
        # Do the first X entries from the JSON
        if i == 100:
            print("Done!")
            exit(0)
        print(f"Embedding {i}, ", end='')
        data = json.loads(line)
        case_id = data['id']
        print(f"ID: {case_id}")
        if case_id in ids_too_many_tokens:
            print("Already tried and errored, skipping")
            continue
        filename = os.path.join("output", f"{case_id}.json")
        if os.path.exists(filename):
            print("File already exists, skipping")
            continue
        with_tags = html.unescape(data['content'])
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+" , " ", with_whitespace)
        try:
            embedding = openai.Embedding.create(input = text, model="text-embedding-ada-002")
            sleep(1)
            with open(filename, 'w') as out:
                json.dump(embedding, out)
        except openai.error.InvalidRequestError as e:
            sleep(1)
            tmt_lst.write(f"{case_id}\n")
            print(e)
            print("Continuing")
