from fastapi import HTTPException, status
from sqlmodel import select
from typing import Optional
import traceback
import logging
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


    async def validate_field(self, field: str, value: str) -> tuple[bool, Optional[User]]:
        valid_fields = ['stx_address_mainnet', "username", "uuid"]
        if field not in valid_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid field to validate")

        query = select(User).where(getattr(User, field) == value)
        try:
            result = await self.session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return True, user
            return False, None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"An error occurred while checking the field: {str(e)}")