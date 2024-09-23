from typing import Optional

from sqlmodel import SQLModel, Field
from app.core.models import UUIDModel, TimestampModel

class UserBase(SQLModel):
    username: str = Field(..., min_length=3, max_length=30, unique=True)
    name: str = Field(..., min_length=3, max_length=30, nullable=True)
    profile_picture: str = Field(None, min_length=3, max_length=100, nullable=True)
    about_me: str = Field(None, min_length=3, max_length=100, nullable=True)

class UserProfile(UserBase):
    followers_count: int = Field(default=0)

class User(UserBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "users"

class UserCreate(UserBase):
    pass

class UserRead(UserBase, UUIDModel):
    pass