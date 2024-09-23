from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import get_async_session
from app.blogs.crud import BlogsCRUD


async def get_blogs_crud(session: AsyncSession = Depends(get_async_session)) -> BlogsCRUD:
    return BlogsCRUD(session=session)
