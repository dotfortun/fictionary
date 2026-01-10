from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class CharacterBase(SQLModel):
    """
    Template model
    """
    name: str = Field(unique=True, index=True)
    portrait: str = Field(default=None)
    description: str = Field(default=None)

class Character(CharacterBase, table=True):
    """
    Database model
    """
    id: int | None = Field(default=None, primary_key=True)
    portrait: Optional[str] = None
    description: Optional[str] = None

class CharacterCreate(CharacterBase):
    name: str
    portrait: Optional[str] = None
    description: Optional[str] = None

class CharacterRead(CharacterBase):
    id: int
    portrait: Optional[str] = None
    description: Optional[str] = None

class CharacterUpdate(CharacterBase):
    name: Optional[str] = None
    portrait: Optional[str] = None
    description: Optional[str] = None

class CharacterList(BaseModel):
    characters: List["CharacterRead"]
