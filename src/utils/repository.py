"""Модуль содержит абстрактный репозиторий."""
from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    """Абстрактный класс репозитория, реализующий CRUD операции на уровне репозитория."""

    @abstractmethod
    async def add_one(self, **kwargs: Any) -> None:
        """Добавление одной записи."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        """Добавление одной записи и получение ID этой записи."""
        raise NotImplementedError

    @abstractmethod
    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        """Добавление одной записи и получение этой записи."""
        raise NotImplementedError

    @abstractmethod
    async def bulk_add(self, values: Sequence[dict[str, Any]]) -> None:
        """Массовое добавление записей."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_one_or_none(self, **kwargs: Any) -> Any:
        """Получение одной записи по заданному фильтру, если она существует."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_filter_all(self, **kwargs: Any) -> Sequence[Any]:
        """Получение всех записей по указанному фильтру."""
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_id(self, obj_id: int | str | UUID, **kwargs: Any) -> Any:
        """Обновление одной записи по её ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_filter(self, **kwargs: Any) -> None:
        """Массовое удаление записей по фильтру."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_ids(self, *args: int | str | UUID) -> None:
        """Массовое удаление записей по переданным ID."""
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self) -> None:
        """Массовое удаление всех записей."""
        raise NotImplementedError


class BaseRepository(AbstractRepository):
    """Базовый репозиторий для выполнения стандартных CRUD операций."""

    model = None  # должна быть моделью SQLAlchemy

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_one(self, **kwargs: Any) -> None:
        """Добавление одной записи."""
        obj = self.model(**kwargs)
        self.session.add(obj)

    async def add_one_and_get_id(self, **kwargs: Any) -> int | str | UUID:
        """Добавление одной записи и получение ID этой записи."""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj.id

    async def add_one_and_get_obj(self, **kwargs: Any) -> Any:
        """Добавление одной записи и получение этой записи."""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def bulk_add(self, values: Sequence[dict[str, Any]]) -> None:
        """Массовое добавление записей."""
        objs = [self.model(**value) for value in values]
        self.session.add_all(objs)

    async def get_by_filter_one_or_none(self, **kwargs: Any) -> Any:
        """Получение одной записи по заданному фильтру, если она существует."""
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_filter_all(self, **kwargs: Any) -> Sequence[Any]:
        """Получение всех записей по указанному фильтру."""
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_one_by_id(self, obj_id: int | str | UUID, **kwargs: Any) -> Any:
        """Обновление одной записи по её ID."""
        query = update(self.model).where(self.model.id == obj_id).values(**kwargs).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete_by_filter(self, **kwargs: Any) -> None:
        """Массовое удаление записей по фильтру."""
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)

    async def delete_by_ids(self, *args: int | str | UUID) -> None:
        """Массовое удаление записей по переданным ID."""
        query = delete(self.model).where(self.model.id.in_(args))
        await self.session.execute(query)

    async def delete_all(self) -> None:
        """Массовое удаление всех записей."""
        query = delete(self.model)
        await self.session.execute(query) 