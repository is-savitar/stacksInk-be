from datetime import timedelta, datetime
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from app import auth_settings
from app.auth.crud import AuthCRUD
from app.auth.deps import get_auth_crud, RefreshTokenBearer, AccessTokenBearer
from app.auth.utils import create_access_token, verify_passwd_hash
from app.core.redis import add_jti_to_blocklist
from app.users.models import UserRead, UserCreate

router = APIRouter()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate, crud: AuthCRUD = Depends(get_auth_crud)):
    existing_user = await crud.get_user_by_stx_address(data.stx_address_mainnet)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this address already exists")
    user = await crud.create_user(data=data)
    return user


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(data: UserCreate, crud: AuthCRUD = Depends(get_auth_crud)):
    user = await crud.get_user_by_stx_address(data.stx_address_mainnet)
    if user is not None:
        password_valid = verify_passwd_hash(data.password, user.password_hash)
        if password_valid:
            access_token = create_access_token(data={
                "stx_address_mainnet": user.stx_address_mainnet,
                "user_id": str(user.uuid)
            })
            refresh_token = create_access_token(data={
                "stx_address_mainnet": user.stx_address_mainnet,
                "user_id": str(user.uuid)
            }, refresh=True, expiry=timedelta(days=auth_settings.refresh_token_expire_days))

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "stx_address_mainnet": user.stx_address_mainnet,
                        "uuid": str(user.uuid),
                    }
                }
            )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect stx_address or password")


@router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    print(token_details)
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(data=token_details["user"])
        return JSONResponse(
            content={
                "access_token": new_access_token,
            }
        )

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")


@router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    await add_jti_to_blocklist(jti)

