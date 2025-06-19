from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.order import Order
from src.models.dish import Dish
from src.utils.repository import BaseRepository

class OrderRepository(BaseRepository):
    model = Order

    async def get_all(self) -> list[Order]:
        """Получение всех заказов с загрузкой связанных блюд."""
        # Загружаем связанные блюда сразу (selectinload) чтобы избежать дополнительных запросов
        result = await self.session.execute(select(Order).options(selectinload(Order.dishes)))
        return result.scalars().all()

    async def get_by_id(self, order_id: int) -> Order | None:
        """Получение заказа по ID."""
        return await self.get_by_filter_one_or_none(id=order_id)

    async def create_with_dishes(self, customer_name: str, dishes: list[Dish]) -> Order:
        """Создание заказа с привязанными блюдами."""
        order_data = {
            "customer_name": customer_name,
            "status": "в обработке"
        }
        new_order = await self.add_one_and_get_obj(**order_data)
        # Привязываем объекты Dish к заказу, если список непустой
        new_order.dishes = dishes
        await self.session.flush()
        await self.session.refresh(new_order)
        return new_order

    async def update_status(self, order: Order, new_status: str) -> Order:
        """Обновляет статус существующего заказа."""
        return await self.update_one_by_id(order.id, status=new_status)

    async def delete_by_id(self, order_id: int) -> bool:
        """Удаляет заказ по ID. Возвращает True, если удален, или False, если не найден."""
        order = await self.get_by_filter_one_or_none(id=order_id)
        if not order:
            return False
        await self.delete_by_ids(order_id)
        return True
