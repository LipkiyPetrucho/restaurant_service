from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.v1.services import orders as order_service
from src.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate
from src.database import get_db
from typing import List

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderRead])
async def list_orders(session: AsyncSession = Depends(get_db)):
    """Получить список всех заказов."""
    return await order_service.list_orders(session)

@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(order: OrderCreate, session: AsyncSession = Depends(get_db)):
    """Создать новый заказ (статус по умолчанию 'в обработке')."""
    return await order_service.create_order(order, session)

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, session: AsyncSession = Depends(get_db)):
    """Отменить заказ."""
    await order_service.delete_order(order_id, session)
    return {"detail": "Deleted"}

@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status(order_id: int, status_update: OrderStatusUpdate,
                              session: AsyncSession = Depends(get_db)):
    """Обновить статус заказа."""
    updated = await order_service.update_order_status(order_id, status_update.status, session)
    return updated
