from sqlalchemy.orm import relationship, Mapped
from src.database import Base
from src.models.mixins.dish_mixin import DishRelatedMixin
from src.utils.custom_types import integer_pk, str_required, order_status, created_at


class Order(Base, DishRelatedMixin):
    __tablename__ = "orders"
    
    # Кастомные настройки отображения - показываем id, customer_name, status
    repr_cols = ('id', 'customer_name', 'status')
    
    id: Mapped[integer_pk]
    customer_name: Mapped[str_required]
    order_time: Mapped[created_at]
    status: Mapped[order_status]
    
    # Связь dishes создается автоматически через DishRelatedMixin