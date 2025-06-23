"""Модуль для работы с базой данных."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class BaseModel(DeclarativeBase):
    """Базовый класс для всех моделей проекта."""
    
    __abstract__ = True

    repr_cols_num = 3
    repr_cols = ()

    def __repr__(self) -> str:
        """Красивое отображение объекта модели."""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__} {", ".join(cols)}>'


engine = create_async_engine(
    settings.DB_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    future=True
)


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Теперь Base это и есть BaseModel
Base = BaseModel

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии базы данных."""
    async with async_session_maker() as session:
        yield session

# Экспорт для удобного импорта
__all__ = [
    "engine",
    "async_session_maker", 
    "Base",
    "BaseModel",  # Экспортируем оба имени для совместимости
    "get_async_session"
]
