from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.order import Order
from src.models.dish import Dish

class OrderRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Order]:
        # Загружаем связанные блюда сразу (selectinload) чтобы избежать дополнительных запросов
        result = await self.session.execute(select(Order).options(selectinload(Order.dishes)))
        return result.scalars().all()

    async def get_by_id(self, order_id: int) -> Order | None:
        return await self.session.get(Order, order_id)

    async def create(self, customer_name: str, dishes: list[Dish]) -> Order:
        new_order = Order(customer_name=customer_name, status="в обработке")
        # Привязываем объекты Dish к заказу, если список непустой
        new_order.dishes = dishes
        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def update_status(self, order: Order, new_status: str) -> Order:
        """Обновляет статус существующего заказа (предполагается, что order привязан к сессии)."""
        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.session.get(Order, order_id)
        if not order:
            return False
        await self.session.delete(order)
        await self.session.commit()
        return True
