"""
User model

Хранит пользователей, аутентифицированных через Telegram
"""

from sqlalchemy import Column, String, BigInteger, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class User(Base):
    """
    Модель пользователя
    
    FR-1.1: Аутентификация через Telegram
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Telegram Data
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username = Column(String(255), nullable=True)
    telegram_first_name = Column(String(255), nullable=True)
    telegram_last_name = Column(String(255), nullable=True)
    telegram_photo_url = Column(String(500), nullable=True)
    
    # User Info
    email = Column(String(255), nullable=True, unique=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    companies = relationship("Company", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.telegram_username})>"
    
    @property
    def full_name(self) -> str:
        """Полное имя пользователя из Telegram"""
        parts = []
        if self.telegram_first_name:
            parts.append(self.telegram_first_name)
        if self.telegram_last_name:
            parts.append(self.telegram_last_name)
        return " ".join(parts) if parts else self.telegram_username or f"User {self.telegram_id}"

