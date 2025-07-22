import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_v1
from app.db.base import init_db
from app.middlewares.api_secret_middleware import APIKeyMiddleware

app = FastAPI(
    title="Planner API",
)
app.include_router(api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Your Nuxt dev server
        "http://localhost:3001",  # Alternative port if needed
        # Add production URLs later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allows all headers including custom ones
)

# # Add middleware
# 1. Frontend: POST /api/v1/auth/login with X-API-Secret header
# 2. Browser: "Wait! Custom header detected. Let me check if this is allowed"
# 3. Browser: OPTIONS /api/v1/auth/login (WITHOUT your custom headers)
# 4. Server: "Yes, X-API-Secret is allowed" (via CORS headers)
# 5. Browser: "OK, now I'll send the real POST with X-API-Secret"
app.add_middleware(APIKeyMiddleware)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@app.on_event("startup")
def on_startup():
    init_db()  # ← tables are created here

# @app.on_event("shutdown")
# def on_shutdown():
#     drop_db()
