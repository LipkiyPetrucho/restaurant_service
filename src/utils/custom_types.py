"""Переиспользуемые типы данных для моделей SQLAlchemy."""
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Integer, String, Float, text
from sqlalchemy.orm import mapped_column
from src.utils.constants import OrderStatus

# Тип для асинхронных функций
AsyncFunc = Callable[..., Awaitable[Any]]

# Переиспользуемые типы для primary key
integer_pk = Annotated[int, mapped_column(Integer, primary_key=True, index=True)]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]

# SQL выражения для временных меток
dt_now_utc_sql = text("TIMEZONE('utc', now())")

# Поля аудита времени
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[datetime, mapped_column(
    DateTime,
    server_default=dt_now_utc_sql,
    onupdate=dt_now_utc_sql,
)]

# Часто используемые типы полей
str_required = Annotated[str, mapped_column(String, nullable=False)]
str_optional = Annotated[str | None, mapped_column(String, nullable=True)]
float_price = Annotated[float, mapped_column(Float, nullable=False)]

# Типы для статусов (можно расширить enum'ами)
order_status = Annotated[str, mapped_column(String, nullable=False, default=OrderStatus.PROCESSING)] 