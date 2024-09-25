from typing import Optional
import logging
import traceback
from fastapi import HTTPException, status as https_status
from sqlmodel import select
from uuid import UUID

from starlette import status

from app.users.models import UserCreate, User, UserRead, UserUpdate


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
        if user is None:
            raise HTTPException(status_code=https_status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def patch(self, user_id: UUID, data: UserUpdate) -> UserRead:
         user = await self.get_by_id(user_id)
         if user is None:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

         new_data = data.model_dump(exclude_unset=True)
         print(new_data)
         for key, attr in new_data.items():
             setattr(user, key, attr)

         await self.session.commit()
         await self.session.refresh(user)

         return user
