from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderCreate(BaseModel):
    customer_name: str
    dish_ids: List[int]

class DishInOrder(BaseModel):
    """Вложенная схема блюда внутри заказа (упрощенная)."""
    id: int
    name: str
    price: float
    category: str

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    customer_name: str
    status: str
    order_time: datetime
    dishes: List[DishInOrder]

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str
