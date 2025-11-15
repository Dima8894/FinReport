# Архитектура FinReportAI

**Версия:** 1.0.0  
**Дата:** 2024-11-15  
**Статус:** Утверждено

## 1. Обзор архитектуры

### 1.1 Архитектурный стиль

**Тип:** Трехзвенная веб-архитектура (Three-tier Architecture)  
**Паттерн:** Clean Architecture + Service Layer

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (Next.js 14 - App Router)                  │
│                                                           │
│  Pages → Components → Hooks → API Client                │
└─────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│                    (FastAPI Backend)                     │
│                                                           │
│  API Routes → Services → Repository → Models            │
└─────────────────────────────────────────────────────────┘
                            ↓ SQL
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                          │
│               (PostgreSQL + Redis)                       │
│                                                           │
│  Tables → Indexes → Constraints → Triggers              │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Ключевые принципы

1. **Separation of Concerns** - четкое разделение слоев
2. **DRY** - Don't Repeat Yourself
3. **SOLID** - особенно Single Responsibility и Dependency Inversion
4. **API-First** - контракты OpenAPI перед реализацией
5. **Security by Design** - безопасность встроена, а не добавлена потом
6. **Fail Fast** - валидация на входе, быстрая обработка ошибок

---

## 2. Backend Architecture (Python/FastAPI)

### 2.1 Структура проекта

```
backend/
├── app/
│   ├── main.py                 # Точка входа FastAPI
│   ├── __init__.py
│   │
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── deps.py            # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py        # /api/v1/auth
│   │       ├── companies.py   # /api/v1/companies
│   │       ├── uploads.py     # /api/v1/uploads
│   │       └── metrics.py     # /api/v1/metrics
│   │
│   ├── core/                   # Конфигурация и утилиты
│   │   ├── __init__.py
│   │   ├── config.py          # Settings (Pydantic)
│   │   ├── security.py        # JWT, hashing
│   │   └── logging.py         # Structured logging
│   │
│   ├── models/                 # SQLAlchemy ORM модели
│   │   ├── __init__.py
│   │   ├── base.py            # Base model
│   │   ├── user.py
│   │   ├── company.py
│   │   ├── financial_data.py
│   │   └── calculated_metric.py
│   │
│   ├── schemas/                # Pydantic схемы (DTO)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── company.py
│   │   ├── upload.py
│   │   └── metrics.py
│   │
│   ├── services/               # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── file_processor.py   # Excel/CSV парсинг
│   │   ├── metrics_calculator.py
│   │   └── forecast_service.py
│   │
│   ├── repositories/           # Data Access Layer
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repo.py
│   │   └── company_repo.py
│   │
│   ├── utils/                  # Вспомогательные утилиты
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── formatters.py
│   │
│   └── db/                     # Database setup
│       ├── __init__.py
│       ├── session.py          # DB session
│       └── migrations/         # Alembic migrations
│
├── tests/                      # Pytest тесты
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_utils/
│
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── Dockerfile
└── README.md
```

### 2.2 Технологический стек Backend

| Компонент | Технология | Версия | Назначение |
|-----------|-----------|---------|------------|
| **Framework** | FastAPI | 0.109+ | Web framework |
| **ORM** | SQLAlchemy | 2.0+ | Database ORM |
| **Validation** | Pydantic | 2.5+ | Data validation |
| **Database** | PostgreSQL | 14+ | Primary database |
| **Cache** | Redis | 7+ | Caching layer |
| **Migrations** | Alembic | 1.13+ | DB migrations |
| **Auth** | python-jose | 3.3+ | JWT tokens |
| **Excel** | pandas | 2.1+ | Excel/CSV parsing |
|  | openpyxl | 3.1+ | Excel read/write |
| **Testing** | pytest | 7.4+ | Test framework |
|  | httpx | 0.25+ | HTTP client for tests |
| **Tasks** | Celery | 5.3+ | Background jobs |
| **Logging** | structlog | 23.3+ | Structured logging |
| **Validation** | python-multipart | 0.0.6+ | File uploads |

### 2.3 Database Schema

**ER-диаграмма:**

