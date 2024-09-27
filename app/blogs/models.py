from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, Relationship
from uuid import UUID
from app.core.models import UUIDModel, TimestampModel


class BlogBase(SQLModel):
    title: str = Field(..., min_length=3, max_length=255)
    tagline: str = Field(..., min_length=3, max_length=255)
    author: str = Field(..., min_length=3, max_length=255)
    author_user_id: UUID = Field(..., foreign_key="users.uuid", ondelete="CASCADE")
    blog_image: str = Field(...)
    blog_content: dict = Field(default_factory=dict, sa_column=Column(JSON))
    categories: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Blog(BlogBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "blogs"
    user: "User" = Relationship(back_populates="blogs")


class BlogRead(BlogBase, UUIDModel):
    user: "User" = Relationship(back_populates="blogs")

class BlogCreate(BlogBase):
    pass

class BlogUpdate(SQLModel):
    title: str | None = None,
    tagline: str | None = None,
    blog_image: str | None = None,
    blog_content: dict | None = None
