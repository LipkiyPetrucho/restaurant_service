"""Сервис для работы с блюдами."""
from fastapi import Depends
from src.schemas.dish import DishCreate
from src.utils.service import BaseService, UnitOfWork, transaction_mode
from src.models.dish import Dish


class DishService(BaseService):
    """Сервис для управления блюдами."""
    
    _repo = "dishes"

    @transaction_mode
    async def get_all_dishes(self) -> list[Dish]:
        """Получение всех блюд."""
        return await self.uow.dishes.get_all()

    @transaction_mode
    async def create_dish(self, dish_data: DishCreate) -> Dish:
        """Создание нового блюда."""
        return await self.uow.dishes.create_from_schema(dish_data)

    @transaction_mode
    async def delete_dish(self, dish_id: int) -> bool:
        """Удаление блюда по ID."""
        success = await self.uow.dishes.delete_by_id(dish_id)
        if not success:
            self.check_existence(None, "Блюдо не найдено")
        return success

    @transaction_mode
    async def get_dishes_by_ids(self, dish_ids: list[int]) -> list[Dish]:
        """Получение блюд по списку ID."""
        return await self.uow.dishes.get_by_ids(dish_ids) 