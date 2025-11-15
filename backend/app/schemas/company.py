"""Company schemas"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.company import IndustryEnum, CompanySizeEnum


class CompanyBase(BaseModel):
    """Базовая схема компании"""
    name: str = Field(..., min_length=1, max_length=200, description="Название компании")
    inn: str = Field(..., description="ИНН (10 или 12 цифр)")
    industry: IndustryEnum = Field(..., description="Отрасль")
    size: CompanySizeEnum = Field(default=CompanySizeEnum.SMALL, description="Размер компании")
    
    description: Optional[str] = Field(None, max_length=1000)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    
    @field_validator('inn')
    @classmethod
    def validate_inn(cls, v: str) -> str:
        """Валидация ИНН"""
        # Удаляем пробелы
        v = v.strip()
        
        # Проверяем что только цифры
        if not v.isdigit():
            raise ValueError('ИНН должен содержать только цифры')
        
        # Проверяем длину (10 для ЮЛ, 12 для ИП)
        if len(v) not in (10, 12):
            raise ValueError('ИНН должен содержать 10 (для ЮЛ) или 12 (для ИП) цифр')
        
        return v


class CompanyCreate(CompanyBase):
    """Схема создания компании"""
    pass


class CompanyUpdate(BaseModel):
    """Схема обновления компании"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    inn: Optional[str] = None
    industry: Optional[IndustryEnum] = None
    size: Optional[CompanySizeEnum] = None
    description: Optional[str] = Field(None, max_length=1000)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    
    @field_validator('inn')
    @classmethod
    def validate_inn(cls, v: Optional[str]) -> Optional[str]:
        """Валидация ИНН"""
        if v is None:
            return v
        
        v = v.strip()
        if not v.isdigit():
            raise ValueError('ИНН должен содержать только цифры')
        if len(v) not in (10, 12):
            raise ValueError('ИНН должен содержать 10 или 12 цифр')
        
        return v


class CompanyResponse(CompanyBase):
    """Схема ответа с данными компании"""
    id: UUID
    owner_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

