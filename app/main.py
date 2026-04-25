from fastapi import FastAPI
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.errors  import limiter
from app.models import create_tables
from app.routers import users, notes, files
from app.errors import (
    AppError,
    app_error_handler,
    not_found_handler,
    server_error_handler
)



app = FastAPI(
    title="SecureVault API",
    description="A learning project with intentional security features and bugs",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(404, not_found_handler)
app.add_exception_handler(500, server_error_handler)
# Create tables on startup
@asynccontextmanager
async def lifespan(app):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
# Register all routes
app.include_router(users.router)
app.include_router(notes.router)
app.include_router(files.router)

@app.get("/")
def root():
    return {
        "message": "SecureVault API is running",
        "docs": "/docs"
    }