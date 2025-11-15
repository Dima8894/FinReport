# FinReportAI Roadmap

**Версия:** 1.0  
**Timeline:** 6 месяцев до публичного запуска  
**Последнее обновление:** 2024-11-15

---

## 📅 Timeline Overview

```
Месяц 1-2: MVP Development
Месяц 3-4: Beta Testing & Improvements  
Месяц 5-6: Public Launch Preparation
```

---

## Phase 1: MVP Development (Месяцы 1-2)

**Цель:** Работающий продукт для первого beta-тестера (Акфикс)

### Week 1-2: Project Setup & Infrastructure

**Backend Setup:**
- [ ] Инициализация Python проекта
- [ ] FastAPI базовая структура
- [ ] PostgreSQL schema + миграции Alembic
- [ ] Базовые модели (User, Company, FinancialData)
- [ ] JWT authentication middleware
- [ ] Telegram OAuth интеграция
- [ ] Docker setup для локальной разработки
- [ ] Railway deployment setup

**Frontend Setup:**
- [ ] Next.js 14 проект с App Router
- [ ] TypeScript конфигурация
- [ ] Tailwind + shadcn/ui setup
- [ ] Базовый layout (header, sidebar)
- [ ] Auth flow (login, callback pages)
- [ ] API client setup (axios + interceptors)
- [ ] Vercel deployment setup

**DevOps:**
- [ ] GitHub Actions CI/CD
- [ ] Automated testing pipeline
- [ ] Linting + formatting (black, prettier)
- [ ] Environment variables setup

**📊 Success Metrics:**
- ✅ Backend поднимается локально
- ✅ Frontend рендерится
- ✅ Telegram login работает
- ✅ CI/CD pipeline green

---

### Week 3-4: Core Features - Authentication & Profile

**Backend:**
- [ ] `POST /api/v1/auth/telegram` - Telegram login
- [ ] `GET /api/v1/auth/me` - Get current user
- [ ] `POST /api/v1/companies` - Create company
- [ ] `GET /api/v1/companies/me` - Get my company
- [ ] `PUT /api/v1/companies/me` - Update company
- [ ] Unit tests (80% coverage)
- [ ] API documentation (OpenAPI)

**Frontend:**
- [ ] Landing page с кнопкой "Войти через Telegram"
- [ ] Dashboard layout (после логина)
- [ ] Company profile form
- [ ] Form validation (Zod + React Hook Form)
- [ ] Error handling (toasts)
- [ ] Loading states

**📊 Success Metrics:**
- ✅ Пользователь может войти через Telegram
- ✅ Пользователь может создать профиль компании
- ✅ Данные сохраняются в БД

---

### Week 5-6: File Upload & Parsing

**Backend:**
- [ ] File upload handler (multipart/form-data)
- [ ] Excel parser (pandas + openpyxl)
- [ ] CSV parser
- [ ] Data validation (Pydantic схемы)
- [ ] Save to `financial_data` table
- [ ] Error handling для неверных форматов
- [ ] Background job для обработки (Celery setup)
- [ ] Unit tests для parser

**Frontend:**
- [ ] Upload page с drag & drop
- [ ] File preview (Excel структура)
- [ ] Upload progress bar
- [ ] Validation feedback
- [ ] Success/error messages

**📊 Success Metrics:**
- ✅ Excel файл успешно загружается
- ✅ Данные парсятся и валидируются
- ✅ Ошибки показываются пользователю
- ✅ CSV также поддерживается

---

### Week 7-8: Metrics Calculation Engine

**Backend:**
- [ ] `MetricsCalculator` service
- [ ] Реализация всех 11 формул:
  - [ ] Выручка и прогноз
  - [ ] Маржинальность
  - [ ] ROS
  - [ ] ROA
  - [ ] ROE
  - [ ] Коэффициенты ликвидности (3 шт)
  - [ ] Финансовая независимость
  - [ ] Оборачиваемость активов
  - [ ] Чистый оборотный капитал
  - [ ] Коэффициент оборотного капитала
- [ ] Save to `calculated_metrics` table
- [ ] `GET /api/v1/metrics/latest` endpoint
- [ ] `GET /api/v1/metrics/{period}` endpoint
- [ ] Comprehensive unit tests (каждая формула)
- [ ] Edge cases testing (деление на 0, отрицательные значения)

**Testing:**
- [ ] Test data generation (fixtures)
- [ ] Golden test cases (эталонные расчеты)
- [ ] Comparison с Excel расчетами

