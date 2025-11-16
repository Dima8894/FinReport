# Руководство по разработке FinReportAI

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- Node.js 20+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (опционально)

### Вариант 1: Docker (рекомендуется)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/your-org/finreportai.git
cd finreportai

# 2. Скопировать .env файлы
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# 3. Заполнить TELEGRAM_BOT_TOKEN в backend/.env

# 4. Запустить все сервисы
docker-compose up -d

# 5. Применить миграции БД
docker-compose exec backend alembic upgrade head

# Готово! 
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Вариант 2: Локально

**Backend:**
```bash
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Скопировать .env
cp .env.example .env
# Заполнить переменные в .env

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend

# Установить зависимости
npm install

# Скопировать .env
cp .env.example .env.local

# Запустить dev server
npm run dev
```

---

## 📝 Workflow разработки

### 1. Создание новой фичи

```bash
# Создать новую ветку от develop
git checkout develop
git pull origin develop
git checkout -b feat/your-feature-name
```

### 2. Разработка

**ВАЖНО:** Всегда читайте файлы перед началом работы:
- `docs/specs/requirements.md` - требования
- `docs/specs/architecture.md` - архитектура
- `docs/adr/*.md` - архитектурные решения
- `.cursor/cursorrules` - правила для AI

**Backend разработка:**

```bash
# 1. Создать модель (app/models/)
# 2. Создать схему Pydantic (app/schemas/)
# 3. Создать сервис (app/services/)
# 4. Создать API endpoint (app/api/v1/)
# 5. Написать тесты (tests/)
# 6. Создать миграцию

# Создание миграции
alembic revision --autogenerate -m "Add feature X"
alembic upgrade head

# Запуск тестов
pytest

# Проверка типов
mypy app/

# Форматирование
black app/
```

**Frontend разработка:**

```bash
# 1. Создать компонент (components/)
# 2. Создать типы (types/)
# 3. Создать хук если нужен (lib/hooks/)
# 4. Создать страницу (app/)
# 5. Написать тесты (__tests__/)

# Запуск тестов
npm run test

# Type checking
npm run type-check

# Линтинг
npm run lint

# Форматирование
npx prettier --write .
```

### 3. Тестирование

**ОБЯЗАТЕЛЬНО:**
- ✅ Test coverage >80%
- ✅ Все тесты проходят
- ✅ No linting errors
- ✅ Type checking проходит

```bash
# Backend
pytest --cov=app --cov-report=term-missing

# Frontend
npm run test:coverage
```

### 4. Коммит

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat(calculator): добавить расчет ROE
fix(auth): исправить ошибку logout
docs(api): обновить OpenAPI спецификацию
test(metrics): добавить тесты для ROS
refactor(services): оптимизировать MetricsCalculator
```

**Формат:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: Новая функциональность
- `fix`: Исправление бага
- `docs`: Документация
- `style`: Форматирование
- `refactor`: Рефакторинг
- `test`: Тесты
- `chore`: Рутинные задачи

### 5. Push и Pull Request

```bash
# Убедиться что все тесты проходят
pytest && npm run test

# Push
git push origin feat/your-feature-name

# Создать PR на GitHub
# Target branch: develop
```

**PR Checklist:**
- [ ] Код покрыт тестами (>80%)
- [ ] Все тесты проходят
- [ ] Линтеры не выдают ошибок
- [ ] Документация обновлена
- [ ] API контракты актуальны
- [ ] Нет хардкода secrets
- [ ] Логирование добавлено
- [ ] Type hints присутствуют

### 6. Code Review

**Для reviewer:**
- Проверить соответствие requirements.md
- Проверить архитектурные решения (ADR)
- Проверить тесты
- Проверить безопасность
- Проверить производительность

**Для автора:**
- Ответить на все комментарии
- Исправить замечания
- Пройти повторное review

### 7. Merge

После approval merge в `develop`:
```bash
# Merge через GitHub UI
# Или через CLI:
gh pr merge --squash
```

---

## 🧪 Тестирование

### Backend (Pytest)

```bash
# Запустить все тесты
pytest

