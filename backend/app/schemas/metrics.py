"""Calculated Metrics schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict
from uuid import UUID


class CalculatedMetricsResponse(BaseModel):
    """
    Схема ответа с рассчитанными метриками
    
    FR-3.1: Все 11 ключевых показателей
    """
    id: UUID
    company_id: UUID
    financial_data_id: UUID
    
    # 1. Выручка и прогноз
    revenue: float = Field(..., description="Выручка (факт)")
    revenue_forecast: Optional[float] = Field(None, description="Прогноз выручки")
    
    # 2. Маржинальность (%)
    gross_margin: float = Field(..., description="Маржинальность, %")
    
    # 3. Рентабельность продаж (%)
    ros: float = Field(..., description="Return on Sales, %")
    
    # 4. Величина активов
    total_assets: float = Field(..., description="Общие активы")
    
    # 5. Рентабельность активов (%)
    roa: float = Field(..., description="Return on Assets, %")
    
    # 6. Рентабельность капитала (%)
    roe: float = Field(..., description="Return on Equity, %")
    
    # 7. Коэффициент текущей ликвидности
    current_ratio: float = Field(..., description="Текущая ликвидность")
    
    # 8. Коэффициент быстрой ликвидности
    quick_ratio: float = Field(..., description="Быстрая ликвидность")
    
    # 9. Коэффициент абсолютной ликвидности
    cash_ratio: float = Field(..., description="Абсолютная ликвидность")
    
    # 10. Коэффициент финансовой независимости
    autonomy_ratio: float = Field(..., description="Финансовая независимость")
    
    # 11. Коэффициент оборачиваемости активов
    asset_turnover: float = Field(..., description="Оборачиваемость активов")
    
    # Дополнительные
    net_working_capital: float = Field(..., description="Чистый оборотный капитал")
    working_capital_ratio: float = Field(..., description="Коэффициент оборотного капитала")
    
    # Статусы метрик
    gross_margin_status: Optional[str] = Field(None, description="good/warning/bad")
    ros_status: Optional[str] = None
    roa_status: Optional[str] = None
    roe_status: Optional[str] = None
    liquidity_status: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MetricsSummary(BaseModel):
    """Краткая сводка ключевых метрик для дашборда"""
    revenue: float
    gross_margin: float
    ros: float
    roa: float
    roe: float
    current_ratio: float
    
    # Статусы (для цветовых индикаторов)
    statuses: Dict[str, str] = Field(
        ..., 
        description="Статусы метрик: {'gross_margin': 'good', ...}"
    )


class MetricsComparison(BaseModel):
    """Сравнение метрик между периодами"""
    current: CalculatedMetricsResponse
    previous: Optional[CalculatedMetricsResponse]
    
    # Изменения в процентах
    revenue_change: Optional[float] = Field(None, description="Изменение выручки, %")
    gross_margin_change: Optional[float] = None
    ros_change: Optional[float] = None
    roa_change: Optional[float] = None

