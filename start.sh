#!/bin/bash
set -e

echo "🚀 Запуск Restaurant Order Service..."

# Проверяем переменные окружения
echo "📋 Проверка переменных окружения:"
echo "DATABASE_URL: ${DATABASE_URL:-'не установлена'}"

# Ожидание готовности базы данных
echo "⏳ Ожидание готовности базы данных..."
timeout=60
while ! pg_isready -h db -p 5432 -U restaurant_user; do
    echo "База данных еще не готова. Ожидание..."
    sleep 2
    timeout=$((timeout - 2))
    if [ $timeout -le 0 ]; then
        echo "❌ Превышено время ожидания базы данных"
        exit 1
    fi
done

echo "✅ База данных готова!"

# Проверяем подключение к базе данных
echo "🔍 Проверка подключения к базе данных..."
python check_db.py

# Выполняем миграции
echo "📊 Выполнение миграций..."
alembic upgrade head

echo "🌟 Запуск FastAPI приложения..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --log-level info 