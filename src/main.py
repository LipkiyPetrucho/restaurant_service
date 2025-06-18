from fastapi import FastAPI
from src.api.v1.routers import dishes as dishes_router, orders as orders_router

app = FastAPI(title="Restaurant Order Service", version="1.0")

# Подключаем маршруты API v1
app.include_router(dishes_router.router)
app.include_router(orders_router.router)
