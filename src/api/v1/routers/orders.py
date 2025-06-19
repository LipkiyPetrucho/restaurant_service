from fastapi import APIRouter, Depends
from src.api.v1.services.order_service import OrderService
from src.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderRead])
async def list_orders(order_service: OrderService = Depends()):
    """Получить список всех заказов."""
    return await order_service.get_all_orders()

@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(order: OrderCreate, order_service: OrderService = Depends()):
    """Создать новый заказ (статус по умолчанию 'в обработке')."""
    return await order_service.create_order(order)

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, order_service: OrderService = Depends()):
    """Отменить заказ."""
    await order_service.delete_order(order_id)
    return {"detail": "Deleted"}

@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: int, status_update: OrderStatusUpdate,
                              order_service: OrderService = Depends()):
    """Обновить статус заказа."""
    return await order_service.update_order_status(order_id, status_update.status)