# Запустить конкретный тест
pytest tests/test_calculator.py::test_calculate_ros

# С покрытием
pytest --cov=app --cov-report=html

# Только быстрые тесты
pytest -m "not slow"
```

**Структура тестов:**

```python
# tests/test_services/test_calculator.py

import pytest
from app.services.calculator import MetricsCalculator
from app.schemas.financial import FinancialData

def test_calculate_ros_positive():
    """Тест расчета ROS с положительными значениями"""
    data = FinancialData(
        revenue=1000,
        net_profit=100,
        # ... остальные поля
    )
    calc = MetricsCalculator(data)
    
    result = calc._calculate_ros()
    
    assert result == 10.0

def test_calculate_ros_zero_revenue():
    """Тест расчета ROS при нулевой выручке"""
    data = FinancialData(revenue=0, net_profit=100, ...)
    calc = MetricsCalculator(data)
    
    result = calc._calculate_ros()
    
    assert result == 0.0
```

### Frontend (Vitest + Testing Library)

```bash
# Запустить все тесты
npm run test

# Watch mode
npm run test:watch

# С покрытием
npm run test:coverage
```

**Структура тестов:**

```typescript
// __tests__/components/metrics-card.test.tsx

import { render, screen } from '@testing-library/react';
import { MetricsCard } from '@/components/dashboard/metrics-card';

describe('MetricsCard', () => {
  it('отображает название метрики', () => {
    const metric = {
      name: 'ROS',
      value: 15.5,
      trend: 'up' as const,
      description: 'Рентабельность продаж',
    };

    render(<MetricsCard metric={metric} />);

    expect(screen.getByText('ROS')).toBeInTheDocument();
    expect(screen.getByText('15.5%')).toBeInTheDocument();
  });
});
```

---

## 🔐 Безопасность

### НЕ коммитить:
- ❌ `.env` файлы
- ❌ API keys
- ❌ Secrets
- ❌ Personal data
- ❌ `node_modules/`
- ❌ `__pycache__/`
- ❌ `.venv/`

### Проверка перед коммитом:
```bash
# Поиск секретов
git diff | grep -i "secret\|password\|key\|token"
```

### Если случайно закоммитили секрет:
```bash
# 1. Немедленно ротировать secret
# 2. Удалить из истории Git
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (с осторожностью!)
git push origin --force --all
```

---

## 📚 Дополнительные ресурсы

### Документация
- [Requirements](docs/specs/requirements.md)
- [Architecture](docs/specs/architecture.md)
- [ADRs](docs/adr/)
- [API Docs](http://localhost:8000/api/docs)

### Полезные ссылки
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Cursor Rules](.cursor/cursorrules)

### Контакты команды
- Product Owner: @dima_telegram
- Tech Lead: TBD
- Code Review: Все senior-девелоперы

---

## 🐛 Troubleshooting

### Backend не запускается

```bash
# Проверить БД
docker-compose ps postgres

# Проверить переменные окружения
cat backend/.env

# Пересоздать БД
docker-compose down -v
docker-compose up -d postgres
alembic upgrade head
```

### Frontend не компилируется

```bash
# Удалить node_modules и .next
rm -rf node_modules .next

# Переустановить зависимости
npm install

# Проверить TypeScript errors
npm run type-check
```

### Тесты падают

```bash
# Очистить cache
pytest --cache-clear

# Запустить с verbose
pytest -vv

# Проверить fixtures
pytest --fixtures
```

---

## 💡 Советы для новых разработчиков

1. **Читайте документацию** перед началом работы
2. **Задавайте вопросы** в Telegram чате
3. **Используйте Cursor AI** - он знает все правила проекта
4. **Пишите тесты** перед кодом (TDD)
5. **Делайте маленькие коммиты** - легче ревьювить
6. **Обновляйте документацию** вместе с кодом
7. **Следуйте Cursor Rules** - они защищают от ошибок

---

**Спасибо за вклад в FinReportAI! 🚀**
