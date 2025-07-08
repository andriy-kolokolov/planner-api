from fastapi import FastAPI

from app.api.v1 import api_v1
from app.db.base import init_db
from app.db.base import drop_db

app = FastAPI(
    title="Planner API",
)
app.include_router(api_v1)


@app.on_event("startup")
def on_startup():
    init_db()  # ← tables are created here

@app.on_event("shutdown")
def on_shutdown():
    drop_db()


