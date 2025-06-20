"""Утилиты для работы с базой данных."""
from sqlalchemy.ext.asyncio import AsyncEngine
from src.database.database import async_engine, Base


async def create_all_tables(engine: AsyncEngine = async_engine) -> None:
    """Создание всех таблиц в базе данных.
    
    Используется для инициализации базы данных в тестах 
    или при первом запуске приложения.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables(engine: AsyncEngine = async_engine) -> None:
    """Удаление всех таблиц из базы данных.
    
    Используется для очистки базы данных в тестах.
    ВНИМАНИЕ: Все данные будут потеряны!
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def recreate_all_tables(engine: AsyncEngine = async_engine) -> None:
    """Пересоздание всех таблиц (удаление + создание).
    
    Полностью очищает и пересоздает структуру базы данных.
    ВНИМАНИЕ: Все данные будут потеряны!
    """
    await drop_all_tables(engine)
    await create_all_tables(engine)


async def check_database_connection() -> bool:
    """Проверка подключения к базе данных.
    
    Returns:
        bool: True если подключение успешно, False в противном случае
    """
    try:
        async with async_engine.begin() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False 