from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import select

from app.blogs.models import BlogCreate, BlogRead, Blog, BlogUpdate


class BlogsCRUD:
    def __init__(self, session):
        self.session = session

    async def create(self, data: BlogCreate) -> BlogRead:
        values = data.model_dump()
        blog = Blog(**values)
        self.session.add(blog)
        await self.session.commit()
        await self.session.refresh(blog)

        return BlogRead.model_validate(blog)

    async def get_by_id(self, blog_id: UUID) -> BlogRead:
        statement = select(Blog).where(Blog.uuid == blog_id)
        result = await self.session.execute(statement)
        blog = result.scalar_one_or_none()
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A blog with this id doesn't exist")

        return blog

    async def get_by_user_uuid(self, user_id: UUID) -> list[BlogRead]:
        statement = select(Blog).where(Blog.author_user_id == user_id)
        result = await self.session.execute(statement)
        blogs = result.scalars().all()
        return blogs

    async def patch(self, blog_id: UUID, data: BlogUpdate, user_id: UUID) -> BlogRead:
        blog = await self.get_by_id(blog_id=blog_id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A blog with this id doesn't exist")

        if blog.author_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to delete this blog")
        new_data = data.model_dump(exclude_unset=True)
        for key, attr in new_data.items():
            setattr(blog, key, attr)
        await self.session.commit()
        await self.session.refresh(blog)

        return BlogRead.model_validate(blog)

    async def delete(self, blog_id: UUID, user_id: UUID) -> None:
        blog = await self.get_by_id(blog_id=blog_id)
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="A blog with this id doesn't exist")

        if blog.author_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to delete this blog")
        self.session.delete(blog)
        await self.session.commit()

        return None