```
┌─────────────────┐         ┌──────────────────┐
│     users       │         │    companies     │
├─────────────────┤         ├──────────────────┤
│ id (PK)         │────┐    │ id (PK)          │
│ telegram_id     │    │    │ user_id (FK)     │
│ telegram_username│   └───>│ name             │
│ email           │         │ inn              │
│ created_at      │         │ industry         │
│ updated_at      │         │ size             │
└─────────────────┘         │ created_at       │
                            │ updated_at       │
                            └──────────────────┘
                                     │
                                     │ 1:N
                                     ↓
                            ┌──────────────────┐
                            │ financial_data   │
                            ├──────────────────┤
                            │ id (PK)          │
                            │ company_id (FK)  │
                            │ period_month     │
                            │ period_year      │
                            │ revenue          │
                            │ cogs             │
                            │ gross_profit     │
                            │ operating_exp    │
                            │ net_profit       │
                            │ current_assets   │
                            │ non_current_ass  │
                            │ current_liab     │
                            │ non_current_liab │
                            │ equity           │
                            │ cash             │
                            │ receivables      │
                            │ inventory        │
                            │ uploaded_at      │
                            │ file_name        │
                            └──────────────────┘
                                     │
                                     │ 1:1
                                     ↓
                            ┌──────────────────┐
                            │calculated_metrics│
                            ├──────────────────┤
                            │ id (PK)          │
                            │ financial_data_id│
                            │ revenue          │
                            │ gross_margin     │
                            │ ros              │
                            │ roa              │
                            │ roe              │
                            │ current_ratio    │
                            │ quick_ratio      │
                            │ cash_ratio       │
                            │ autonomy_ratio   │
                            │ asset_turnover   │
                            │ nwc              │
                            │ working_cap_ratio│
                            │ calculated_at    │
                            └──────────────────┘
```

**SQL Schema:**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(255),
    email VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    trial_ends_at TIMESTAMP,
    subscription_tier VARCHAR(50) DEFAULT 'trial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Companies table
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    inn VARCHAR(12) NOT NULL,
    industry VARCHAR(50),
    size VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_company UNIQUE(user_id)
);

-- Financial data table
CREATE TABLE financial_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    period_month INTEGER NOT NULL CHECK (period_month BETWEEN 1 AND 12),
    period_year INTEGER NOT NULL CHECK (period_year BETWEEN 2000 AND 2100),
    
    -- P&L data
    revenue DECIMAL(15,2) NOT NULL CHECK (revenue >= 0),
    cogs DECIMAL(15,2) NOT NULL CHECK (cogs >= 0),
    gross_profit DECIMAL(15,2) NOT NULL,
    operating_expenses DECIMAL(15,2) NOT NULL CHECK (operating_expenses >= 0),
    ebit DECIMAL(15,2) NOT NULL,
    net_profit DECIMAL(15,2) NOT NULL,
    
    -- Balance sheet data
    current_assets DECIMAL(15,2) NOT NULL CHECK (current_assets >= 0),
    non_current_assets DECIMAL(15,2) NOT NULL CHECK (non_current_assets >= 0),
    current_liabilities DECIMAL(15,2) NOT NULL CHECK (current_liabilities >= 0),
    non_current_liabilities DECIMAL(15,2) NOT NULL CHECK (non_current_liabilities >= 0),
    equity DECIMAL(15,2) NOT NULL,
    cash DECIMAL(15,2) NOT NULL CHECK (cash >= 0),
    receivables DECIMAL(15,2) NOT NULL CHECK (receivables >= 0),
    inventory DECIMAL(15,2) NOT NULL CHECK (inventory >= 0),
    
    -- Metadata
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_name VARCHAR(255),
    
    CONSTRAINT unique_period UNIQUE(company_id, period_month, period_year)
);

-- Calculated metrics table
CREATE TABLE calculated_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    financial_data_id UUID NOT NULL REFERENCES financial_data(id) ON DELETE CASCADE,
    
    -- All 11 metrics
    revenue DECIMAL(15,2),
    revenue_forecast DECIMAL(15,2),
    gross_margin DECIMAL(5,2),
    ros DECIMAL(5,2),
    total_assets DECIMAL(15,2),
    roa DECIMAL(5,2),
    roe DECIMAL(5,2),
    current_ratio DECIMAL(5,2),
    quick_ratio DECIMAL(5,2),
    cash_ratio DECIMAL(5,2),
    autonomy_ratio DECIMAL(5,2),
    asset_turnover DECIMAL(5,2),
    net_working_capital DECIMAL(15,2),
    working_capital_ratio DECIMAL(5,2),
    
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT unique_metrics UNIQUE(financial_data_id)
);

