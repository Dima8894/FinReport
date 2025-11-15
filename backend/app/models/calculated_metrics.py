"""
Calculated Metrics model

FR-3.1: Калькулятор метрик
Хранит рассчитанные финансовые показатели (11 метрик)
"""

from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class CalculatedMetrics(Base):
    """
    Модель рассчитанных финансовых показателей
    
    11 ключевых метрик:
    1. Выручка и прогноз
    2. Маржинальность (Gross Margin)
    3. Рентабельность продаж (ROS)
    4. Величина активов
    5. Рентабельность активов (ROA)
    6. Рентабельность капитала (ROE)
    7-9. Коэффициенты ликвидности (3 шт)
    10. Финансовая независимость
    11. Оборачиваемость активов
    + Чистый оборотный капитал
    + Коэффициент оборотного капитала
    """
    __tablename__ = "calculated_metrics"
    
    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign Keys
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    financial_data_id = Column(UUID(as_uuid=True), ForeignKey("financial_data.id"), nullable=False, unique=True)
    
    # ============ Метрики ============
    
    # 1. Выручка и прогноз
    revenue = Column(Float, nullable=False, comment="Выручка (факт)")
    revenue_forecast = Column(Float, nullable=True, comment="Прогноз выручки")
    
    # 2. Маржинальность (%)
    gross_margin = Column(Float, nullable=False, comment="(Валовая прибыль / Выручка) × 100%")
    
    # 3. Рентабельность продаж (%)
    ros = Column(Float, nullable=False, comment="Return on Sales: (Чистая прибыль / Выручка) × 100%")
    
    # 4. Величина активов
    total_assets = Column(Float, nullable=False, comment="Оборотные + Внеоборотные активы")
    
    # 5. Рентабельность активов (%)
    roa = Column(Float, nullable=False, comment="Return on Assets: (Чистая прибыль / Средние активы) × 100%")
    
    # 6. Рентабельность капитала (%)
    roe = Column(Float, nullable=False, comment="Return on Equity: (Чистая прибыль / Средний капитал) × 100%")
    
    # 7. Коэффициент текущей ликвидности
    current_ratio = Column(Float, nullable=False, comment="Оборотные активы / Краткосрочные обязательства")
    
    # 8. Коэффициент быстрой ликвидности
    quick_ratio = Column(Float, nullable=False, comment="(Оборотные активы - Запасы) / Краткосрочные обязательства")
    
    # 9. Коэффициент абсолютной ликвидности
    cash_ratio = Column(Float, nullable=False, comment="Денежные средства / Краткосрочные обязательства")
    
    # 10. Коэффициент финансовой независимости
    autonomy_ratio = Column(Float, nullable=False, comment="Собственный капитал / Валюта баланса")
    
    # 11. Коэффициент оборачиваемости активов
    asset_turnover = Column(Float, nullable=False, comment="Выручка / Средние активы")
    
    # Дополнительные метрики
    net_working_capital = Column(Float, nullable=False, comment="Оборотные активы - Краткосрочные обязательства")
    working_capital_ratio = Column(Float, nullable=False, comment="Текущие активы / Текущие обязательства")
    
    # ============ Статус метрик (индикаторы) ============
    
    # Статусы: "good", "warning", "bad"
    gross_margin_status = Column(String(10), nullable=True, comment="Статус маржинальности")
    ros_status = Column(String(10), nullable=True)
    roa_status = Column(String(10), nullable=True)
    roe_status = Column(String(10), nullable=True)
    liquidity_status = Column(String(10), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    company = relationship("Company", back_populates="calculated_metrics")
    financial_data = relationship("FinancialData", back_populates="metrics")
    
    def __repr__(self) -> str:
        return f"<CalculatedMetrics(id={self.id}, revenue={self.revenue}, ros={self.ros}%)>"
    
    def assess_status(self) -> dict:
        """
        Оценка статуса метрик по отраслевым бенчмаркам
        
        Returns:
            dict с оценками каждой метрики
        """
        return {
            "gross_margin": self._assess_gross_margin(),
            "ros": self._assess_ros(),
            "roa": self._assess_roa(),
            "roe": self._assess_roe(),
            "current_ratio": self._assess_current_ratio(),
        }
    
    def _assess_gross_margin(self) -> str:
        """Маржа: 30-50% норма"""
        if self.gross_margin >= 30:
            return "good"
        elif self.gross_margin >= 20:
            return "warning"
        return "bad"
    
    def _assess_ros(self) -> str:
        """ROS: 10-20% норма"""
        if self.ros >= 10:
            return "good"
        elif self.ros >= 5:
            return "warning"
        return "bad"
    
    def _assess_roa(self) -> str:
        """ROA: 5-15% норма"""
        if self.roa >= 5:
            return "good"
        elif self.roa >= 2:
            return "warning"
        return "bad"
    
    def _assess_roe(self) -> str:
        """ROE: 15-25% норма"""
        if self.roe >= 15:
            return "good"
        elif self.roe >= 10:
            return "warning"
        return "bad"
    
    def _assess_current_ratio(self) -> str:
        """Текущая ликвидность: >1.5 норма"""
        if self.current_ratio >= 1.5:
            return "good"
        elif self.current_ratio >= 1.0:
            return "warning"
        return "bad"

