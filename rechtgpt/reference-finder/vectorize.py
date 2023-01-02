import json
import html
import re
import openai
import os

with open('.apikey', 'r') as f:
    openai.api_key = f.readlines()[0].strip()

with open('2019-02-19_oldp_cases.json', 'r') as f:
    for i, line in enumerate(f.readlines()):
        # Do the first X entries from the JSON
        if i == 1:
            print("Done!")
            exit(0)
        print(f"Embedding {i}, ", end='')
        data = json.loads(line)
        case_id = data['id']
        print(f"ID: {case_id}")
        filename = os.path.join("output", f"{case_id}.json")
        if os.path.exists(filename):
            print("File already exists, skipping")
            continue
        with_tags = html.unescape(data['content'])
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+" , " ", with_whitespace)
        try:
            embedding = openai.Embedding.create(input = [text], model="text-embedding-ada-002")
            with open(filename, 'w') as out:
                json.dump(embedding, out)
        except openai.error.InvalidRequestError as e:
            print(e)
            print("Continuing")
