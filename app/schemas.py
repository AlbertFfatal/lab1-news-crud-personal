import re

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
from pydantic import EmailStr, validator
class UserBase(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None

class UserCreate(UserBase):
    is_author_verified: Optional[bool] = False

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    is_author_verified: Optional[bool] = None

class UserOut(UserBase):
    id: int
    registration_date: datetime
    is_author_verified: bool

    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    content: Dict  # JSON
    cover: Optional[str] = None

class NewsCreate(NewsBase):
    author_id: int

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[Dict] = None
    cover: Optional[str] = None

class NewsOut(NewsBase):
    id: int
    publication_date: datetime
    author_id: int

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    news_id: int
    author_id: int

class CommentUpdate(BaseModel):
    text: Optional[str] = None

class CommentOut(CommentBase):
    id: int
    news_id: int
    author_id: int
    publication_date: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserRoleUpdate(BaseModel):
    is_author_verified: Optional[bool] = None
    is_admin: Optional[bool] = None

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    is_author_verified: Optional[bool] = False
    is_admin: Optional[bool] = False
    avatar: Optional[str] = None

    @validator('email')
    def validate_email(cls, v):
        if len(v) < 3 or len(v) > 32 or not re.match(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Invalid email format")
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8 or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v):
            raise ValueError("Invalid password format")
        return v

class UserLogin(BaseModel):
    email: str
    password: str

class CommentCreateProtected(BaseModel):
    text: str
    news_id: int