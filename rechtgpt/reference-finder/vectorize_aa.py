import json
import html
import re
from aleph_alpha_client import AlephAlphaClient, AlephAlphaModel, SemanticEmbeddingRequest, SemanticRepresentation, Prompt
import os
from time import sleep
import nltk
import math

nltk.download('punkt')

SENTENCE_LIMIT = 100
SENTENCE_LIMIT_HARD = 400

with open('.apikey', 'r') as f:
    aam = AlephAlphaModel.from_model_name("luminous-base", f.readlines()[2].strip())

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
        with_tags = html.unescape(data['content'])
        with_whitespace = re.sub('<[^<]+?>', ' ', with_tags)
        text = re.sub("\s\s+", " ", with_whitespace)
        sentences = nltk.tokenize.sent_tokenize(text)
        if len(sentences) > SENTENCE_LIMIT_HARD:
            print(f"Text likely too long ({len(sentences)} sentences), skipping")
            continue
        if len(sentences) > SENTENCE_LIMIT:
            num_parts = int(math.ceil(len(sentences) / SENTENCE_LIMIT))
            sentences_per_part = int(math.ceil(len(sentences) / num_parts))
            parts = []
            for i in range(num_parts):
                if len(sentences) > i * sentences_per_part:
                    parts.append(" ".join(sentences[i * sentences_per_part:(i + 1) * sentences_per_part]))
        else:
            parts = [" ".join(sentences)]
        for i, part in enumerate(parts):
            print(f"Embedding part {i + 1} of {len(parts)}")
            filename = os.path.join("output_aa", f"{case_id}_{i}.json")
            if os.path.exists(filename):
                print("File already exists, skipping")
                continue
            request = SemanticEmbeddingRequest(prompt=Prompt.from_text(part), representation=SemanticRepresentation.Document)
            embedding = aam.semantic_embed(request).embedding
            with open(filename, 'w') as out:
                json.dump(embedding, out)
