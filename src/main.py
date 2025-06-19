import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from src.api.v1.routers import dishes as dishes_router, orders as orders_router
from src.database import Base
from src.config import settings

engine = create_async_engine(settings.DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаем таблицы при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Закрываем движок при завершении
    await engine.dispose()

app = FastAPI(
    title="Restaurant Order Service",
    description="API сервис для управления заказами еды в ресторане",
    version="1.0.0",
    lifespan=lifespan
)

# Подключаем маршруты API v1
app.include_router(dishes_router.router, prefix="/api/v1")
app.include_router(orders_router.router, prefix="/api/v1")

@app.get("/", tags=["Health"])
async def root():
    """Проверка работоспособности API."""
    return {"message": "Restaurant Order Service API is running!", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка состояния сервиса."""
    return {"status": "healthy", "service": "restaurant-order-service"}
