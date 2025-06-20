"""Базовая модель для всех моделей SQLAlchemy."""
from sqlalchemy.orm import DeclarativeBase, Mapped
from src.utils.custom_types import created_at, updated_at


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


class BaseModelWithTimestamps(BaseModel):
    """Базовый класс с полями аудита времени для новых моделей."""
    
    __abstract__ = True
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at] 