**📊 Success Metrics:**
- ✅ Все 11 метрик рассчитываются корректно
- ✅ Результаты совпадают с ручными расчетами
- ✅ Test coverage 90%+

---

### Week 9-10: Dashboard & Visualization

**Frontend:**
- [ ] Metrics Grid компонент
- [ ] Metric Card компонент (с цветовой индикацией)
- [ ] Revenue Chart (Recharts line chart)
- [ ] Responsive layout (desktop + mobile)
- [ ] Loading skeleton states
- [ ] Empty state (нет данных)
- [ ] Period selector (если есть история)
- [ ] Tooltips с пояснениями метрик

**Design:**
- [ ] Финализация цветовой схемы
- [ ] Icons для каждой метрики
- [ ] Color coding (зеленый/желтый/красный)

**📊 Success Metrics:**
- ✅ Все метрики отображаются на дашборде
- ✅ Графики работают
- ✅ Адаптив на mobile
- ✅ Performance <2s load time

---

### Week 11-12: History & Polish

**Backend:**
- [ ] `GET /api/v1/uploads` - история загрузок
- [ ] `GET /api/v1/metrics/history` - история метрик
- [ ] Pagination support
- [ ] Filtering by period

**Frontend:**
- [ ] History page (таблица загрузок)
- [ ] Детальный view метрик за конкретный период
- [ ] Comparison view (опционально для Phase 2)

**Polish:**
- [ ] Onboarding flow для новых пользователей
- [ ] Help tooltips
- [ ] Error pages (404, 500)
- [ ] Performance optimization
- [ ] Bug fixing

**Documentation:**
- [ ] User manual (как загружать файлы)
- [ ] Excel template с примером
- [ ] FAQ
- [ ] Video tutorial (5 минут)

**📊 Success Metrics:**
- ✅ Пользователь может видеть историю
- ✅ Пользователь понимает как работать с системой
- ✅ Нет критичных багов

---

## ✅ MVP Completion Criteria

- [ ] Telegram authentication работает
- [ ] Пользователь может загрузить Excel/CSV
- [ ] Все 11 метрик рассчитываются правильно
- [ ] Дашборд отображает метрики + графики
- [ ] Mobile responsive
- [ ] Test coverage >80%
- [ ] Performance Lighthouse >90
- [ ] Документация для пользователей
- [ ] Deployed на Railway + Vercel
- [ ] **Акфикс успешно использует систему**

**Target Date:** Конец Месяца 2

---

## Phase 2: Beta Testing & Improvements (Месяцы 3-4)

**Цель:** Получить feedback, исправить баги, оптимизировать

### Month 3: Beta Testing with Akfix

**Week 13-14: Deployment & Onboarding**
- [ ] Production deployment
- [ ] Onboarding сессия с Акфикс
- [ ] Обучение команды Акфикс
- [ ] Сбор первых feedback

**Week 15-16: Iteration 1**
- [ ] Fix bugs из feedback
- [ ] UX improvements
- [ ] Performance optimization
- [ ] Additional помощь/подсказки в UI

**Metrics to track:**
- Time to first successful upload
- Success rate
- User satisfaction (NPS)
- Bugs reported

### Month 4: Feature Improvements

**Week 17-18: Advanced Features**
- [ ] 1С интеграция (инструкция по выгрузке)
- [ ] Comparison view (сравнение периодов)
- [ ] Export дашборда в PDF
- [ ] Email notifications (опционально)

**Week 19-20: Polish & Optimization**
- [ ] Caching (Redis) для частых запросов
- [ ] Database optimization (indexes)
- [ ] Frontend code splitting
- [ ] SEO optimization лендинга
- [ ] А/В тестирование CTA

**📊 Success Metrics:**
- ✅ Churn rate <5%
- ✅ Daily active usage
- ✅ <10 bugs per week
- ✅ Response time p95 <500ms

---

## Phase 3: Launch Preparation (Месяцы 5-6)

**Цель:** Готовность к публичному запуску

### Month 5: Monetization & Marketing

**Week 21-22: Payment Integration**
- [ ] Выбор payment processor (ЮKassa / CloudPayments)
- [ ] Subscription logic
- [ ] Trial period (14 дней)
- [ ] 2 тарифных плана:
  - Базовый: 3000₽/мес
  - Стандарт: 10000₽/мес
