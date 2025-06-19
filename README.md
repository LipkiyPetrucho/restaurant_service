# 🍽️ API-сервис заказов еды в ресторане

REST API для управления заказами еды в ресторане. Сервис позволяет создавать, просматривать и отменять заказы, а также управлять меню и доступными блюдами.

## 📋 Функциональность

### Модели данных:
- **Dish** (Блюдо): id, name, description, price, category
- **Order** (Заказ): id, customer_name, dishes (Many-to-Many), order_time, status

### API эндпоинты:
- `GET /dishes/` — список всех блюд
- `POST /dishes/` — добавить новое блюдо
- `DELETE /dishes/{id}` — удалить блюдо
- `GET /orders/` — список всех заказов
- `POST /orders/` — создать новый заказ
- `DELETE /orders/{id}` — отменить заказ
- `PATCH /orders/{id}/status` — изменить статус заказа

## 🚀 Быстрый запуск

### Требования
- Docker
- Docker Compose

### Запуск приложения

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd restaurant_order_service
```

2. Запустите сервисы:
```bash
docker-compose up --build
```

3. Приложение будет доступно по адресу: http://localhost:8000

4. Документация API (Swagger): http://localhost:8000/docs

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
- **SQLAlchemy** — ORM
- **PostgreSQL** — база данных
- **Alembic** — миграции БД
- **Docker** — контейнеризация
- **Pydantic** — валидация данных

## 🔧 Разработка

### Переменные окружения

Создайте `.env` файл со следующими переменными:

```env
DATABASE_URL=postgresql+asyncpg://restaurant_user:restaurant_password@db:5432/restaurant_db
```

### Структура статусов заказов

1. "в обработке" (processing)
2. "готовится" (cooking)
3. "доставляется" (delivering)
4. "завершен" (completed)
5. "отменен" (cancelled)

Отменить заказ можно только в статусе "в обработке".

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