-- Indexes for performance
CREATE INDEX idx_companies_user ON companies(user_id);
CREATE INDEX idx_financial_data_company ON financial_data(company_id);
CREATE INDEX idx_financial_data_period ON financial_data(period_year, period_month);
CREATE INDEX idx_users_telegram ON users(telegram_id);
```

### 2.4 API Design

**Базовый URL:** `https://api.finreportai.com/api/v1`

**Эндпоинты:**

| Method | Endpoint | Описание | Auth |
|--------|----------|----------|------|
| POST | `/auth/telegram` | Вход через Telegram | No |
| GET | `/auth/me` | Текущий пользователь | Yes |
| POST | `/auth/refresh` | Обновить токен | Yes |
| | | | |
| POST | `/companies` | Создать компанию | Yes |
| GET | `/companies/me` | Моя компания | Yes |
| PUT | `/companies/me` | Обновить компанию | Yes |
| | | | |
| POST | `/uploads` | Загрузить файл | Yes |
| GET | `/uploads` | История загрузок | Yes |
| GET | `/uploads/{id}` | Детали загрузки | Yes |
| | | | |
| GET | `/metrics/latest` | Последние метрики | Yes |
| GET | `/metrics/{period}` | Метрики за период | Yes |
| GET | `/metrics/history` | История метрик | Yes |

**Пример запроса:**

```http
POST /api/v1/uploads HTTP/1.1
Host: api.finreportai.com
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data

------WebKitFormBoundary
Content-Disposition: form-data; name="file"; filename="report_oct_2024.xlsx"
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

[binary data]
------WebKitFormBoundary--
```

**Пример ответа:**

```json
{
  "success": true,
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "period": "2024-10",
    "metrics": {
      "revenue": 1200000,
      "gross_margin": 35.5,
      "ros": 12.3,
      "roa": 8.5,
      "roe": 15.2,
      "current_ratio": 1.8,
      "quick_ratio": 1.2,
      "cash_ratio": 0.5,
      "autonomy_ratio": 0.65,
      "asset_turnover": 1.5,
      "net_working_capital": 450000,
      "working_capital_ratio": 1.8
    },
    "uploaded_at": "2024-11-15T10:30:00Z"
  }
}
```

### 2.5 Services Layer

**MetricsCalculator Service:**

