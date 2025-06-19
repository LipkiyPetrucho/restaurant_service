from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models.base import BaseModel
from src.utils.custom_types import integer_pk, str_required, order_status, created_at

order_dish = Table(
    "order_dish",
    BaseModel.metadata,
    mapped_column("id", primary_key=True),
    mapped_column("order_id", ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
    mapped_column("dish_id", ForeignKey("dishes.id", ondelete="CASCADE"), nullable=False)
)

class Order(BaseModel):
    __tablename__ = "orders"
    
    # Кастомные настройки отображения - показываем id, customer_name, status
    repr_cols = ('id', 'customer_name', 'status')
    
    id: Mapped[integer_pk]
    customer_name: Mapped[str_required]
    order_time: Mapped[created_at]  # Автоматически устанавливается при создании
    status: Mapped[order_status]    # По умолчанию "в обработке"
    
    # Связи
    dishes: Mapped[list["Dish"]] = relationship("Dish", secondary=order_dish, back_populates="orders")
