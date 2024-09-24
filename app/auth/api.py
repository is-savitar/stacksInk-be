from fastapi import APIRouter, status, Depends

from app.auth.crud import AuthCRUD
from app.auth.deps import get_auth_crud
from app.users.models import UserRead, UserCreate

router = APIRouter()

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, crud: AuthCRUD = Depends(get_auth_crud)):
    user = await crud.create_user(data=data)
    return user