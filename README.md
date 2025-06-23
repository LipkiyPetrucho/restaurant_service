# 🍽️ API-сервис заказов еды в ресторане

REST API для управления заказами еды в ресторане. Сервис позволяет создавать, просматривать и отменять заказы, а также управлять меню и доступными блюдами.

## 📋 Функциональность

### Модели данных:
- **Dish** (Блюдо): id, name, description, price, category
- **Order** (Заказ): id, customer_name, dishes (Many-to-Many), order_time, status

### API эндпоинты:
- `GET /api/v1/dishes/` — список всех блюд
- `POST /api/v1/dishes/` — добавить новое блюдо
- `DELETE /api/v1/dishes/{id}` — удалить блюдо
- `GET /api/v1/orders/` — список всех заказов
- `POST /api/v1/orders/` — создать новый заказ
- `DELETE /api/v1/orders/{id}` — отменить заказ
- `PATCH /api/v1/orders/{id}/status` — изменить статус заказа

## 🚀 Быстрый запуск

### Требования
- Docker
- Docker Compose
- Python 3.11+ (для локальной разработки)
- Poetry (для управления зависимостями)

### Запуск приложения

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd restaurant_order_service
```

2. Запустите сервисы:
```bash
cd deploy
docker-compose up --build
```

3. Приложение будет доступно по адресу: http://localhost:8000

4. Документация API:
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

### Альтернативный запуск (локальная разработка)

Если хотите запустить без Docker:

1. Установите зависимости:
```bash
poetry install
```

2. Настройте базу данных PostgreSQL и создайте `.env` файл

3. Выполните миграции:
```bash
poetry run alembic upgrade head
```

4. Запустите приложение:
```bash
poetry run python -m src
```

### Работа с миграциями

Если потребуется выполнить миграции вручную:

```bash
# Войти в контейнер приложения
docker exec -it restaurant_app bash

# Выполнить миграции
alembic upgrade head

# Создать новую миграцию (при изменении моделей)
alembic revision --autogenerate -m "описание изменений"
```

## 🏗️ Архитектура проекта

```
src/
├── api/v1/
│   ├── routers/          # API роутеры
│   └── services/         # Бизнес-логика
├── models/               # SQLAlchemy модели
├── schemas/              # Pydantic схемы
├── repositories/         # Слой доступа к данным
├── config.py            # Конфигурация
├── database.py          # Настройки БД
└── main.py              # Точка входа
```

## 🛠️ Технологии

- **FastAPI** — веб-фреймворк
- **Poetry** — управление зависимостями
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Alembic** — миграции БД
- **Docker** — контейнеризация
- **Pydantic** — валидация данных
- **Uvicorn** — ASGI сервер

## 🔧 Разработка

### Переменные окружения

Создайте `.env` файл со следующими переменными:

```env
# Для локальной разработки
DB_URL=postgresql+asyncpg://restaurant_user:restaurant_password@localhost:5432/restaurant_db
MODE=DEV

# Для отключения документации в продакшене
# DISABLE_DOCS=true
```

> **Примечание**: В Docker Compose переменные уже настроены автоматически.

### Структура статусов заказов

1. "в обработке" (processing)
2. "готовится" (cooking)
3. "доставляется" (delivering)
4. "завершен" (completed)
5. "отменен" (cancelled)

Отменить заказ можно только в статусе "в обработке".

## 🚨 Устранение неполадок

### Проблема: "Port 5432 is already allocated"
```bash
# Остановите локальный PostgreSQL или измените порт в docker-compose.yml
sudo service postgresql stop
# или используйте другой порт (например, 5433:5432)
```

### Проблема: "404 Not Found" на /docs
- Убедитесь, что `MODE=DEV` в переменных окружения
- Проверьте, что контейнер перезапущен после изменений

### Проблема: "Connection refused"
- Проверьте, что контейнеры запущены: `docker-compose ps`
- Убедитесь, что приложение слушает `0.0.0.0:8000`, а не `127.0.0.1:8000`

### Просмотр логов
```bash
cd deploy
docker-compose logs web    # Логи приложения
docker-compose logs db     # Логи базы данных
```

---

<details>
<summary><b>Связаться со мной</b></summary>
<p align="left">
  <a href="mailto:pafos.light@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-%23EA4335.svg?style=plastic&logo=gmail&logoColor=white" alt="Gmail"/>
  </a>
  <a href="https://t.me/petr_lip">
    <img src="https://img.shields.io/badge/Telegram-0088CC?style=plastic&logo=telegram&logoColor=white" alt="Telegram"/>
  </a>
</p>
</details>