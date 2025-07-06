from fastapi import FastAPI

from app.api.v1.tasks import router as tasks_router

app = FastAPI(title="Planner API")
app.include_router(tasks_router)
