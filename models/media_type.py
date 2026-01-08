from typing import List, Optional
from pydantic import BaseModel
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
    cover_img: Optional[str] = None


class MediaCreate(MediaTypeBase):
    name: str
    cover_img: Optional[str] = None


class MediaRead(MediaTypeBase):
    id: int
    name: str
    cover_img: Optional[str] = None


class MediaUpdate(MediaTypeBase):
    name: Optional[str] = None
    cover_img: Optional[str] = None


class MediaList(BaseModel):
    types: List["MediaRead"]
