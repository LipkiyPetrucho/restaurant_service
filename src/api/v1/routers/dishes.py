from fastapi import APIRouter, Depends
from src.api.v1.services.dish_service import DishService
from src.schemas.dish import DishCreate, DishRead
from typing import List

router = APIRouter(prefix="/dishes", tags=["Dishes"])

@router.get("/", response_model=List[DishRead])
async def list_dishes(dish_service: DishService = Depends()):
    """Получить список всех блюд."""
    return await dish_service.get_all_dishes()

@router.post("/", response_model=DishRead, status_code=201)
async def create_dish(dish: DishCreate, dish_service: DishService = Depends()):
    """Добавить новое блюдо."""
    return await dish_service.create_dish(dish)

@router.delete("/{dish_id}", status_code=204)
async def delete_dish(dish_id: int, dish_service: DishService = Depends()):
    """Удалить блюдо."""
    await dish_service.delete_dish(dish_id)
    return {"detail": "Deleted"}
