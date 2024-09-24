from sqlmodel import select
from typing import Optional

from app.auth.utils import generate_passwd_hash
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
        user.password_hash = generate_passwd_hash(values['password'])
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user