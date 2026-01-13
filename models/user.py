from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from models.mixins import TimeStampMixin

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserBase(SQLModel, TimeStampMixin):
    """
    Template model
    """
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = False
    admin: Optional[bool] = False


class User(UserBase, table=True):
    """
    Database model
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = False
    admin: Optional[bool] = False
    pwd_hash: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db, username: str):
    pass
