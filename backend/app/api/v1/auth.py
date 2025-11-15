"""
Authentication API endpoints

FR-1.1: Telegram OAuth authentication
"""

import hashlib
import hmac
from typing import Dict
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import TelegramAuthData, Token, LoginResponse
from app.schemas.user import UserResponse
from app.api.deps import get_current_user

router = APIRouter()


def verify_telegram_auth(auth_data: TelegramAuthData) -> bool:
    """
    Верификация данных от Telegram
    
    Проверяем что данные действительно пришли от Telegram,
    используя bot token для создания hash
    
    Алгоритм: https://core.telegram.org/widgets/login#checking-authorization
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    
    # Создаем data_check_string
    data_check_arr = []
    data_dict = auth_data.model_dump(exclude={'hash'})
    
    for key in sorted(data_dict.keys()):
        value = data_dict[key]
        if value is not None:
            data_check_arr.append(f"{key}={value}")
    
    data_check_string = "\n".join(data_check_arr)
    
    # Создаем secret key из bot token
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    
    # Создаем hash
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Сравниваем с полученным hash
    return calculated_hash == auth_data.hash


@router.post("/telegram", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def telegram_login(
    auth_data: TelegramAuthData,
    db: Session = Depends(get_db)
):
    """
    Telegram OAuth login endpoint
    
    FR-1.1: Аутентификация через Telegram
    
    Flow:
    1. Frontend использует Telegram Login Widget
    2. Telegram возвращает auth_data
    3. Frontend отправляет auth_data на этот endpoint
    4. Мы верифицируем данные
    5. Создаем или обновляем пользователя
    6. Возвращаем JWT token
    """
    
    # 1. Верифицируем данные от Telegram
    if not verify_telegram_auth(auth_data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Telegram authentication data"
        )
    
    # 2. Проверяем что данные не устарели (макс 24 часа)
    auth_timestamp = datetime.fromtimestamp(auth_data.auth_date)
    if datetime.utcnow() - auth_timestamp > timedelta(hours=24):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication data expired"
        )
    
    # 3. Ищем существующего пользователя
    user = db.query(User).filter(User.telegram_id == auth_data.id).first()
    
    is_new_user = False
    
    if user is None:
        # 4. Создаем нового пользователя
        user = User(
            telegram_id=auth_data.id,
            telegram_username=auth_data.username,
            telegram_first_name=auth_data.first_name,
            telegram_last_name=auth_data.last_name,
            telegram_photo_url=auth_data.photo_url,
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        is_new_user = True
    else:
        # 5. Обновляем данные существующего пользователя
        user.telegram_username = auth_data.username
        user.telegram_first_name = auth_data.first_name
        user.telegram_last_name = auth_data.last_name
        user.telegram_photo_url = auth_data.photo_url
        user.last_login_at = datetime.utcnow()
    
    db.commit()
    db.refresh(user)
    
    # 6. Создаем JWT token
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": str(user.id), "telegram_id": user.telegram_id},
        expires_delta=access_token_expires
    )
    
    # 7. Формируем response
    token = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds())
    )
    
    return LoginResponse(
        token=token,
        user={
            "id": str(user.id),
            "telegram_id": user.telegram_id,
            "username": user.telegram_username,
            "full_name": user.full_name,
            "is_active": user.is_active
        },
        is_new_user=is_new_user
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Получить информацию о текущем пользователе
    
    Требует авторизации (JWT token в header)
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint
    
    Note: JWT tokens stateless, поэтому на backend стороне мы не можем
    их "отозвать". Frontend должен удалить token из localStorage.
    """
    return {
        "success": True,
        "message": "Successfully logged out"
    }

