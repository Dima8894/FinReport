# 🎉 FinReportAI - Готовый Репозиторий

**Дата создания:** 2024-11-15  
**Версия:** 1.0.0 (MVP Ready)

---

## 📦 Что внутри

Полностью готовая структура проекта со всеми спецификациями, защитой от ошибок и настройками для безопасной AI-кодинга в Cursor.

### Структура репозитория:

```
finreportai-new/
├── README.md                    # Общее описание проекта
├── CONTRIBUTING.md              # Руководство для разработчиков
├── Makefile                     # Удобные команды
├── docker-compose.yml           # Docker setup для локальной разработки
├── .gitignore                   # Git ignore rules
│
├── .cursor/
│   └── cursorrules              # ⭐ КРИТИЧНО: Правила для AI-агента
│
├── docs/
│   ├── specs/
│   │   ├── requirements.md      # ⭐ Полная спецификация требований
│   │   └── architecture.md      # ⭐ Архитектура системы
│   └── adr/
│       └── 001-technology-stack.md  # Архитектурные решения
│
├── plan/
│   └── roadmap.md               # ⭐ Подробный 6-месячный roadmap
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/                 # API endpoints (будут созданы)
│   │   ├── core/                # Config, security
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Бизнес-логика
│   │   ├── repositories/        # Data access
│   │   └── utils/               # Утилиты
│   ├── tests/                   # Pytest тесты
│   ├── requirements.txt         # Python dependencies
│   ├── requirements-dev.txt     # Dev dependencies
│   └── .env.example             # Пример .env файла
│
├── frontend/
│   ├── app/                     # Next.js 14 App Router
│   ├── components/              # React components
│   ├── lib/                     # Utilities, hooks, API client
│   ├── types/                   # TypeScript types
│   ├── package.json             # Node dependencies
│   └── .env.example             # Пример .env файла
│
└── .github/
    └── workflows/
        └── ci-cd.yml            # ⭐ CI/CD pipeline (auto-testing, deploy)
```

---

## 🚀 Быстрый старт

### Вариант 1: Docker (рекомендуется для начала)

```bash
# 1. Распаковать архив
tar -xzf finreportai-new.tar.gz
cd finreportai-new

# 2. Создать .env файлы
make env

# 3. ВАЖНО: Открыть backend/.env и заполнить:
#    - TELEGRAM_BOT_TOKEN (получить от @BotFather)
#    - SECRET_KEY (сгенерировать: openssl rand -hex 32)

# 4. Запустить все сервисы
make docker-up

# 5. Применить миграции БД
docker-compose exec backend alembic upgrade head

# Готово!
# Frontend:  http://localhost:3000
# Backend:   http://localhost:8000
# API Docs:  http://localhost:8000/api/docs
```

### Вариант 2: Локально (для активной разработки)

```bash
# 1. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Создать .env и заполнить
cp .env.example .env
# Заполнить TELEGRAM_BOT_TOKEN и SECRET_KEY

# 2. Frontend setup
cd ../frontend
npm install

# Создать .env.local
cp .env.example .env.local

# 3. Запустить (в разных терминалах)
# Terminal 1:
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2:
cd frontend
npm run dev
```

---

## 🎯 Что делать дальше

### День 1: Setup & Знакомство

1. **Прочитать ключевые документы:**
   - ✅ `README.md` - обзор проекта
   - ✅ `docs/specs/requirements.md` - ЧТО мы строим
   - ✅ `docs/specs/architecture.md` - КАК мы строим
   - ✅ `.cursor/cursorrules` - Правила для AI
   - ✅ `plan/roadmap.md` - План на 6 месяцев

2. **Поднять проект локально:**
   ```bash
   make docker-up
   ```

3. **Проверить что все работает:**
   - Backend health: http://localhost:8000/api/health
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/api/docs

### Day 2-7: Week 1-2 Tasks (Project Setup)

Согласно roadmap, первые 2 недели:

**Backend:**
- [ ] Создать базовые модели (User, Company, FinancialData)
- [ ] Настроить Alembic миграции
- [ ] Реализовать JWT authentication middleware
- [ ] Telegram OAuth интеграция
- [ ] Базовые API endpoints

**Frontend:**
- [ ] Базовый layout (header, sidebar)
- [ ] Auth flow (login, callback pages)
- [ ] API client setup

**Важно:** Перед КАЖДОЙ задачей:
1. Читай `docs/specs/requirements.md` для конкретной фичи
2. Смотри примеры в `.cursor/cursorrules`
3. Используй Cursor AI - он знает все правила

### Следующие недели

Следуй `plan/roadmap.md`:
- Week 3-4: Authentication & Profile
- Week 5-6: File Upload & Parsing
- Week 7-8: Metrics Calculation
- Week 9-10: Dashboard & Visualization
- Week 11-12: History & Polish

---

## 🛡️ Защита от ошибок

### Обязательные проверки перед коммитом:

```bash
# Backend
cd backend
pytest                    # Тесты
black app/               # Форматирование
mypy app/                # Type checking
flake8 app/              # Linting

# Frontend
cd frontend
npm run test             # Тесты
npm run type-check       # TypeScript
npm run lint             # ESLint
```

**Или через Makefile:**
```bash
make test        # Все тесты
make lint        # Все линтеры
make format      # Форматирование
```

