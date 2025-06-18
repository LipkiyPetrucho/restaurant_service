from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.repositories.order_repository import OrderRepository
from src.repositories.dish_repository import DishRepository
from src.schemas.order import OrderCreate

# Карта последовательности статусов заказа: текущий -> следующий допустимый
_next_status = {
    "в обработке": "готовится",
    "готовится": "доставляется",
    "доставляется": "завершен"
}

async def list_orders(session: AsyncSession):
    return await OrderRepository(session).get_all()

async def create_order(order_data: OrderCreate, session: AsyncSession):
    # Проверяем существование всех блюд по переданным dish_ids
    dish_repo = DishRepository(session)
    dishes = await dish_repo.get_by_ids(order_data.dish_ids)
    if len(dishes) != len(order_data.dish_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некоторые из указанных блюд не существуют")
    # Создаем заказ через репозиторий (статус автоматически будет "в обработке")
    order_repo = OrderRepository(session)
    new_order = await order_repo.create(order_data.customer_name, dishes)
    return new_order

async def delete_order(order_id: int, session: AsyncSession):
    # Отменяем заказ (удаляем), только если он еще в статусе "в обработке"
    order_repo = OrderRepository(session)
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    if order.status != "в обработке":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отменить заказ можно только в статусе 'в обработке'")
    # Удаляем заказ
    await order_repo.delete(order_id)

async def update_order_status(order_id: int, new_status: str, session: AsyncSession):
    order_repo = OrderRepository(session)
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    # Проверяем допустимость перехода статуса
    current_status = order.status
    if current_status not in _next_status:
        # Текущий статус "завершен" или неизвестный – изменить нельзя
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Статус заказа не может быть изменен")
    expected_next = _next_status[current_status]
    if new_status != expected_next:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Неверная последовательность статуса. Ожидалось '{expected_next}'")
    # Обновляем статус через репозиторий
    updated_order = await order_repo.update_status(order, new_status)
    return updated_order
