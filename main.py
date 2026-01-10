from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from models import create_db_and_tables
from routes.media_type import media_type
from routes.universe import universe

create_db_and_tables()

app = FastAPI(
    title="Fictionary",
    description="Fictionary API",
    version="1.0.0",
)

app.include_router(media_type, tags=["Media Type"])
app.include_router(universe, tags=["Universe"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    include_in_schema=False,
    response_class=HTMLResponse
)
def read_root():
    with open("./index.html", "rt") as htmlfile:
        return htmlfile.read()
