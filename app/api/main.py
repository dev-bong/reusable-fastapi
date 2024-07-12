from fastapi import APIRouter

from app.api.routes import users, login, posts

api_router = APIRouter()
api_router.include_router(login.router, tags=["로그인"])
api_router.include_router(users.router, prefix="/users", tags=["유저"])
api_router.include_router(posts.router, prefix="/posts", tags=["게시글"])
