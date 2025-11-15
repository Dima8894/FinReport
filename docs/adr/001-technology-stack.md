# ADR-001: Выбор технологического стека

**Дата:** 2024-11-15  
**Статус:** Утверждено  
**Авторы:** Dima, Tech Team

## Контекст

FinReportAI требует выбора технологий для MVP с учетом:
- Команда junior-уровня
- Быстрая разработка (4-6 месяцев)
- Финансовые расчеты с высокой точностью
- Обработка Excel/CSV файлов
- Telegram аутентификация
- Масштабируемость

## Решение

### Backend: Python + FastAPI

**Выбрали:**
- Python 3.11+
- FastAPI web framework
- Pandas + NumPy для расчетов
- PostgreSQL database
- SQLAlchemy ORM

**Обоснование:**
1. **Python** идеален для финансовых расчетов:
   - Pandas отлично работает с табличными данными
   - NumPy для быстрых вычислений
   - Богатая экосистема (openpyxl, xlrd для Excel)

2. **FastAPI** преимущества:
   - Автогенерация OpenAPI документации
   - Type hints обязательны → меньше ошибок
   - Async/await из коробки
   - Pydantic валидация
   - Быстрая разработка

3. **Простота для junior-девов:**
   - Python читаемый синтаксис
   - Меньше boilerplate чем Django
   - Хорошая документация FastAPI

### Frontend: Next.js 14 (App Router) + TypeScript

**Выбрали:**
- Next.js 14+ с App Router
- TypeScript strict mode
- Tailwind CSS + shadcn/ui
- Recharts для графиков

**Обоснование:**
1. **Next.js 14 App Router:**
   - Server Components → быстрая загрузка
   - Встроенная оптимизация
   - Легкий деплой на Vercel
   - SEO из коробки для лендинга

2. **TypeScript:**
   - Защита от ошибок на compile-time
   - Autocomplete для junior-девов
   - Refactoring безопасен

3. **Tailwind + shadcn:**
   - Быстрая разработка UI
   - Готовые компоненты
   - Консистентный дизайн

### Database: PostgreSQL

**Выбрали:**
- PostgreSQL 14+
- Railway Managed PostgreSQL

**Обоснование:**
1. **Надежность для финансовых данных**
2. **ACID транзакции**
3. **JSON support** (для метаданных)
4. **Хорошая ORM поддержка**
5. **Бесплатный tier на Railway**

## Альтернативы

### Отклоненные варианты:

**1. Node.js/NestJS Backend**
- ❌ Слабее для работы с Excel
- ❌ Меньше библиотек для финансовой математики
- ✅ Единый язык с frontend (но не критично)

**2. Django Backend**
- ❌ Слишком монолитный для API
- ❌ Много лишнего (admin panel не нужен)
- ❌ Медленнее разработка чем FastAPI

**3. .NET/C# Backend**
- ❌ Сложнее для junior-девов
- ❌ Медленнее разработка
- ✅ Лучше для 1С интеграции (но не критично для MVP)

**4. MySQL Database**
- ❌ Слабее чем PostgreSQL по features
- ❌ Хуже работает с complex queries

## Последствия

### Положительные:
- ✅ Быстрая разработка MVP
- ✅ Хорошая защита от ошибок (type hints everywhere)
- ✅ Отличная экосистема для Excel/финансов
- ✅ Легкий deployment (Railway + Vercel)
- ✅ Низкий порог входа для junior-девов

### Отрицательные:
- ⚠️ Python медленнее чем compiled languages (но для нашего кейса достаточно быстр)
- ⚠️ Next.js 14 App Router относительно новый (меньше примеров)
- ⚠️ Vendor lock-in на Vercel/Railway (но миграция возможна)

### Риски и митигация:
1. **Риск:** Performance issues при большом объеме данных
   - **Митигация:** Pagination, caching (Redis), background jobs (Celery)

2. **Риск:** Junior-девы не знают Python/FastAPI
   - **Митигация:** Документация + примеры + Cursor AI помощь

3. **Риск:** Проблемы с типами в Python
   - **Митигация:** Обязательные type hints + mypy в CI/CD

## Связанные решения

- ADR-002: Выбор хостинга (Railway + Vercel)
- ADR-003: Архитектура аутентификации (Telegram OAuth)
- ADR-004: Стратегия тестирования

## Примечания

Решение можно пересмотреть после MVP если:
- Performance станет критичной проблемой
- Потребуется глубокая интеграция с 1С (тогда .NET)
- Команда значительно вырастет

---

**Статус:** ✅ Утверждено и внедрено
