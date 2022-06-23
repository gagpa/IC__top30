from fastapi import FastAPI

from .auth import router as auth_router
from .coach import router as coach_router
from .registration import router as registration
from .student import router as student_router
from .user import router as user_router


def add_routers(app: FastAPI):
    app.include_router(coach_router)
    app.include_router(auth_router)
    app.include_router(student_router)
    app.include_router(registration)
    app.include_router(user_router)
