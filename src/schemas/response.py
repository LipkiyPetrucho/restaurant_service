from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Базовая схема ответа API."""
    success: bool = True
    message: str = "Operation completed successfully" 