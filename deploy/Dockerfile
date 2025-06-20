FROM python:3.13-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя приложения
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Копируем и делаем исполняемым скрипт запуска
COPY start.sh /start.sh
COPY check_db.py /app/check_db.py
RUN chmod +x /start.sh

# Изменяем владельца файлов
RUN chown -R app:app /app

# Переключаемся на пользователя приложения
USER app

EXPOSE 8000

# Используем скрипт запуска
CMD ["/start.sh"]
