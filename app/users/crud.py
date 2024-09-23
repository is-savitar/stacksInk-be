from sqlmodel import select
from uuid import UUID
from app.users.models import UserCreate, User, UserRead


class UsersCRUD:
    def __init__(self, session):
        self.session = session

    async def post(self, data: UserCreate) -> User:
        values = data.model_dump()
        user = User(**values)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get_all(self) -> list[UserRead]:
        statement = select(User)
        result = await self.session.execute(statement)

        users = result.scalars().all()
        return users

    async def get_by_id(self, user_id: UUID) -> UserRead:
        statement = select(User).where(User.uuid == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user