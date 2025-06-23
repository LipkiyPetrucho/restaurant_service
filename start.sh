#!/bin/bash

# Запуск Restaurant Order Service

echo "Starting Restaurant Order Service..."

# Проверяем наличие .env файла
if [ ! -f .env ]; then
    echo "Warning: .env file not found, using default values"
fi

# Запускаем миграции базы данных
echo "Running database migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting FastAPI application..."
python -m src 