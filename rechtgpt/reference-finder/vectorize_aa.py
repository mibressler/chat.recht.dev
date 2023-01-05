import json
import html
import re
from aleph_alpha_client import AlephAlphaClient, AlephAlphaModel, SemanticEmbeddingRequest, SemanticRepresentation, Prompt
import os
from time import sleep
import nltk
import math

nltk.download('punkt')

SENTENCE_LIMIT = 80

with open('.apikey', 'r') as f:
    aam = AlephAlphaModel.from_model_name("luminous-base", f.readlines()[2].strip())

with open('2019-02-19_oldp_cases.json', 'r') as f:
    for i, line in enumerate(f.readlines()):
        # Do the first X entries from the JSON
        if i < 800:
            continue
        if i == 1000:
            print("Done!")
            exit(0)
        print(f"Embedding {i}, ", end='')
        data = json.loads(line)
        case_id = data['id']
        print(f"ID: {case_id}")
        if str(case_id) in ['171314', '116787', '175091', '175096']:
            print(f"Skipping due to exclusion list")
            continue
        with_tags = html.unescape(data['content'])
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+", " ", with_whitespace)
        sentences = nltk.tokenize.sent_tokenize(text)

        retry = True
        num_parts = int(math.ceil(len(sentences) / SENTENCE_LIMIT))
        while retry:
            retry = False
            if num_parts > 1:
                sentences_per_part = int(math.ceil(len(sentences) / num_parts))
                parts = []
                for i in range(num_parts):
                    if len(sentences) > i * sentences_per_part:
                        parts.append(" ".join(sentences[i * sentences_per_part:(i + 1) * sentences_per_part]))
            else:
                parts = [" ".join(sentences)]
            written_files = []
            for i, part in enumerate(parts):
                print(f"Embedding part {i + 1} of {len(parts)}")
                filename = os.path.join("output_aa", f"{case_id}_{i}.json")
                if os.path.exists(filename):
                    print("File already exists, skipping")
                    continue
                try:
                    request = SemanticEmbeddingRequest(prompt=Prompt.from_text(part), representation=SemanticRepresentation.Document)
                    embedding = aam.semantic_embed(request).embedding
                    with open(filename, 'w') as out:
                        json.dump(embedding, out)
                        written_files.append(filename)
                except ValueError as e:
                    print(f"Error: {e}, reducing sentence limit")
                    # TODO Possible optimization: Never remove data that has already been processed and instead
                    # TODO just split up the remaining text further
                    for f in written_files:
                        print(f"Removing {f}")
                        os.remove(f)
                    written_files.clear()
                    num_parts += 1
                    retry = True
                    break
