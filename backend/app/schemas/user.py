"""User schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    telegram_id: int = Field(..., description="Telegram ID")
    telegram_username: Optional[str] = Field(None, max_length=255)
    telegram_first_name: Optional[str] = Field(None, max_length=255)
    telegram_last_name: Optional[str] = Field(None, max_length=255)
    telegram_photo_url: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """Схема создания пользователя"""
    pass


class UserResponse(UserBase):
    """Схема ответа с данными пользователя"""
    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login_at: Optional[datetime]
    full_name: str
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Схема обновления пользователя"""
    email: Optional[str] = Field(None, max_length=255)
    telegram_username: Optional[str] = Field(None, max_length=255)

