from fastapi import APIRouter, status as https_status, Depends

from app.blogs.crud import BlogsCRUD
from app.blogs.deps import get_blogs_crud
from app.blogs.models import BlogRead

router = APIRouter()

@router.get("/", response_model=BlogRead, status_code=https_status.HTTP_200_OK)
async def get_blog(blog_id, crud:BlogsCRUD=Depends(get_blogs_crud) ):
    blog = await crud.get_by_id(blog_id=blog_id)
    return blog