from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://restaurant_user:restaurant_password@db:5432/restaurant_db"

    class Config:
        env_file = ".env"

settings = Settings()
