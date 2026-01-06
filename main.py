import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sqlmodel import create_engine, SQLModel

from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title="Fictionary",
    description="Fictionary",
    version="1.0.0",
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./index.html", "rt") as htmlfile:
        return htmlfile.read()
