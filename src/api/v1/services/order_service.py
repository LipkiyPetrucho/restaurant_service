"""Сервис для работы с заказами."""
from fastapi import HTTPException, status, Depends
from src.schemas.order import OrderCreate
from src.utils.service import BaseService, UnitOfWork, transaction_mode
from src.models.order import Order
from src.api.v1.services.dish_service import DishService
from src.utils.constants import (
    ORDER_NOT_FOUND_MSG,
    ORDER_CANNOT_BE_CANCELLED_MSG,
    ORDER_INVALID_STATUS_TRANSITION_MSG,
    OrderStatus,
    ORDER_EMPTY_DISHES_MSG
)


# Карта последовательности статусов заказа: текущий -> следующий допустимый
_next_status = {
    "в обработке": "готовится",
    "готовится": "доставляется",
    "доставляется": "завершен"
}


class OrderService(BaseService):
    """Сервис для управления заказами."""
    
    _repo = "orders"

    def __init__(self, uow: UnitOfWork = Depends(), dish_service: DishService = Depends()) -> None:
        super().__init__(uow)
        self.dish_service = dish_service

    @transaction_mode
    async def get_all_orders(self) -> list[Order]:
        """Получение всех заказов."""
        return await self.uow.orders.get_all()

    @transaction_mode
    async def create_order(self, order_data: OrderCreate) -> Order:
        """Создание нового заказа."""
        # Проверяем существование всех блюд по переданным dish_ids
        dishes = await self.dish_service.get_dishes_by_ids(order_data.dish_ids)
        if len(dishes) != len(order_data.dish_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Некоторые из указанных блюд не существуют"
            )
        
        # Создаем заказ через репозиторий (статус автоматически будет OrderStatus.PROCESSING)
        new_order = await self.uow.orders.create_with_dishes(order_data.customer_name, dishes)
        return new_order

    @transaction_mode
    async def delete_order(self, order_id: int) -> None:
        """Удаление заказа по ID (только в статусе 'в обработке')."""
        order = await self.uow.orders.get_by_id(order_id)
        self.check_existence(order, ORDER_NOT_FOUND_MSG)
        
        if not OrderStatus.can_be_cancelled(order.status):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ORDER_CANNOT_BE_CANCELLED_MSG
            )
        
        # Удаляем заказ
        await self.uow.orders.delete_by_id(order_id)

    @transaction_mode
    async def update_order_status(self, order_id: int, new_status: str) -> Order:
        """Обновление статуса заказа."""
        order = await self.uow.orders.get_by_id(order_id)
        self.check_existence(order, ORDER_NOT_FOUND_MSG)
        
        # Проверяем допустимость перехода статуса
        current_status = order.status
        if not OrderStatus.can_transition(current_status, new_status):
            # Получаем список допустимых статусов для более информативной ошибки
            valid_transitions = OrderStatus.get_valid_transitions().get(current_status, [])
            if valid_transitions:
                detail = f"Из статуса '{current_status}' можно перейти только к: {', '.join(valid_transitions)}"
            else:
                detail = f"Статус '{current_status}' является финальным и не может быть изменен"
                
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        
        # Обновляем статус через репозиторий
        updated_order = await self.uow.orders.update_status(order, new_status)
        return updated_order 