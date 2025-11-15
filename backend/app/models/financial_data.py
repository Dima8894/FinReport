"""
Financial Data model

FR-2.1: Загрузка Excel/CSV файлов
Хранит исходные финансовые данные из загруженных файлов
"""

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class FinancialData(Base):
    """
    Модель финансовых данных
    
    Содержит:
    - P&L (Отчет о прибылях и убытках)
    - Balance Sheet (Баланс)
    """
    __tablename__ = "financial_data"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    
    # Period Info
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    period_name = Column(String(100), nullable=False, index=True)  # например "Октябрь 2024"
    
    # ============ P&L Data (Отчет о прибылях и убытках) ============
    
    # Выручка
    revenue = Column(Float, nullable=False)
    
    # Себестоимость
    cogs = Column(Float, nullable=False, comment="Cost of Goods Sold")
    
    # Валовая прибыль
    gross_profit = Column(Float, nullable=False)
    
    # Операционные расходы
    operating_expenses = Column(Float, nullable=False)
    
    # Прибыль до налогообложения
    ebit = Column(Float, nullable=False, comment="Earnings Before Interest and Taxes")
    
    # Чистая прибыль
    net_profit = Column(Float, nullable=False)
    
    # ============ Balance Sheet (Баланс) ============
    
    # Активы
    current_assets = Column(Float, nullable=False, comment="Оборотные активы")
    non_current_assets = Column(Float, nullable=False, comment="Внеоборотные активы")
    
    # Обязательства
    current_liabilities = Column(Float, nullable=False, comment="Краткосрочные обязательства")
    non_current_liabilities = Column(Float, nullable=False, comment="Долгосрочные обязательства")
    
    # Капитал
    equity = Column(Float, nullable=False, comment="Собственный капитал")
    
    # Детализация оборотных активов
    cash = Column(Float, nullable=False, comment="Денежные средства")
    receivables = Column(Float, nullable=False, comment="Дебиторская задолженность")
    inventory = Column(Float, nullable=False, comment="Запасы")
    
    # ============ Metadata ============
    
    # Upload info
    source_filename = Column(String(255), nullable=True, comment="Имя загруженного файла")
    source_file_type = Column(String(20), nullable=True, comment="xlsx, xls, csv")
    upload_notes = Column(Text, nullable=True, comment="Заметки о загрузке")
    
    # Version control
    version = Column(Integer, default=1, nullable=False, comment="Версия данных (для обновлений)")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="financial_data")
    metrics = relationship("CalculatedMetrics", back_populates="financial_data", uselist=False)
    
    def __repr__(self) -> str:
        return f"<FinancialData(id={self.id}, period={self.period_name}, revenue={self.revenue})>"
    
    @property
    def total_assets(self) -> float:
        """Величина активов"""
        return self.current_assets + self.non_current_assets
    
    @property
    def total_liabilities(self) -> float:
        """Общие обязательства"""
        return self.current_liabilities + self.non_current_liabilities
    
    def validate_balance(self) -> bool:
        """
        Проверка балансового уравнения:
        Активы = Обязательства + Капитал
        """
        assets = self.total_assets
        liabilities_and_equity = self.total_liabilities + self.equity
        
        # Допускаем погрешность 0.01% (округление)
        return abs(assets - liabilities_and_equity) / assets < 0.0001

