from fastapi import FastAPI

from .admin import router as admin_router
from .auth import router as auth_router
from .coach import router as coach_router
from .registration import router as registration
from .request import router as requests_router
from .self import router as self_router
from .slot import router as slot_router
from .student import router as student_router
from .user import router as user_router
from .event import router as event_router


def add_routers(app: FastAPI):
    app.include_router(admin_router, prefix='/api/v1')
    app.include_router(coach_router, prefix='/api/v1')
    app.include_router(auth_router, prefix='/api/v1')
    app.include_router(event_router, prefix='/api/v1')
    app.include_router(student_router, prefix='/api/v1')
    app.include_router(self_router, prefix='/api/v1')
    app.include_router(slot_router, prefix='/api/v1')
    app.include_router(requests_router, prefix='/api/v1')
    app.include_router(registration, prefix='/api/v1')
    app.include_router(user_router, prefix='/api/v1')
