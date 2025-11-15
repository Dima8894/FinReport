"""
Company model

FR-1.2: Профиль компании
"""

from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class IndustryEnum(str, enum.Enum):
    """Отрасли компаний"""
    TRADE = "trade"
    MANUFACTURING = "manufacturing"
    SERVICES = "services"
    IT = "it"
    CONSTRUCTION = "construction"
    FINANCE = "finance"
    OTHER = "other"


class CompanySizeEnum(str, enum.Enum):
    """Размер компании"""
    SMALL = "small"  # Малый бизнес (до 300 млн руб/год)
    MEDIUM = "medium"  # Средний бизнес (300 млн - 2 млрд руб/год)


class Company(Base):
    """
    Модель компании
    
    Связана с пользователем 1:Many (у пользователя может быть несколько компаний)
    """
    __tablename__ = "companies"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Owner
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Company Info
    name = Column(String(200), nullable=False)
    inn = Column(String(12), nullable=False, index=True)  # ИНН (10 или 12 цифр)
    industry = Column(Enum(IndustryEnum), nullable=False, default=IndustryEnum.OTHER)
    size = Column(Enum(CompanySizeEnum), nullable=False, default=CompanySizeEnum.SMALL)
    
    # Optional fields
    description = Column(String(1000), nullable=True)
    address = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="companies")
    financial_data = relationship("FinancialData", back_populates="company", cascade="all, delete-orphan")
    calculated_metrics = relationship("CalculatedMetrics", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name={self.name}, inn={self.inn})>"
    
    def validate_inn(self) -> bool:
        """
        Валидация ИНН
        
        ИНН может быть:
        - 10 цифр (для юридических лиц)
        - 12 цифр (для индивидуальных предпринимателей)
        """
        return self.inn.isdigit() and len(self.inn) in (10, 12)

