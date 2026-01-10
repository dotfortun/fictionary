from typing import Annotated
from fastapi import (
    APIRouter, Depends,
    HTTPException, Path, Request, Response,
    status,
)
from sqlmodel import Session, select

from models import (
    get_session, Character,
    CharacterList, CharacterRead, CharacterCreate, CharacterUpdate
)

character = APIRouter(prefix="/character")

@character.post(
    "/",
    response_model=CharacterRead
)
def create_character(
    character: CharacterCreate,
    session: Session = Depends(get_session)
):
    db_character = Character.model_validate(character)
    session.add(db_character)
    session.commit()
    session.refresh(db_character)
    return db_character

@character.get(
    "/",
    response_model=CharacterList
)
def read_characters(
    session: Session = Depends(get_session)
):
    character = session.exec(
        select(Character).order_by(Character.id)
    ).all()
    return {
        "characters": character
    }

@character.get(
    "/{id}",
    response_model=CharacterRead
)
def read_character(
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session)
):
    character = session.exec(
        select(Character).where(Character.id == id)
    ).first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaType #{id} doesn't exist."
        )

    return character

@character.put(
    "/{id}",
    response_model=CharacterRead
)
def update_media_type(
    id: Annotated[int, Path(title="id")],
    req_character: CharacterUpdate,
    session: Session = Depends(get_session)
):
    db_character = session.exec(
        select(Character).where(Character.id == id)
    ).first()

    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaType #{id} doesn't exist."
        )

    req_data = req_character.model_dump(exclude_unset=True)
    db_character = db_character.model_copy(update=req_data)
    session.merge(db_character)
    session.commit()
    return db_character

@character.delete("/{id}")
async def delete_character(
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    db_character = session.exec(
        select(Character).where(Character.id == id)
    ).first()

    if not db_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character #{id} doesn't exist."
        )

    session.delete(db_character)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )