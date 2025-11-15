# FinReportAI Makefile
# Удобные команды для разработки

.PHONY: help setup dev test lint clean docker-up docker-down migrate

# Показать список команд
help:
	@echo "FinReportAI Development Commands"
	@echo "================================="
	@echo ""
	@echo "Setup:"
	@echo "  make setup         - Первоначальная настройка проекта"
	@echo "  make env           - Создать .env файлы из примеров"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Запустить backend + frontend локально"
	@echo "  make dev-backend   - Запустить только backend"
	@echo "  make dev-frontend  - Запустить только frontend"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up     - Запустить все сервисы в Docker"
	@echo "  make docker-down   - Остановить все сервисы"
	@echo "  make docker-logs   - Показать логи"
	@echo "  make docker-clean  - Очистить volumes и containers"
	@echo ""
	@echo "Database:"
	@echo "  make migrate       - Применить миграции БД"
	@echo "  make migrate-create MSG='description' - Создать новую миграцию"
	@echo "  make db-reset      - Сбросить БД (осторожно!)"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Запустить все тесты"
	@echo "  make test-backend  - Запустить тесты backend"
	@echo "  make test-frontend - Запустить тесты frontend"
	@echo "  make coverage      - Тесты с coverage"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          - Запустить линтеры"
	@echo "  make format        - Форматировать код"
	@echo "  make type-check    - Проверить типы"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Очистить временные файлы"

# ============================================
# SETUP
# ============================================
setup: env
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install -r requirements-dev.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Setup complete! Run 'make dev' to start development"

env:
	@echo "📝 Creating .env files..."
	@test -f backend/.env || cp backend/.env.example backend/.env
	@test -f frontend/.env.local || cp frontend/.env.example frontend/.env.local
	@echo "⚠️  Don't forget to fill in TELEGRAM_BOT_TOKEN in backend/.env"

# ============================================
# DEVELOPMENT
# ============================================
dev:
	@echo "🚀 Starting development servers..."
	@make -j2 dev-backend dev-frontend

dev-backend:
	@echo "🐍 Starting backend..."
	cd backend && \
		. venv/bin/activate && \
		uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	@echo "⚛️  Starting frontend..."
	cd frontend && npm run dev

# ============================================
# DOCKER
# ============================================
docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 5
	@echo "✅ Services started!"
	@echo "   Backend:  http://localhost:8000"
	@echo "   Frontend: http://localhost:3000"
	@echo "   API Docs: http://localhost:8000/api/docs"

docker-down:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	@echo "🧹 Cleaning Docker volumes and containers..."
	docker-compose down -v
	docker system prune -f

# ============================================
# DATABASE
# ============================================
migrate:
	@echo "📊 Applying database migrations..."
	cd backend && \
		. venv/bin/activate && \
		alembic upgrade head

migrate-create:
	@echo "📝 Creating new migration..."
	cd backend && \
		. venv/bin/activate && \
		alembic revision --autogenerate -m "$(MSG)"

db-reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		docker-compose up -d postgres; \
		sleep 3; \
		make migrate; \
		echo "✅ Database reset complete"; \
	fi

# ============================================
# TESTING
# ============================================
test: test-backend test-frontend

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && \
		. venv/bin/activate && \
		pytest -v

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm run test

coverage:
	@echo "📊 Running tests with coverage..."
	@echo "Backend coverage:"
	cd backend && \
		. venv/bin/activate && \
		pytest --cov=app --cov-report=term-missing
	@echo ""
	@echo "Frontend coverage:"
	cd frontend && npm run test:coverage

# ============================================
# CODE QUALITY
# ============================================
lint: lint-backend lint-frontend

lint-backend:
	@echo "🔍 Linting backend..."
	cd backend && \
		. venv/bin/activate && \
		flake8 app/ && \
		mypy app/

lint-frontend:
	@echo "🔍 Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "✨ Formatting code..."
	cd backend && \
		. venv/bin/activate && \
		black app/ tests/
	cd frontend && npx prettier --write .

type-check:
	@echo "🔎 Type checking..."
	cd backend && \
		. venv/bin/activate && \
		mypy app/
	cd frontend && npm run type-check

# ============================================
# CLEANUP
# ============================================
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "node_modules" -prune -o -type d -name ".next" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================
# PRODUCTION (use with caution)
# ============================================
deploy-backend:
	@echo "🚀 Deploying backend to Railway..."
	cd backend && railway up

deploy-frontend:
	@echo "🚀 Deploying frontend to Vercel..."
	cd frontend && vercel --prod
