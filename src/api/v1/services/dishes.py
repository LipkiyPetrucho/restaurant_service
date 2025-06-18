from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.dish_repository import DishRepository
from src.schemas.dish import DishCreate

async def list_dishes(session: AsyncSession):
    return await DishRepository(session).get_all()

async def create_dish(data: DishCreate, session: AsyncSession):
    return await DishRepository(session).create(data)

async def delete_dish(dish_id: int, session: AsyncSession):
    success = await DishRepository(session).delete(dish_id)
    if not success:
        # Бросаем HTTPException, которая будет обработана FastAPI и возвращена клиенту
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Блюдо не найдено")
