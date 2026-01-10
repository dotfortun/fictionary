from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from models import create_db_and_tables
from routes.media_type import media_type

from routes.character import character
from routes.universe import universe

create_db_and_tables()

app = FastAPI(
    title="Fictionary",
    description="Fictionary API",
    version="1.0.0",
    docs_url="/swagger",
)

app.include_router(character, tags=["Character"])
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


@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
    )
