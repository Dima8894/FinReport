# 🚀 FinReportAI - Быстрый старт

**Готово к запуску!** Вся базовая структура Week 1-2 создана.

---

## ⚡ Запуск за 3 шага

### Шаг 1: Создайте .env файлы

```bash
# Backend
cd /Users/dmitrijtitov/Documents/FinReport/backend
cp .env.example .env
```

**Откройте `backend/.env` и заполните:**

```bash
# Генерируем SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32)
echo "SECRET_KEY=$SECRET_KEY"

# Получить TELEGRAM_BOT_TOKEN:
# 1. Откройте Telegram
# 2. Найдите @BotFather
# 3. Отправьте /newbot
# 4. Следуйте инструкциям
# 5. Скопируйте token
```

**Frontend:**
```bash
cd ../frontend
cp .env.example .env.local
```

---

### Шаг 2: Настройте БД

```bash
cd /Users/dmitrijtitov/Documents/FinReport

# Запустите PostgreSQL через Docker
docker-compose up -d postgres

# Установите зависимости Python
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Создайте миграцию
alembic revision --autogenerate -m "Initial database schema"

# Примените миграцию
alembic upgrade head
```

---

### Шаг 3: Запустите проект

**Вариант A: Docker (все сразу)**
```bash
cd /Users/dmitrijtitov/Documents/FinReport
docker-compose up -d
```

**Вариант B: Локально (для разработки)**

Terminal 1 (Backend):
```bash
cd /Users/dmitrijtitov/Documents/FinReport/backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd /Users/dmitrijtitov/Documents/FinReport/frontend
npm install
npm run dev
```

---

## ✅ Проверка

Откройте браузер:

1. **Frontend:** http://localhost:3000
   - Должна загрузиться landing page
   - Кнопка "Войти через Telegram"

2. **Backend API:** http://localhost:8000
   - Должен вернуть JSON с версией

3. **API Docs:** http://localhost:8000/api/docs
   - Swagger UI с документацией API

---

## 🎯 Что работает

✅ **Backend:**
- FastAPI сервер
- PostgreSQL подключение
- 4 модели БД (User, Company, FinancialData, CalculatedMetrics)
- Telegram OAuth endpoints
- Companies CRUD endpoints
- JWT authentication

✅ **Frontend:**
- Next.js 14 App Router
- Landing page
- Telegram Login Widget
- Auth Context
- Dashboard page (заглушка)
- API client

✅ **Infrastructure:**
- Docker Compose
- Alembic миграции
- Environment variables

---

## 🐛 Troubleshooting

### Проблема: "ModuleNotFoundError: No module named 'app'"
**Решение:**
```bash
cd backend
pip install -r requirements.txt
```

### Проблема: "Connection to localhost:5432 refused"
**Решение:**
```bash
# Проверьте что PostgreSQL запущен
docker-compose ps postgres

# Если не запущен:
docker-compose up -d postgres
```

### Проблема: "Alembic command not found"
**Решение:**
```bash
cd backend
source venv/bin/activate
pip install alembic
```

### Проблема: "Frontend не загружается"
**Решение:**
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

---

## 📝 Следующие шаги

После успешного запуска:

1. ✅ **Протестируйте Telegram login**
   - Откройте http://localhost:3000
   - Нажмите "Войти через Telegram"
   - Пройдите авторизацию
   - Должны попасть на /dashboard

2. ✅ **Проверьте API в Swagger**
   - http://localhost:8000/api/docs
   - Попробуйте endpoints

3. ⏭️ **Переходите к Week 3-4**
   - Создание профиля компании
   - Загрузка Excel файлов
   - Расчет метрик

---

## 📞 Нужна помощь?

Смотрите:
- `PROGRESS.md` - Детальный отчет
- `docs/specs/requirements.md` - Требования
- `plan/roadmap.md` - План разработки

---

**Готово! Можно начинать разработку! 🚀**

