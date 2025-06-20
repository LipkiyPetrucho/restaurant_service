"""Продвинутая конфигурация базы данных с оптимизациями производительности."""
from collections.abc import AsyncGenerator
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.models.base import BaseModel

# Создаем движок с продвинутыми настройками производительности
async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Управляем логированием через переменные окружения
    future=True,  # Используем SQLAlchemy 2.0 API
    pool_size=settings.DB_POOL_SIZE,  # Настраиваемый размер пула соединений
    max_overflow=settings.DB_MAX_OVERFLOW,  # Настраиваемое количество дополнительных соединений
    connect_args={
        # Уникальные имена для prepared statements для избежания конфликтов
        'prepared_statement_name_func': lambda: f'__asyncpg_{uuid4()}__',
    },
)

# Фабрика сессий с оптимальными настройками
async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,  # Отключаем автоматический flush для лучшего контроля
    autocommit=False,  # Явное управление транзакциями
    expire_on_commit=False,  # Объекты остаются доступными после commit
)

# Используем новый BaseModel вместо declarative_base()
Base = BaseModel


async def get_async_connection() -> AsyncGenerator[AsyncConnection, None]:
    """Получение асинхронного соединения с базой данных.
    
    Используется для выполнения DDL операций, миграций и других 
    операций, которые требуют прямого доступа к соединению.
    """
    async with async_engine.begin() as conn:
        yield conn


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии для работы с ORM.
    
    Основная функция для dependency injection в FastAPI роутерах.
    """
    async with async_session_maker() as session:
        yield session


# Алиас для обратной совместимости
get_db = get_async_session

# Экспорт для удобного импорта
__all__ = [
    "async_engine",
    "async_session_maker", 
    "Base",
    "get_async_connection",
    "get_async_session",
    "get_db"
]
