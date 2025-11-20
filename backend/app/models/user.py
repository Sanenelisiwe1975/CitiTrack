"""User models"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles"""
    CITIZEN = "citizen"
    OFFICER = "officer"
    ADMIN = "admin"


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    phone: Optional[str] = None
    full_name: str
    role: UserRole = UserRole.CITIZEN


class UserCreate(UserBase):
    """Create user request"""
    password: str = Field(..., min_length=8)


class User(UserBase):
    """User model"""
    id: str
    is_active: bool = True
    created_at: datetime
    reports_count: int = 0
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None