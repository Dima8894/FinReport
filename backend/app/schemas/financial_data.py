"""Financial Data schemas"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class PLData(BaseModel):
    """
    Схема для данных P&L (Отчет о прибылях и убытках)
    
    FR-2.1: Структура входного файла - Лист 1
    """
    revenue: float = Field(..., gt=0, description="Выручка")
    cogs: float = Field(..., ge=0, description="Себестоимость")
    gross_profit: float = Field(..., description="Валовая прибыль")
    operating_expenses: float = Field(..., ge=0, description="Операционные расходы")
    ebit: float = Field(..., description="Прибыль до налогообложения")
    net_profit: float = Field(..., description="Чистая прибыль")
    
    @field_validator('revenue')
    @classmethod
    def revenue_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Выручка должна быть положительной')
        return v


class BalanceData(BaseModel):
    """
    Схема для данных Баланса
    
    FR-2.1: Структура входного файла - Лист 2
    """
    # Активы
    current_assets: float = Field(..., ge=0, description="Оборотные активы")
    non_current_assets: float = Field(..., ge=0, description="Внеоборотные активы")
    
    # Обязательства
    current_liabilities: float = Field(..., ge=0, description="Краткосрочные обязательства")
    non_current_liabilities: float = Field(..., ge=0, description="Долгосрочные обязательства")
    
    # Капитал
    equity: float = Field(..., description="Собственный капитал")
    
    # Детализация
    cash: float = Field(..., ge=0, description="Денежные средства")
    receivables: float = Field(..., ge=0, description="Дебиторская задолженность")
    inventory: float = Field(..., ge=0, description="Запасы")
    
    @field_validator('current_assets', 'non_current_assets', 'current_liabilities', 
                     'non_current_liabilities', 'cash', 'receivables', 'inventory')
    @classmethod
    def non_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Значение не может быть отрицательным')
        return v
    
    def validate_balance_equation(self) -> bool:
        """
        Проверка балансового уравнения:
        Активы = Обязательства + Капитал
        """
        assets = self.current_assets + self.non_current_assets
        liabilities_and_equity = self.current_liabilities + self.non_current_liabilities + self.equity
        
        # Допускаем погрешность 0.1%
        if assets == 0:
            return False
        
        diff_percentage = abs(assets - liabilities_and_equity) / assets
        return diff_percentage < 0.001


class FinancialDataCreate(BaseModel):
    """Схема создания финансовых данных"""
    company_id: UUID
    period_start: datetime
    period_end: datetime
    period_name: str = Field(..., min_length=1, max_length=100, description="Название периода")
    
    # P&L данные
    pl_data: PLData
    
    # Balance данные
    balance_data: BalanceData
    
    # Metadata
    source_filename: Optional[str] = Field(None, max_length=255)
    source_file_type: Optional[str] = Field(None, max_length=20)
    upload_notes: Optional[str] = None
    
    def model_post_init(self, __context) -> None:
        """Дополнительная валидация после инициализации"""
        # Проверяем балансовое уравнение
        if not self.balance_data.validate_balance_equation():
            raise ValueError(
                'Балансовое уравнение не сходится: '
                'Активы должны равняться Обязательства + Капитал'
            )


class FinancialDataResponse(BaseModel):
    """Схема ответа с финансовыми данными"""
    id: UUID
    company_id: UUID
    period_start: datetime
    period_end: datetime
    period_name: str
    
    # P&L
    revenue: float
    cogs: float
    gross_profit: float
    operating_expenses: float
    ebit: float
    net_profit: float
    
    # Balance
    current_assets: float
    non_current_assets: float
    current_liabilities: float
    non_current_liabilities: float
    equity: float
    cash: float
    receivables: float
    inventory: float
    
    # Metadata
    source_filename: Optional[str]
    source_file_type: Optional[str]
    version: int
    created_at: datetime
    updated_at: datetime
    
    # Computed
    total_assets: float
    total_liabilities: float
    
    class Config:
        from_attributes = True

