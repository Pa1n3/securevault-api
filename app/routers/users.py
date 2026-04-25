from fastapi import APIRouter, HTTPException, Depends
from app.limiter import limiter 
from fastapi import Request
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse, ForgotPassword
from app.database import execute_query
import secrets
import hashlib
from app.auth import (
    hash_password, verify_password,
    create_access_token, generate_api_key,
    get_current_user, require_admin
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse)
def register(data: UserRegister):
    # Check if username or email already exists

    existing = execute_query(
        "SELECT id FROM users WHERE username = %s OR email = %s",
        (data.username, data.email),
        fetch='one'
    )
    
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already taken")
    
    # Hash the password — NEVER store plaintext
    hashed = hash_password(data.password)
    api_key = generate_api_key()
    
    # Insert new user
    user = execute_query(
        """
        INSERT INTO users (username, email, password, api_key)
        VALUES (%s, %s, %s, %s)
        RETURNING id, username, email, role, api_key
        """,
        (data.username, data.email, hashed, api_key),
        fetch='one'
    )
    
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "role": user[3],
        "api_key": user[4]
    }


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request:Request , data: UserLogin):
    # Find user
    
    user = execute_query(
        "SELECT id, username, password, role FROM users WHERE username = %s",
        (data.username,),
        fetch='one'
    )
    
    # IMPORTANT: Always say "Invalid credentials" never "User not found"
    # Telling attackers which field is wrong is an info leak
    if not user or not verify_password(data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create JWT
    token = create_access_token({
        "sub": user[1],
        "user_id": user[0],
        "role": user[3]
    })
    
    return {"access_token": token}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    """Get your own profile"""
    user = execute_query(
        "SELECT id, username, email, role, api_key FROM users WHERE id = %s",
        (current_user["id"],),
        fetch='one'
    )
    return {
        "id": user[0], "username": user[1],
        "email": user[2], "role": user[3], "api_key": user[4]
    }

@router.post("/forgot-password")
@router.post("/forgot-password")
@router.post("/forgot-password")
def create_token(data: ForgotPassword):
    user = execute_query(
        "SELECT id FROM users WHERE email = %s",
        (data.email,),
        fetch='one'
    )

    if not user:
        raise HTTPException(status_code=401, detail="Email Not Found")

    token = secrets.token_urlsafe(32)

    execute_query("""
        INSERT INTO password_resets(user_id, token, expires_at)
        VALUES (%s, %s, NOW() + INTERVAL '10 minutes')
    """, (user[0], token))

    return {"token": token}
     
    

@router.get("/all")
def get_all_users(admin: dict = Depends(require_admin)):
    """Admin only — see all users"""
    users = execute_query(
        "SELECT id, username, email, role, created_at FROM users",
        fetch='all'
    )
    return [{"id": u[0], "username": u[1], "email": u[2], 
             "role": u[3], "created_at": str(u[4])} for u in users]