from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class UniverseBase(SQLModel):
    """
    Template model
    """
    name: str = Field(unique=True, index=True)
    cover_img: str = Field(default=None)


class Universe(UniverseBase, table=True):
    """
    Database model
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    cover_img: Optional[str] = None


class UniverseCreate(UniverseBase):
    name: str
    cover_img: Optional[str] = None


class UniverseRead(UniverseBase):
    id: int
    name: str
    cover_img: Optional[str] = None


class UniverseUpdate(UniverseBase):
    name: Optional[str] = None
    cover_img: Optional[str] = None


class UniverseList(BaseModel):
    types: List["UniverseRead"]