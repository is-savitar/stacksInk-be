from sqlmodel import select
from typing import Optional

from app.users.models import UserCreate, User


class AuthCRUD:
    def __init__(self, session):
        self.session = session

    async def get_user_by_stx_address(self, stx_address_mainnet: str) -> Optional[User]:
        statement = select(User).where(User.stx_address_mainnet == stx_address_mainnet)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create_user(self, data: UserCreate) -> User:
        values = data.model_dump()
        user = User(**values)
        existing_user = await self.get_user_by_stx_address(user.stx_address_mainnet)

        if existing_user:
            return existing_user

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user