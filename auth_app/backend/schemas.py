from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    confirm_password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age_group: Optional[str] = None
    gender: Optional[str] = None
    language: Optional[str] = None

    class Config:
        orm_mode = True   # important for returning SQLAlchemy objects directly

class ProfileUpdateRequest(BaseModel):
    # Allow partial updates
    name: Optional[str] = None
    new_password: Optional[str] = Field(default=None, min_length=6, max_length=128)
    age_group: Optional[str] = None
    gender: Optional[str] = None
    language: Optional[str] = None
