from fastapi import APIRouter, status as https_status, Depends

from app.blogs.crud import BlogsCRUD
from app.blogs.deps import get_blogs_crud
from app.blogs.models import BlogRead, BlogCreate
from uuid import UUID
router = APIRouter()


@router.get("", response_model=BlogRead, status_code=https_status.HTTP_200_OK)
async def get_blog(blog_id: UUID, crud: BlogsCRUD = Depends(get_blogs_crud)):
    blog = await crud.get_by_id(blog_id=blog_id)
    return blog


@router.post("", response_model=BlogRead, status_code=https_status.HTTP_201_CREATED)
async def create_blog(data: BlogCreate, crud: BlogsCRUD = Depends(get_blogs_crud)):
    blog = await crud.create(data=data)
    return blog

@router.get("/users", response_model=list[BlogRead], status_code=https_status.HTTP_200_OK)
async def get_users_blogs(user_id:UUID, crud: BlogsCRUD = Depends(get_blogs_crud)):
    blogs = await crud.get_by_user_uuid(user_id=user_id)

    return blogs
