from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.users.crud import UsersCRUD


async def get_users_crud(session: AsyncSession = Depends(get_async_session)) -> UsersCRUD:
    return UsersCRUD(session=session)
