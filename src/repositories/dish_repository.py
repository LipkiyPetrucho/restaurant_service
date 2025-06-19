from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.dish import Dish
from src.utils.repository import BaseRepository

class DishRepository(BaseRepository):
    model = Dish

    async def get_all(self) -> list[Dish]:
        """Получение всех блюд."""
        return await self.get_by_filter_all()

    async def get_by_ids(self, ids: list[int]) -> list[Dish]:
        """Получение блюд по списку ID."""
        if not ids:
            return []
        result = await self.session.execute(select(Dish).where(Dish.id.in_(ids)))
        return result.scalars().all()

    async def create_from_schema(self, dish_data) -> Dish:
        """Создает новый объект Dish в базе из схемы DishCreate."""
        return await self.add_one_and_get_obj(**dish_data.model_dump())

    async def delete_by_id(self, dish_id: int) -> bool:
        """Удаляет блюдо по ID. Возвращает True, если удалено, или False, если не найдено."""
        dish = await self.get_by_filter_one_or_none(id=dish_id)
        if not dish:
            return False
        await self.delete_by_ids(dish_id)
        return True
