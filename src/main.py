import os

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api import router
from src.metadata import DESCRIPTION, TAG_METADATA, TITLE, VERSION


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv('.env'))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
        )
    else:
        fastapi_app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None,
        )

    fastapi_app.include_router(router, prefix='/api')
    return fastapi_app


app = create_fast_api_app()

@app.get("/", tags=["Health"])
async def root():
    """Проверка работоспособности API."""
    return {"message": "Restaurant Order Service API is running!", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check():
    """Проверка состояния сервиса."""
    return {"status": "healthy", "service": "restaurant-order-service"}
