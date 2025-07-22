# middlewares/api_secret_middleware.py
import hashlib
import hmac

from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.security import logger, settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_paths=None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or ["/docs", "/redoc", "/openapi.json", "/health"]

    async def dispatch(self, request: Request, call_next):
        """
        Validate API key for all requests except:
        1. OPTIONS requests (CORS preflight)
        2. Explicitly excluded paths
        """
        logger.debug(f"{request.method} {request.url.path}")

        # ALWAYS let OPTIONS through - this is NOT a security risk
        # OPTIONS only checks if the actual request would be allowed
        if request.method == "OPTIONS":
            response = await call_next(request)
            return response

        # Skip validation for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)

        # Now validate API key for all other requests
        api_key = request.headers.get(settings.API_SECRET_HEADER_NAME)

        if not api_key:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "API secret header missing"}
            )

        # Secure hash comparison
        provided_hash = hashlib.sha256(api_key.encode()).digest()
        expected_hash = hashlib.sha256(settings.API_SECRET_KEY.encode()).digest()

        if not hmac.compare_digest(provided_hash, expected_hash):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": "Invalid API credentials"}
            )

        # Valid API key - proceed
        response = await call_next(request)
        return response