- [ ] Billing dashboard
- [ ] Invoices generation

**Week 23-24: Marketing Assets**
- [ ] Landing page optimization
- [ ] Product video (2-3 минуты)
- [ ] Case study с Акфикс
- [ ] Blog posts (3-5 статей)
- [ ] Email drip campaign
- [ ] Social media content

**Sales:**
- [ ] Pricing page
- [ ] Feature comparison table
- [ ] Testimonials
- [ ] FAQ expansion

### Month 6: Launch

**Week 25-26: Final Testing**
- [ ] Load testing (100+ concurrent users)
- [ ] Security audit
- [ ] Penetration testing
- [ ] Legal review (Terms, Privacy Policy)
- [ ] Compliance check (152-ФЗ)

**Week 27-28: Launch!**
- [ ] Soft launch (limited users)
- [ ] Monitoring setup (Sentry, alerts)
- [ ] Customer support process
- [ ] Public launch announcement
- [ ] PR & media outreach

**Post-Launch Week 1-2:**
- [ ] Monitor metrics 24/7
- [ ] Quick bug fixes
- [ ] User support
- [ ] Collect feedback
- [ ] Iterate quickly

**📊 Success Metrics:**
- ✅ 50+ signups в первый месяц
- ✅ 20+ paid subscriptions
- ✅ Uptime >99%
- ✅ Customer satisfaction >4/5

---

## Post-Launch Roadmap (Month 7+)

### Planned Features (Priority Order):

1. **Платежный календарь** (Q1 2025)
   - Планирование денежных потоков
   - Cash flow forecast
   - Alerts о кассовых разрывах

2. **Расширенная аналитика** (Q1 2025)
   - Сравнение с отраслевыми бенчмарками
   - Drill-down по категориям
   - Custom KPIs

3. **Автоматическая интеграция с 1С** (Q2 2025)
   - 1С расширение
   - Автоматическая синхронизация
   - API для 1С

4. **Прогнозирование (ML)** (Q2 2025)
   - Forecast выручки
   - Anomaly detection
   - Scenario planning

5. **Мобильное приложение** (Q3 2025)
   - iOS app
   - Android app
   - Push notifications

6. **Интеграция с банками** (Q3 2025)
   - Автоматическая подгрузка выписок
   - Reconciliation

7. **Multi-company support** (Q4 2025)
   - Консолидированная отчетность
   - Группа компаний

8. **Белый лейбл** (2026)
   - Для консалтинговых компаний
   - Custom branding

---

## Resource Allocation

### Team Size по Phases:

**Phase 1 (Месяцы 1-2):** 2 разработчика
- Dima (Product + Backend)
- Junior Dev (Full-stack)

**Phase 2 (Месяцы 3-4):** 2-3 разработчика
- +1 Junior (если нужно)
- +1 Support person (part-time)

**Phase 3 (Месяцы 5-6):** 3-4 разработчика
- +1 Marketing/Sales person
- +1 Customer Success

### Budget Estimate:

**Phase 1:** ~500k руб (зарплаты + инфраструктура)  
**Phase 2:** ~700k руб  
**Phase 3:** ~900k руб  
**Total:** ~2.1M руб до launch

---

## Risks & Mitigation

| Риск | Вероятность | Impact | Митигация |
|------|-------------|--------|-----------|
| Затягивание разработки | Средняя | Высокий | Agile спринты, еженедельные review |
| Баги в расчетах | Средняя | Критичный | Extensive testing, golden datasets |
| Low user adoption | Средняя | Высокий | Early beta testing, marketing pre-launch |
| Competition | Низкая | Средний | Focus на UX и speed-to-value |
| Technical debt | Высокая | Средний | Code review, refactoring спринты |
| Security breach | Низкая | Критичный | Security audit, penetration testing |

---

## Success Metrics (KPIs)

### Development Metrics:
- **Velocity:** Story points per sprint
- **Quality:** Test coverage >80%
- **Performance:** <2s dashboard load
- **Bugs:** <10 critical bugs at launch

### Business Metrics:
- **Beta:** 1 satisfied customer (Акфикс)
- **Month 1:** 50+ signups
- **Month 3:** 20+ paying customers
- **Month 6:** 100+ paying customers
- **Revenue:** 200k+ руб MRR к концу года

---

**Владелец roadmap:** Dima  
**Review frequency:** Каждые 2 недели  
**Next review:** Week 2 (after project setup)
