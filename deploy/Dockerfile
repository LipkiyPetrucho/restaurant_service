FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry==2.1.2

# Создаем пользователя приложения
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Копируем файлы Poetry для установки зависимостей
COPY pyproject.toml poetry.lock* ./

# Настраиваем Poetry и устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --only=main --no-interaction --no-ansi --no-root

# Копируем исходный код
COPY src/ src/
COPY alembic/ alembic/
COPY alembic.ini .

# Копируем скрипты
COPY start.sh /start.sh
COPY check_db.py .
RUN chmod +x /start.sh

# Изменяем владельца файлов
RUN chown -R app:app /app

# Переключаемся на пользователя приложения
USER app

EXPOSE 8000

# Используем скрипт запуска
CMD ["/start.sh"]
