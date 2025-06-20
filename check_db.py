#!/usr/bin/env python3
"""
Скрипт для проверки подключения к базе данных
"""
import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://restaurant_user:restaurant_password@db:5432/restaurant_db")

async def check_database():
    try:
        # Парсим URL подключения
        url_parts = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        print(f"Подключение к: {url_parts}")
        
        # Создаем подключение
        conn = await asyncpg.connect(url_parts)
        
        # Выполняем простой запрос
        result = await conn.fetchval('SELECT version()')
        print(f"✅ Подключение успешно!")
        print(f"Версия PostgreSQL: {result}")
        
        # Проверяем существование таблиц
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        print(f"Найдено таблиц: {len(tables)}")
        for table in tables:
            print(f"  - {table['table_name']}")
            
        await conn.close()
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = asyncio.run(check_database())
    exit(0 if success else 1) 