"""Модуль содержит Unit of Work для управления транзакциями."""
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_maker
from src.repositories.dish_repository import DishRepository
from src.repositories.order_repository import OrderRepository


class AbstractUnitOfWork(ABC):
    """Абстрактный класс Unit of Work."""

    @abstractmethod
    async def __aenter__(self):
        """Вход в контекстный менеджер."""
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера."""
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        """Подтверждение транзакции."""
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        """Откат транзакции."""
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        """Синхронизация изменений с базой данных без подтверждения транзакции."""
        raise NotImplementedError

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Проверка, открыт ли Unit of Work."""
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """Unit of Work для управления транзакциями SQLAlchemy."""

    def __init__(self) -> None:
        self.session: AsyncSession | None = None
        self._session_factory = async_session_maker
        self._is_open = False

    async def __aenter__(self):
        """Вход в контекстный менеджер - создание сессии и репозиториев."""
        if self.session is None:
            self.session = self._session_factory()
            self._is_open = True
        
        # Создание репозиториев с текущей сессией
        self.dishes = DishRepository(self.session)
        self.orders = OrderRepository(self.session)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера - закрытие сессии."""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        
        if self.session:
            await self.session.close()
            self.session = None
            self._is_open = False

    async def commit(self):
        """Подтверждение транзакции."""
        if self.session:
            await self.session.commit()

    async def rollback(self):
        """Откат транзакции."""
        if self.session:
            await self.session.rollback()

    async def flush(self):
        """Синхронизация изменений с базой данных без подтверждения транзакции."""
        if self.session:
            await self.session.flush()

    @property
    def is_open(self) -> bool:
        """Проверка, открыт ли Unit of Work."""
        return self._is_open and self.session is not None 