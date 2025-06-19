from sqlalchemy.orm import relationship, Mapped
from src.models.base import BaseModel
from src.utils.custom_types import integer_pk, str_required, str_optional, float_price

class Dish(BaseModel):
    __tablename__ = "dishes"
    
    # Кастомные настройки отображения - показываем id, name, price
    repr_cols = ('id', 'name', 'price')
    
    id: Mapped[integer_pk]
    name: Mapped[str_required]
    description: Mapped[str_optional]
    price: Mapped[float_price]
    category: Mapped[str_required]
    
    # Связи
    orders: Mapped[list["Order"]] = relationship("Order", secondary="order_dish", back_populates="dishes")
