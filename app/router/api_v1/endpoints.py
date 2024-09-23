from fastapi import APIRouter

from app.users.api import router as users_router
from app.blogs.api import router as blogs_router
api_router = APIRouter()
include_api = api_router.include_router

routers = [
    (users_router, "users", "users"),
    (blogs_router, "blogs", "blogs"),
]

for router_item in routers:
    router, prefix, tag = router_item
    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=prefix)