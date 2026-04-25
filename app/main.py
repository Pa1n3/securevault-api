from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.models import create_tables
from app.routers import users, notes, files



app = FastAPI(
    title="SecureVault API",
    description="A learning project with intentional security features and bugs",
    version="1.0.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Create tables on startup
@app.on_event("startup")
def startup():
    create_tables()

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