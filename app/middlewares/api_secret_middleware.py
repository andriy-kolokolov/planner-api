# middlewares/api_secret_middleware.py
import hashlib
import hmac
import logging

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths=None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/redoc", "/openapi.json", "/health"]

    async def dispatch(self, request: Request, call_next):
        from app.core.config import get_settings
        settings = get_settings()

        # Skip for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        # Get API key from header
        api_key = request.headers.get(settings.API_SECRET_HEADER_NAME)

        # Validate API key
        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "API secret header missing"}
            )

        # Hash comparison for security
        provided_hash = hashlib.sha256(api_key.encode()).digest()
        expected_hash = hashlib.sha256(settings.API_SECRET_KEY.encode()).digest()

        if not hmac.compare_digest(provided_hash, expected_hash):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid API credentials"}
            )

        # Process request if validation passes
        response = await call_next(request)
        return response
