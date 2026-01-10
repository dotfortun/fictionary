from typing import Annotated
from fastapi import (
    APIRouter, Depends,
    HTTPException, Path, Request, Response,
    status,
)
from sqlmodel import Session, select

from models import (
    get_session, Universe,
    UniverseList, UniverseRead,
    UniverseCreate, UniverseUpdate
)

universe = APIRouter(prefix="/universe")


@universe.post(
    "/",
    response_model=UniverseRead
)
def create_universes(
    request: Request,
    universe: UniverseCreate,
    session: Session = Depends(get_session)
):
    db_universe = Universe.model_validate(universe)
    session.add(db_universe)
    session.commit()
    session.refresh(db_universe)
    return db_universe


@universe.get(
    "/",
    response_model=UniverseList
)
def read_universes(
    request: Request,
    session: Session = Depends(get_session)
):
    universes = session.exec(
        select(Universe).order_by(Universe.id)
    ).all()
    return {
        "types": universes
    }


@universe.get(
    "/{id}",
    response_model=UniverseRead
)
def read_universe(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session)
):
    universe = session.exec(
        select(Universe).where(Universe.id == id)
    ).first()

    if not universe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Universe #{id} doesn't exist."
        )

    return universe


@universe.put(
    "/{id}",
    response_model=UniverseRead
)
def update_universe(
    request: Request,
    id: Annotated[int, Path(title="id")],
    req_mediatype: UniverseUpdate,
    session: Session = Depends(get_session)
):
    db_universe = session.exec(
        select(Universe).where(Universe.id == id)
    ).first()

    if not universe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Universe #{id} doesn't exist."
        )

    req_data = req_mediatype.model_dump(exclude_unset=True)
    db_universe = db_universe.model_copy(update=req_data)
    session.merge(db_universe)
    session.commit()
    return db_universe


@universe.delete("/{id}")
async def delete_mediatype(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    db_universe = session.exec(
        select(Universe).where(Universe.id == id)
    ).first()

    if not db_universe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Universe #{id} doesn't exist."
        )

    session.delete(db_universe)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
