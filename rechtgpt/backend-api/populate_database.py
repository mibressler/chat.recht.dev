import models, schemas
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
ids_too_many_tokens = []

data_path = os.path.join("..", "reference-finder")
tmt_file = os.path.join(data_path, "too_many_tokens.csv")
with open(tmt_file, 'r') as f:
    for id in f.readlines():
        try:
            ids_too_many_tokens.append(int(id.strip()))
        except ValueError as e:
            print(f"Could not load errored ID: {e}, skipping")

data_file = os.path.join(data_path, "2019-02-19_oldp_cases.json")
with open(data_file, 'r') as f:
    for i, line in enumerate(f.readlines()):
        # Do the first X entries from the JSON
        if i == 10000:
            print("Done!")
            exit(0)
        print(f"Loading {i}, ", end='')
        data = json.loads(line)
        case_id = data['id']
        print(f"ID: {case_id}")
        if case_id in ids_too_many_tokens:
            print("Too many tokens, skipping")
            continue
        ruling = models.Ruling(
            id = case_id,
            content = data['content'],
            additional_data = json.dumps({
                "slug": data['slug'],
                "court": data['court'],
                "file_number": data['file_number'],
                "date": data['date'],
                "created_date": data['created_date'],
                "updated_date": data['updated_date'],
                "type": data['type'],
                "ecli": data['ecli']
            })
        )
        models.insert_ruling(db, ruling)
