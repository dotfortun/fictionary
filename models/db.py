import os

from sqlmodel import create_engine, SQLModel, Session

from dotenv import load_dotenv

import models.media_type

load_dotenv()

database_url = os.getenv("POSTGRES_URL", "sqlite:///database.sqlite3")

engine = create_engine(database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

