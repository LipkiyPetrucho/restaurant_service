from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.database import Base

order_dish = Table(
    "order_dish",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE")),
    Column("dish_id", Integer, ForeignKey("dishes.id", ondelete="CASCADE"))
)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    order_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)
    dishes = relationship("Dish", secondary=order_dish, back_populates="orders")
