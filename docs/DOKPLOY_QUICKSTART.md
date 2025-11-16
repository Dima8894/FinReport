# 🚀 Dokploy - Краткая шпаргалка

## За 5 шагов до деплоя!

### Шаг 1: Получите токены (5 минут)

**Telegram Bot:**
```
1. Откройте @BotFather в Telegram
2. Отправьте: /newbot
3. Назовите бот: FinReportAI
4. Username: FinReportAIBot
5. Скопируйте токен!
```

**SECRET_KEY:**
```bash
openssl rand -hex 32
# Скопируйте результат
```

---

### Шаг 2: Настройте Dokploy (2 минуты)

1. Войдите в Dokploy
2. Откройте ваш проект
3. **Source → GitHub:**
   - Repo: `https://github.com/Dima8894/FinReport.git`
   - Branch: `main`
   - Auto Deploy: ✅

4. **Deploy Type:**
   - Type: `Docker Compose`
   - File: `docker-compose.prod.yml`

---

### Шаг 3: Environment Variables (3 минуты)

Добавьте в Dokploy (раздел Environment Variables):

```bash
# Обязательные:
POSTGRES_USER=finreportai
POSTGRES_PASSWORD=придумайте_сложный_пароль
POSTGRES_DB=finreportai
SECRET_KEY=ваш_сгенерированный_ключ_из_шага_1
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather

# URLs (замените на свои):
BACKEND_URL=https://api.yourdomain.com   # или http://ваш-ip:8000
FRONTEND_URL=https://yourdomain.com      # или http://ваш-ip:3000

# Настройки:
TELEGRAM_BOT_NAME=FinReportAIBot
ENVIRONMENT=production
DEBUG=False
```

---

### Шаг 4: Запустите деплой (5 минут)

Нажмите кнопку **"Deploy"** в Dokploy.

Дождитесь:
```
✓ Building...
✓ Starting...
✓ Running!
```

---

### Шаг 5: Создайте БД (1 минута)

**В Dokploy Console (для backend контейнера):**

```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

**Или через SSH:**
```bash
docker exec -it finreportai_backend_prod bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
exit
```

---

## ✅ Готово! Проверьте:

1. **Frontend:** http://ваш-ip:3000 или https://yourdomain.com
2. **Backend:** http://ваш-ip:8000 или https://api.yourdomain.com
3. **API Docs:** http://ваш-ip:8000/api/docs

Попробуйте войти через Telegram!

---

## 🐛 Не работает?

### Backend не запускается
→ Проверьте Environment Variables  
→ Посмотрите логи в Dokploy

### Frontend показывает ошибку
→ Убедитесь что `BACKEND_URL` правильный  
→ Проверьте что backend работает

### Telegram login не работает
→ Проверьте `TELEGRAM_BOT_TOKEN`  
→ Убедитесь что бот создан в @BotFather

### База данных пустая
→ Выполните миграции (Шаг 5)

---

## 📚 Полная инструкция

См. `DOKPLOY_DEPLOY.md` - там всё очень подробно расписано!

---

**Удачи! 🚀**

