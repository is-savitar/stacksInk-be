from typing import Optional
import logging
import traceback
from fastapi import HTTPException, status as https_status
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
        if user is None:
            raise HTTPException(status_code=https_status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def validate_field(self, field: str, value: str) -> tuple[bool, Optional[User]]:
        valid_fields = ['stx_address_mainnet', "username", "uuid"]
        if field not in valid_fields:
            raise HTTPException(
                status_code=https_status.HTTP_400_BAD_REQUEST, detail="Invalid field to validate")

        query = select(User).where(getattr(User, field) == value)
        try:
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return True, user
            return False, None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(status_code=https_status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while checking the field: {str(e)}")
