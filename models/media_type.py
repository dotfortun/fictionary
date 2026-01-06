from typing import List, Optional
from sqlmodel import Field, SQLModel

class MediaTypeBase(SQLModel):
    """
    Template model
    """
    name: str = Field(unique=True, index=True)
    cover_img: str = Field(default=None)


class MediaType(MediaTypeBase, table=True):
    """
    Database model
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    cover_img: Optional[str]


class MediaCreate(MediaTypeBase):
    name: str
    cover_img: Optional[str]


class MediaRead(MediaTypeBase):
    name: str
    cover_img: Optional[str]


class MediaUpdate(MediaTypeBase):
    name: Optional[str]
    cover_img: Optional[str]


class MediaList:
    types: List[MediaType]
