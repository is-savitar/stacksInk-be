from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_async_session
from app.auth.crud import AuthCRUD


async def get_auth_crud(session: AsyncSession = Depends(get_async_session)) -> AuthCRUD:
    return AuthCRUD(session=session)