### CI/CD автоматически проверит:

- ✅ Test coverage >80%
- ✅ Type checking проходит
- ✅ No linting errors
- ✅ Security scan
- ✅ Build successful

### Cursor AI будет помогать:

Файл `.cursor/cursorrules` содержит:
- Обязательные type hints
- Правила валидации данных
- Примеры правильного кода
- Что ЗАПРЕЩЕНО делать
- Чек-листы перед PR

---

## 📚 Важные документы

### Для разработки:
1. **[requirements.md](docs/specs/requirements.md)** - Все требования к системе
2. **[architecture.md](docs/specs/architecture.md)** - Архитектура и tech stack
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Как работать с репозиторием
4. **[roadmap.md](plan/roadmap.md)** - Что делать и когда

### Для Cursor AI:
1. **[.cursor/cursorrules](.cursor/cursorrules)** - Главные правила
2. **[ADRs](docs/adr/)** - Архитектурные решения

---

## 🔑 Критичные моменты

### 1. Secrets Management

**НИКОГДА не коммитить:**
- ❌ `.env` файлы
- ❌ API keys
- ❌ Database passwords
- ❌ TELEGRAM_BOT_TOKEN

**Всегда использовать:**
- ✅ `.env.example` (без реальных значений)
- ✅ Environment variables
- ✅ Secrets в GitHub Actions (Settings → Secrets)

### 2. Database Migrations

```bash
# Создание новой миграции
cd backend
alembic revision --autogenerate -m "Add users table"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

**НИКОГДА не редактируй существующие миграции после merge в main!**

### 3. Testing

Минимальное покрытие: **80%**

```bash
# Backend
pytest --cov=app --cov-report=term-missing

# Frontend
npm run test:coverage
```

### 4. Git Workflow

```
main        ← production (только через PR)
  ↑
develop     ← integration branch
  ↑
feature/*   ← ваши фичи
fix/*       ← багфиксы
```

**Всегда:**
- ✅ Создавать ветку от `develop`
- ✅ PR в `develop` (не в `main`)
- ✅ Проходить code review
- ✅ Проверять CI/CD

---

## 🎓 Для junior разработчиков

### Если не знаешь что делать:

1. **Посмотри roadmap:**
   ```
   plan/roadmap.md → найди текущую неделю → выбери задачу
   ```

2. **Прочитай спецификацию задачи:**
   ```
   docs/specs/requirements.md → найди FR для фичи
   ```

3. **Посмотри примеры:**
   ```
   .cursor/cursorrules → есть примеры кода
   ```

4. **Спроси Cursor AI:**
   ```
   "Как реализовать FR-1.1 (Telegram auth) согласно requirements.md?"
   ```

5. **Если все еще не понятно:**
   - Спроси в Telegram чате команды
   - Посмотри ADR (docs/adr/)
   - Проверь документацию (FastAPI, Next.js)

### Частые вопросы:

**Q: Как создать новый API endpoint?**
A: Смотри `.cursor/cursorrules` → раздел "Backend разработка"

**Q: Как добавить новую страницу?**
A: `frontend/app/` → создай папку с `page.tsx`

**Q: Как написать тест?**
A: Смотри примеры в `tests/` или `__tests__/`

**Q: Как задеплоить?**
A: Push в `main` → CI/CD сделает автоматически

---

## 🚨 Troubleshooting

### Backend не запускается

```bash
# Проверить БД
docker-compose ps postgres

# Проверить .env
cat backend/.env

# Пересоздать БД
make db-reset
```

### Frontend ошибки компиляции

```bash
# Удалить и переустановить
cd frontend
rm -rf node_modules .next
npm install
```

### Тесты падают

```bash
# Backend
cd backend
pytest --lf  # re-run только failed тесты
pytest -vv   # verbose output

# Frontend
npm run test -- --reporter=verbose
```

---

## 📞 Контакты

- **Product Owner:** Dima (@dima_telegram)
- **Tech Questions:** Telegram чат команды
- **Bugs/Issues:** GitHub Issues

---

## ✅ Чек-лист перед началом работы

- [ ] Распаковал архив
- [ ] Прочитал README.md
- [ ] Прочитал docs/specs/requirements.md
- [ ] Прочитал .cursor/cursorrules
- [ ] Создал .env файлы
- [ ] Заполнил TELEGRAM_BOT_TOKEN
- [ ] Поднял Docker (`make docker-up`)
- [ ] Backend работает (http://localhost:8000)
- [ ] Frontend работает (http://localhost:3000)
- [ ] Прочитал CONTRIBUTING.md
- [ ] Знаю что делать дальше (plan/roadmap.md)

---

## 🎉 Готово!

Теперь у тебя есть:

✅ Полная структура проекта  
✅ Все спецификации и документация  
✅ Защита от ошибок через Cursor rules  
✅ CI/CD pipeline  
✅ Подробный roadmap на 6 месяцев  
✅ Примеры и best practices  
✅ Docker setup для быстрого старта  

**Начинай с Week 1 задач из roadmap.md!**

**Удачи! 🚀**

---

P.S. Не забывай:
- Читать спецификации ПЕРЕД кодингом
- Писать тесты
- Следовать Cursor rules
- Делать маленькие коммиты
- Просить code review

**Если что-то непонятно - пиши в Telegram!**
