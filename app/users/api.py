from uuid import UUID

from fastapi import APIRouter, status as https_status, Depends
from app.users.crud import UsersCRUD
from app.users.deps import get_users_crud
from app.users.models import User, UserCreate, UserRead

router = APIRouter()
@router.post('', response_model=User, status_code=https_status.HTTP_201_CREATED)
async def create_user(data: UserCreate, crud: UsersCRUD = Depends(get_users_crud)):
    user = await crud.post(data=data)
    return user

@router.get("/all", response_model=list[UserRead], status_code=https_status.HTTP_200_OK)
async def get_all_users(crud: UsersCRUD = Depends(get_users_crud)):
    users = await crud.get_all()
    return users

@router.get("", response_model=UserRead, status_code=https_status.HTTP_200_OK)
async def get_user_by_uuid(user_id: UUID, crud: UsersCRUD = Depends(get_users_crud)):
    user = await crud.get_by_id(user_id=user_id)
    return user