from typing import Annotated
from fastapi import (
    APIRouter, Depends,
    HTTPException, Path, Request, Response,
    status,
)
from sqlmodel import Session, select

from models import (
    get_session, Creator,
    CreatorList, CreatorRead, CreatorCreate, CreatorUpdate
)

creator = APIRouter(prefix="/creator")

@creator.post(
    "/",
    response_model=CreatorRead
)
def create_creator(
    creator: CreatorCreate,
    session: Session = Depends(get_session)
):
    db_creator = Creator.model_validate(creator)
    session.add(db_creator)
    session.commit()
    session.refresh(db_creator)
    return db_creator

@creator.get(
    "/",
    response_model=CreatorList
)
def read_creators(
    session: Session = Depends(get_session)
):
    creator = session.exec(
        select(Creator).order_by(Creator.id)
    ).all()
    return {
        "creators": creator
    }

@creator.get(
    "/{id}",
    response_model=CreatorRead
)
def read_creator(
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session)
):
    creator = session.exec(
        select(Creator).where(Creator.id == id)
    ).first()

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator #{id} doesn't exist."
        )

    return creator

@creator.put(
    "/{id}",
    response_model=CreatorRead
)
def update_creator(
    id: Annotated[int, Path(title="id")],
    req_character: CreatorUpdate,
    session: Session = Depends(get_session)
):
    db_creator = session.exec(
        select(Creator).where(Creator.id == id)
    ).first()

    if not db_creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator #{id} doesn't exist."
        )

    req_data = req_character.model_dump(exclude_unset=True)
    db_creator = db_creator.model_copy(update=req_data)
    session.merge(db_creator)
    session.commit()
    return db_creator

@creator.delete("/{id}")
async def delete_creator(
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    db_creator = session.exec(
        select(Creator).where(Creator.id == id)
    ).first()

    if not db_creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator #{id} doesn't exist."
        )

    session.delete(db_creator)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )