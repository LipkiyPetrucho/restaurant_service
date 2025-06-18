from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.dish import Dish

class DishRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Dish]:
        result = await self.session.execute(select(Dish))
        return result.scalars().all()

    async def get_by_ids(self, ids: list[int]) -> list[Dish]:
        if not ids:
            return []
        result = await self.session.execute(select(Dish).where(Dish.id.in_(ids)))
        return result.scalars().all()

    async def create(self, dish_data) -> Dish:
        """Создает новый объект Dish в базе из схемы DishCreate."""
        new_dish = Dish(**dish_data.dict())
        self.session.add(new_dish)
        await self.session.commit()
        await self.session.refresh(new_dish)
        return new_dish

    async def delete(self, dish_id: int) -> bool:
        """Удаляет блюдо по ID. Возвращает True, если удалено, или False, если не найдено."""
        dish = await self.session.get(Dish, dish_id)
        if not dish:
            return False
        await self.session.delete(dish)
        await self.session.commit()
        return True
