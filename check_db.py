#!/usr/bin/env python3
"""
Скрипт для проверки подключения к базе данных
"""

import os
import sys
import psycopg2
from src.config import settings

def main():
    """Проверка подключения к базе данных."""
    print("🔍 Проверка подключения к базе данных...")
    
    # Парсим URL базы данных
    db_url = settings.DB_URL
    url_parts = db_url.replace("postgresql+asyncpg://", "postgresql://")
    
    try:
        # Пытаемся подключиться к базе данных
        conn = psycopg2.connect(url_parts)
        cursor = conn.cursor()
        
        # Выполняем простой запрос
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print(f"✅ Подключение к базе данных успешно!")
        print(f"📊 Версия PostgreSQL: {db_version[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print(f"🔗 DB_URL: {settings.DB_URL}")
        sys.exit(1)

if __name__ == "__main__":
    main() 