from uuid import UUID
from fastapi import APIRouter, status as https_status, Depends

from app.blogs.api import access_token_bearer
from app.users.crud import UsersCRUD
from app.users.deps import get_users_crud
from app.users.models import  UserRead, UserUpdate

router = APIRouter()

@router.get("/all", response_model=list[UserRead], status_code=https_status.HTTP_200_OK)
async def get_all_users(crud: UsersCRUD = Depends(get_users_crud)):
    users = await crud.get_all()
    return users

@router.get("", response_model=UserRead, status_code=https_status.HTTP_200_OK)
async def get_user_by_uuid(user_id: UUID, crud: UsersCRUD = Depends(get_users_crud)):
    user = await crud.get_by_id(user_id=user_id)
    return user

@router.patch("", response_model=UserRead, status_code=https_status.HTTP_200_OK)
async def patch_user(user_id: UUID,data: UserUpdate, crud: UsersCRUD = Depends(get_users_crud)):
    user = await crud.patch(user_id=user_id, data=data)
    return user

@router.get("/me", response_model=UserRead, status_code=https_status.HTTP_200_OK)
async def get_current_user(user_details=Depends(access_token_bearer), crud: UsersCRUD = Depends(get_users_crud)):
    print(user_details)
    user = await crud.get_by_id(user_id=user_details["user"]["user_id"])
    return user