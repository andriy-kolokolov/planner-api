from fastapi import APIRouter

from .authentication import router as authentication_router
from .tasks import router as tasks_router
from .users import router as users_router

api_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
api_v1.include_router(tasks_router)
api_v1.include_router(authentication_router)
api_v1.include_router(users_router)
