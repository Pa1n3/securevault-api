from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ─── User Schemas ─────────────────────────────────────────────

class UserRegister(BaseModel):
    username: str = Field(
        min_length= 3,
        max_length = 30,
        pattern= "^[a-zA-Z0-9_]+$",
    )
    email: EmailStr
    password: str = Field(min_length=8,)


class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    api_key: Optional[str]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─── Note Schemas ─────────────────────────────────────────────

class NoteCreate(BaseModel):
    title: str
    content: str
    is_private: bool = True


class NoteUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_private: Optional[bool]


class NoteResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    is_private: bool    
# ─── Password Schemas ─────────────────────────────────────────────

class ForgotPassword(BaseModel):
    email : EmailStr
class ResetPassword(BaseModel):  
    token: str
    new_password : str = Field(min_length=8,)
    confirm_password: str
