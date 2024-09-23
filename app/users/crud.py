from sqlmodel import select

from app.users.models import UserCreate, User


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

    async def get_all(self) -> list[User]:
        statement = select(User)
        result = await self.session.execute(statement)

        users = result.scalars().all()
        return users