from fastapi import APIRouter, status as https_status, Depends
from pydantic.v1.typing import NoneType

from app.auth.deps import AccessTokenBearer
from app.blogs.crud import BlogsCRUD
from app.blogs.deps import get_blogs_crud
from app.blogs.models import BlogRead, BlogCreate, BlogUpdate
from uuid import UUID

router = APIRouter()
access_token_bearer = AccessTokenBearer()


@router.get("", response_model=BlogRead, status_code=https_status.HTTP_200_OK)
async def get_blog(blog_id: UUID, crud: BlogsCRUD = Depends(get_blogs_crud)):
    blog = await crud.get_by_id(blog_id=blog_id)
    return blog


@router.patch("", response_model=BlogRead, status_code=https_status.HTTP_200_OK)
async def patch_blog(blog_id: UUID, data: BlogUpdate, crud: BlogsCRUD = Depends(get_blogs_crud),
                     user_details=Depends(access_token_bearer)):
    blog = await crud.patch(blog_id=blog_id, data=data, user_id=user_details["user"]["user_id"])
    return blog


@router.delete("", status_code=https_status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: UUID, crud: BlogsCRUD = Depends(get_blogs_crud),
                      user_details=Depends(access_token_bearer)):
    await crud.delete(blog_id=blog_id, user_id=user_details["user"]["user_id"])
    return None


@router.post("", response_model=BlogRead, status_code=https_status.HTTP_201_CREATED)
async def create_blog(data: BlogCreate, crud: BlogsCRUD = Depends(get_blogs_crud),
                      user_details=Depends(access_token_bearer)):
    blog = await crud.create(data=data)
    return blog


@router.get("/users", response_model=list[BlogRead], status_code=https_status.HTTP_200_OK)
async def get_users_blogs(user_id: UUID, crud: BlogsCRUD = Depends(get_blogs_crud),
                          user_details=Depends(access_token_bearer)):
    blogs = await crud.get_by_user_uuid(user_id=user_id)

    return blogs
