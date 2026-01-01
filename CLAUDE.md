# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Telegram bot project with a FastAPI backend API. The bot implements an auto-funnel system for user engagement and includes features for quiz handling, PDF distribution, and consultation management.

**Stack:**
- Python 3.12
- aiogram 3.x (Telegram bot framework)
- FastAPI (REST API)
- SQLAlchemy 2.x (async ORM)
- PostgreSQL 16
- Redis
- Alembic (migrations)
- APScheduler (scheduled tasks)
- Docker Compose

## Architecture

### Two Main Services

1. **Bot Service** (`backend/bot/`): Telegram bot using aiogram
2. **API Service** (`backend/api/`): FastAPI REST API for user operations

Both services share:
- Database models (`backend/infrastructure/database/models/`)
- Database repositories (`backend/infrastructure/database/repo/`)
- Settings (`backend/settings/`)
- Alembic migrations (`backend/infrastructure/migrations/`)

### Key Components

**Handler System (Bot):**
- Handlers organized by type: `user/`, `admin/`, `channel/`, `errors/`
- All routers imported and registered in `handlers/__init__.py` via `routers_list`
- Uses FSM (Finite State Machine) for conversation flows

**Middleware Architecture (Bot):**
- `ConfigMiddleware`: Injects settings and scheduler
- `DatabaseMiddleware`: Injects session pool and Redis
- `CustomI18nMiddleware`: Internationalization support
- Different middleware stacks for message vs channel handlers (see `register_global_middlewares` in `backend/bot/main.py:32`)

**Auto-Funnel System:**
- Scheduled job runs hourly via APScheduler (configured in `backend/bot/main.py:134`)
- Sends timed messages on Days 2, 5, and 7 after PDF download
- Logic in `backend/bot/services/auto_funnel.py`
- Tracks user state via `autoresponder_day` field in User model

**User Tracking:**
- Comprehensive user fields in `backend/infrastructure/database/models/users.py`
- Tracks: source, PDF downloads, channel subscription, consultation requests/status
- Auto-funnel progression tracked via `autoresponder_day` (0-7)

### Settings System

Nested settings using Pydantic with `env_nested_delimiter="__"`:
- `AppSettings` is the root (in `backend/settings/app_settings.py`)
- Contains: `BotSettings`, `DatabaseSettings`, `RedisSettings`, `LoggingSettings`, `MiscellaneousSettings`
- Environment variables use double underscore (e.g., `POSTGRES__DB_USER`)
- Default env file: `.env.prod` (configured in `AppSettings`)

## Development Commands

### Running Locally

**Start services (test environment):**
```bash
docker compose -f docker/test.yml --env-file docker/.env.test up --build -d
```

**Stop services:**
```bash
docker compose -f docker/test.yml --env-file docker/.env.test down
```

**View logs (via Dozzle):**
- http://localhost:8080

**API access:**
- http://localhost:8000
- API docs: http://localhost:8000/api/openapi

### Database Migrations

**Create new migration:**
```bash
docker exec bot alembic revision --autogenerate -m "migration_name"
sudo chmod +777 backend/infrastructure/migrations/versions/*
```

**Apply migrations:**
```bash
docker exec bot alembic upgrade head
```

**Downgrade migration:**
```bash
docker exec bot alembic downgrade -1
```

**Note:** Migrations must be run inside the bot container. Alembic is configured in `backend/alembic.ini` with env.py at `backend/infrastructure/migrations/env.py`.

### Environment Files

- `docker/.env.test` - Local testing
- `docker/.env.dev` - Development server
- `docker/.env.prod` - Production server

## Project Structure Notes

**Backend Organization:**
- `backend/bot/` - Bot code (handlers, keyboards, middlewares, services, utils)
- `backend/api/` - FastAPI application
- `backend/infrastructure/` - Shared infrastructure (database, migrations, API services)
- `backend/settings/` - Configuration classes
- `backend/scripts/` - Helper scripts (alembic, postgres)

**Working Directory:**
- Bot runs from `/app/bot/` in container
- Relative paths for i18n locales: `os.path.join(os.getcwd(), "bot", "locales")`

## Important Patterns

**Database Access:**
- Repository pattern: inherit from `BaseRepo` in `backend/infrastructure/database/repo/base.py`
- Sessions injected via middleware in bot handlers
- FastAPI uses dependency injection: `get_db()` from `backend/infrastructure/database/setup.py:37`

**Handler Registration:**
- Import router in `backend/bot/handlers/__init__.py`
- Add to `routers_list`
- Router will be auto-included in main.py

**Scheduled Tasks:**
- Register jobs in `backend/bot/main.py` before `scheduler.start()`
- Use async functions with sessionmaker passed as arg

**Settings Access:**
- Bot: `get_app_settings()` singleton
- API: global `settings` import from `settings/__init__.py`

## Deployment

**Development branch:** `develop` - auto-deploys to dev server via GitHub Actions
**Production:** Manual workflow dispatch or push to main

Deploy commands run:
```bash
docker compose --env-file docker/.env.dev -f ./docker/dev.yml down
git pull
docker compose --env-file docker/.env.dev -f ./docker/dev.yml up -d --build
```
