from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from datetime import date

class CreatorBase(SQLModel):
    """
    Template model
    """
    name: str = Field(unique=True, index=True)
    birth: date = Field(default=None)
    death: date = Field(default=None)

class Creator(CreatorBase, table=True):
    """
    Database model
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str
    birth: Optional[date] = None
    death: Optional[date] = None

class CreatorCreate(CreatorBase):
    name: str
    birth: Optional[date] = None
    death: Optional[date] = None

class CreatorRead(CreatorBase):
    id: int
    name: str
    birth: Optional[date] = None
    death: Optional[date] = None

class CreatorUpdate(CreatorBase):
    name: Optional[str] = None
    birth: Optional[date] = None
    death: Optional[date] = None

class CreatorList(BaseModel):
    creators: List["CreatorRead"]