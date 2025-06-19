from pydantic import BaseModel

class DishBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category: str

class DishCreate(DishBase):
    """Схема для создания нового блюда."""
    pass

class DishRead(DishBase):
    """Схема для вывода информации о блюде."""
    id: int

    class Config:
        from_attributes = True
