from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from src.database import Base

class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    orders = relationship("Order", secondary="order_dish", back_populates="dishes")