```python
# app/services/metrics_calculator.py

from typing import Dict, Optional
from decimal import Decimal
from app.schemas.financial import FinancialData, CalculatedMetrics
from app.core.logging import get_logger

logger = get_logger(__name__)

class MetricsCalculator:
    """
    Сервис расчета финансовых показателей.
    
    Реализует все 11 метрик согласно requirements.md
    """
    
    def __init__(self, data: FinancialData):
        self.data = data
        self._validate_data()
    
    def _validate_data(self) -> None:
        """Валидация входных данных"""
        if self.data.revenue < 0:
            raise ValueError("Выручка не может быть отрицательной")
        
        # Проверка баланса: Активы = Пассивы
        total_assets = self.data.current_assets + self.data.non_current_assets
        total_liabilities = (
            self.data.current_liabilities + 
            self.data.non_current_liabilities + 
            self.data.equity
        )
        
        if abs(total_assets - total_liabilities) > 0.01:  # tolerance
            logger.warning(f"Баланс не сходится: {total_assets} != {total_liabilities}")
    
    def calculate_all(self) -> CalculatedMetrics:
        """Рассчитывает все 11 показателей"""
        logger.info(f"Начало расчета метрик для выручки {self.data.revenue}")
        
        try:
            metrics = CalculatedMetrics(
                revenue=self.data.revenue,
                gross_margin=self._calculate_gross_margin(),
                ros=self._calculate_ros(),
                total_assets=self._calculate_total_assets(),
                roa=self._calculate_roa(),
                roe=self._calculate_roe(),
                current_ratio=self._calculate_current_ratio(),
                quick_ratio=self._calculate_quick_ratio(),
                cash_ratio=self._calculate_cash_ratio(),
                autonomy_ratio=self._calculate_autonomy_ratio(),
                asset_turnover=self._calculate_asset_turnover(),
                net_working_capital=self._calculate_nwc(),
                working_capital_ratio=self._calculate_working_capital_ratio(),
            )
            
            logger.info("Расчет метрик успешно завершен")
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка при расчете метрик: {str(e)}")
            raise
    
    def _calculate_gross_margin(self) -> Decimal:
        """Маржинальность: (Валовая прибыль / Выручка) × 100%"""
        if self.data.revenue == 0:
            return Decimal(0)
        return (self.data.gross_profit / self.data.revenue) * 100
    
    def _calculate_ros(self) -> Decimal:
        """Рентабельность продаж: (Чистая прибыль / Выручка) × 100%"""
        if self.data.revenue == 0:
            return Decimal(0)
        return (self.data.net_profit / self.data.revenue) * 100
    
    def _calculate_total_assets(self) -> Decimal:
        """Величина активов"""
        return self.data.current_assets + self.data.non_current_assets
    
    def _calculate_roa(self) -> Decimal:
        """ROA: (Чистая прибыль / Средние активы) × 100%"""
        total_assets = self._calculate_total_assets()
        if total_assets == 0:
            return Decimal(0)
        # Для MVP используем текущие активы
        # В Post-MVP: среднее между началом и концом периода
        return (self.data.net_profit / total_assets) * 100
    
    def _calculate_roe(self) -> Decimal:
        """ROE: (Чистая прибыль / Собственный капитал) × 100%"""
        if self.data.equity == 0:
            return Decimal(0)
        return (self.data.net_profit / self.data.equity) * 100
    
    def _calculate_current_ratio(self) -> Decimal:
        """Текущая ликвидность: Оборотные активы / Краткосрочные обязательства"""
        if self.data.current_liabilities == 0:
            return Decimal(999)  # Практически бесконечно
        return self.data.current_assets / self.data.current_liabilities
    
    def _calculate_quick_ratio(self) -> Decimal:
        """Быстрая ликвидность: (Оборотные активы - Запасы) / Краткосрочные обязательства"""
        if self.data.current_liabilities == 0:
            return Decimal(999)
        liquid_assets = self.data.current_assets - self.data.inventory
        return liquid_assets / self.data.current_liabilities
    
    def _calculate_cash_ratio(self) -> Decimal:
        """Абсолютная ликвидность: Денежные средства / Краткосрочные обязательства"""
        if self.data.current_liabilities == 0:
            return Decimal(999)
        return self.data.cash / self.data.current_liabilities
    
    def _calculate_autonomy_ratio(self) -> Decimal:
        """Финансовая независимость: Собственный капитал / Валюта баланса"""
        total_assets = self._calculate_total_assets()
        if total_assets == 0:
            return Decimal(0)
        return self.data.equity / total_assets
    
    def _calculate_asset_turnover(self) -> Decimal:
        """Оборачиваемость активов: Выручка / Средние активы"""
        total_assets = self._calculate_total_assets()
        if total_assets == 0:
            return Decimal(0)
        return self.data.revenue / total_assets
    
    def _calculate_nwc(self) -> Decimal:
        """Чистый оборотный капитал: Оборотные активы - Краткосрочные обязательства"""
        return self.data.current_assets - self.data.current_liabilities
    
    def _calculate_working_capital_ratio(self) -> Decimal:
        """Коэффициент оборотного капитала: Текущие активы / Текущие обязательства"""
        return self._calculate_current_ratio()  # Аналог текущей ликвидности
```

---

## 3. Frontend Architecture (Next.js 14)

### 3.1 Структура проекта

