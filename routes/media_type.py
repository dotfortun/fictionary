from typing import Annotated
from fastapi import (
    APIRouter, Depends,
    HTTPException, Path, Request, Response,
    status,
)
from sqlmodel import Session, select

from models import (
    get_session, MediaType,
    MediaList, MediaRead, MediaCreate, MediaUpdate
)

media_type = APIRouter(prefix="/mediatype")


@media_type.post(
    "/",
    response_model=MediaRead
)
def create_media_types(
    request: Request,
    media_type: MediaCreate,
    session: Session = Depends(get_session)
):
    db_mediatype = MediaType.model_validate(media_type)
    session.add(db_mediatype)
    session.commit()
    session.refresh(db_mediatype)
    return db_mediatype


@media_type.get(
    "/",
    response_model=MediaList
)
def read_media_types(
    request: Request,
    session: Session = Depends(get_session)
):
    media_types = session.exec(
        select(MediaType).order_by(MediaType.id)
    ).all()
    return {
        "types": media_types
    }


@media_type.get(
    "/{id}",
    response_model=MediaRead
)
def read_media_type(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session)
):
    media_type = session.exec(
        select(MediaType).where(MediaType.id == id)
    ).first()

    if not media_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaType #{id} doesn't exist."
        )

    return media_type


@media_type.put(
    "/{id}",
    response_model=MediaRead
)
def update_media_type(
    request: Request,
    id: Annotated[int, Path(title="id")],
    req_mediatype: MediaUpdate,
    session: Session = Depends(get_session)
):
    db_mediatype = session.exec(
        select(MediaType).where(MediaType.id == id)
    ).first()

    if not media_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaType #{id} doesn't exist."
        )

    req_data = req_mediatype.model_dump(exclude_unset=True)
    db_mediatype = db_mediatype.model_copy(update=req_data)
    session.merge(db_mediatype)
    session.commit()
    return db_mediatype


@media_type.delete("/{id}")
async def delete_mediatype(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    db_mediatype = session.exec(
        select(MediaType).where(MediaType.id == id)
    ).first()

    if not db_mediatype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MediaType #{id} doesn't exist."
        )

    session.delete(db_mediatype)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )
