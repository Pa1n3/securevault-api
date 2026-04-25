from fastapi.responses import JSONResponse
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


# ─── Custom Exception Class ───────────────────────────────────

class AppError(Exception):
    def __init__(self, status_code: int, error: str, message: str):
        self.status_code = status_code
        self.error = error
        self.message = message


# ─── Exception Handler ────────────────────────────────────────

async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error,
            "message": exc.message
        }
    )


# ─── 404 Handler ─────────────────────────────────────────────

async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "message": "Route not found"
        }
    )


# ─── 500 Handler ─────────────────────────────────────────────

async def server_error_handler(request: Request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "server_error",
            "message": "Something went wrong"
        }
    )

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