```
frontend/
├── app/                        # App Router
│   ├── layout.tsx             # Root layout
│   ├── page.tsx               # Landing page
│   ├── (auth)/
│   │   ├── login/
│   │   └── callback/          # Telegram callback
│   ├── (dashboard)/
│   │   ├── layout.tsx         # Dashboard layout
│   │   ├── dashboard/         # Main dashboard
│   │   ├── upload/            # Upload page
│   │   └── history/           # History page
│   └── api/                   # Route handlers
│       └── auth/
│
├── components/
│   ├── ui/                    # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── ...
│   ├── dashboard/
│   │   ├── metrics-grid.tsx
│   │   ├── metric-card.tsx
│   │   └── revenue-chart.tsx
│   ├── upload/
│   │   ├── file-dropzone.tsx
│   │   └── file-preview.tsx
│   └── layout/
│       ├── header.tsx
│       └── sidebar.tsx
│
├── lib/
│   ├── api/                   # API клиент
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── metrics.ts
│   │   └── uploads.ts
│   ├── hooks/
│   │   ├── use-metrics.ts
│   │   ├── use-upload.ts
│   │   └── use-auth.ts
│   ├── utils/
│   │   ├── cn.ts
│   │   ├── formatters.ts
│   │   └── validators.ts
│   └── constants/
│       └── metrics-config.ts
│
├── types/
│   ├── api.ts
│   ├── financial.ts
│   └── user.ts
│
├── public/
│   ├── images/
│   └── fonts/
│
├── __tests__/
├── .env.local
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

### 3.2 Технологический стек Frontend

| Компонент | Технология | Версия | Назначение |
|-----------|-----------|---------|------------|
| **Framework** | Next.js | 14.1+ | React framework |
| **Language** | TypeScript | 5.3+ | Type safety |
| **Styling** | Tailwind CSS | 3.4+ | Utility-first CSS |
| **UI Components** | shadcn/ui | latest | Component library |
| **Charts** | Recharts | 2.10+ | Data visualization |
| **State** | Zustand | 4.5+ | State management |
| **Forms** | React Hook Form | 7.50+ | Form handling |
| **Validation** | Zod | 3.22+ | Schema validation |
| **HTTP** | Axios | 1.6+ | HTTP client |
| **Testing** | Vitest | 1.2+ | Unit testing |
|  | Testing Library | 14+ | Component testing |

### 3.3 State Management

**Zustand store:**

```typescript
// lib/store/auth-store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  telegram_username: string;
  email?: string;
  subscription_tier: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      setUser: (user) => set({ user, isAuthenticated: true }),
      setToken: (token) => set({ token }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
```

---

## 4. Security Architecture

### 4.1 Аутентификация

**Telegram OAuth Flow:**

```
User → Click "Login" → Telegram Widget → Telegram Auth
         ↓
Backend receives data from Telegram
         ↓
Validate hash with bot token
         ↓
Create/Update user in DB
         ↓
Generate JWT token (30 days)
         ↓
Return token to frontend
         ↓
Frontend stores in secure cookie
```

**JWT Structure:**

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "telegram_id": 123456789,
    "exp": 1701388800,
    "iat": 1698796800
  }
}
```

### 4.2 Авторизация

**Middleware проверка:**

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    token: str = Depends(security)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user(user_id)
    if user is None:
        raise credentials_exception
    
    return user
```

### 4.3 Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/uploads")
@limiter.limit("10/minute")  # Максимум 10 загрузок в минуту
async def upload_file(...):
    pass
```

---

## 5. Infrastructure Architecture

### 5.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Cloudflare CDN                     │
│                  (Static Assets)                     │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                 Vercel (Frontend)                    │
│              Next.js 14 App Router                   │
│                                                       │
│  Edge Functions → ISR → API Routes                  │
└─────────────────────────────────────────────────────┘
                         ↓ HTTPS
┌─────────────────────────────────────────────────────┐
│                Railway (Backend)                     │
│                  FastAPI + Gunicorn                  │
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Web      │    │ Worker   │    │ Redis    │      │
│  │ Server   │───>│ (Celery) │───>│ Cache    │      │
│  └──────────┘    └──────────┘    └──────────┘      │
└─────────────────────────────────────────────────────┘
                         ↓ SQL
┌─────────────────────────────────────────────────────┐
│           Railway PostgreSQL Database                │
│                                                       │
│  Primary → Replica (Auto-backup daily)              │
└─────────────────────────────────────────────────────┘
```

### 5.2 CI/CD Pipeline

**GitHub Actions workflow:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Type check
        run: |
          cd backend
          mypy app/
      - name: Lint
        run: |
          cd backend
          black --check .
          flake8 app/

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm run test
      - name: Type check
        run: |
          cd frontend
          npm run type-check
      - name: Lint
        run: |
          cd frontend
          npm run lint

  deploy-backend:
    needs: [test-backend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Railway
        run: |
          # Railway CLI deployment
          railway up

  deploy-frontend:
    needs: [test-frontend]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        run: |
          # Vercel CLI deployment
          vercel --prod
```

---

## 6. Monitoring & Observability

### 6.1 Logging

**Structured logging с structlog:**

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "file_uploaded",
    user_id=user.id,
    file_size=file.size,
    file_type=file.content_type,
    processing_time_ms=elapsed_ms
)
```

### 6.2 Metrics

**Key metrics to track:**

- Request latency (p50, p95, p99)
- Error rate
- Upload success rate
- Calculation time
- Active users
- API calls per minute

---

**Утверждено:** Technical Lead (Dima)  
**Дата утверждения:** 2024-11-15
