from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum

class UserRole(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: Optional[UserRole] = UserRole.viewer

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
