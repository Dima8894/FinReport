"""Authentication schemas"""

from pydantic import BaseModel, Field
from typing import Optional


class Token(BaseModel):
    """JWT Token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token lifetime in seconds")


class TokenData(BaseModel):
    """Data stored in JWT token payload"""
    user_id: str = Field(..., description="User UUID")
    telegram_id: int = Field(..., description="Telegram ID")


class TelegramAuthData(BaseModel):
    """
    Данные от Telegram OAuth
    
    FR-1.1: Telegram authentication flow
    
    Telegram отправляет эти данные после авторизации
    """
    id: int = Field(..., description="Telegram user ID")
    first_name: str = Field(..., max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    username: Optional[str] = Field(None, max_length=255)
    photo_url: Optional[str] = Field(None, max_length=500)
    auth_date: int = Field(..., description="Unix timestamp")
    hash: str = Field(..., description="Hash для верификации данных")


class LoginResponse(BaseModel):
    """Response после успешного логина"""
    token: Token
    user: dict = Field(..., description="User info")
    is_new_user: bool = Field(..., description="True если это первый вход")

