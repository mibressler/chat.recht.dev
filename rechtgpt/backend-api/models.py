from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, String
import schemas

Base = declarative_base()

class Ruling(Base):
    __tablename__ = "rulings"
    id = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=False)
    additional_data = Column(String, nullable=False)
    summary = Column(String)

def get_ruling(db: Session, id: str):
    return db.query(Ruling).filter(Ruling.id == id).first()

def insert_ruling(db: Session, ruling: schemas.Ruling):
    db_ruling = Ruling(id = ruling.id, content = ruling.content, additional_data = ruling.additional_data)
    db.add(db_ruling)
    db.commit()
    db.refresh(db_ruling)
    return db_ruling
