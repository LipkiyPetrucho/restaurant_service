from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.services import dishes as dish_service
from src.schemas.dish import DishCreate, DishRead
from src.database import get_db
from typing import List

router = APIRouter(prefix="/dishes", tags=["Dishes"])

@router.get("/", response_model=List[DishRead])
async def list_dishes(session: AsyncSession = Depends(get_db)):
    """Получить список всех блюд."""
    return await dish_service.list_dishes(session)

@router.post("/", response_model=DishRead, status_code=201)
async def create_dish(dish: DishCreate, session: AsyncSession = Depends(get_db)):
    """Добавить новое блюдо."""
    return await dish_service.create_dish(dish, session)

@router.delete("/{dish_id}", status_code=204)
async def delete_dish(dish_id: int, session: AsyncSession = Depends(get_db)):
    """Удалить блюдо."""
    await dish_service.delete_dish(dish_id, session)
    return {"detail": "Deleted"}  # при 204 тело ответа обычно не используется
