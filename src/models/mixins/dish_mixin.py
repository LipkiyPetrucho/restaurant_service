"""Миксин для связи с блюдами."""
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, declared_attr, relationship

if TYPE_CHECKING:
    from src.models.dish import Dish


class DishRelatedMixin:
    """Миксин для добавления связи многие-ко-многим с блюдами.
    
    Автоматически создает:
    - Промежуточную таблицу для связи многие-ко-многим
    - dishes: relationship к модели Dish (односторонняя связь)
    
    Обратные связи не создаются автоматически. Для получения связанных 
    объектов в модели Dish используйте прямые запросы или методы.
    """

    @declared_attr
    def __dish_association_table(cls):
        """Создает промежуточную таблицу для связи многие-ко-многим."""
        # Получаем имя таблицы класса (например "orders")
        table_name = cls.__tablename__
        # Создаем имя промежуточной таблицы (например "order_dish")  
        association_table_name = f"{table_name[:-1]}_dish"  # убираем 's' в конце
        
        return Table(
            association_table_name,
            cls.metadata,
            Column("id", Integer, primary_key=True),
            Column(f"{table_name[:-1]}_id", Integer, ForeignKey(f"{table_name}.id", ondelete="CASCADE"), nullable=False),
            Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="CASCADE"), nullable=False)
        )

    @declared_attr
    def dishes(cls) -> Mapped[list['Dish']]:
        """Односторонняя связь многие-ко-многим с блюдами."""
        return relationship(
            'Dish',
            secondary=cls.__dish_association_table,
            # Убираем back_populates для односторонней связи
        ) 