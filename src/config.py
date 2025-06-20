from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Основные настройки базы данных
    DATABASE_URL: str = "postgresql+asyncpg://restaurant_user:restaurant_password@db:5432/restaurant_db"
    
    # Настройки производительности базы данных
    DB_ECHO: bool = False  # Логирование SQL запросов (включить для отладки)
    DB_POOL_SIZE: int = 50  # Размер пула соединений
    DB_MAX_OVERFLOW: int = 100  # Максимальное количество дополнительных соединений
    
    # Общие настройки приложения
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
