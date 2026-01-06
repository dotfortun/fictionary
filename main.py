from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from models.db import create_db_and_tables

create_db_and_tables()

app = FastAPI(
    title="Fictionary",
    description="Fictionary API",
    version="1.0.0",
)

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./index.html", "rt") as htmlfile:
        return htmlfile.read()
