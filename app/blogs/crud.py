from uuid import UUID

from sqlmodel import select

from app.blogs.models import BlogCreate, BlogRead, Blog


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

        return blog

    async def get_by_user_uuid(self, user_id: UUID) -> list[BlogRead]:
        statement = select(Blog).where(Blog.author_user_id == user_id)
        result = await self.session.execute(statement)
        blogs = result.scalars().all()
        return blogs