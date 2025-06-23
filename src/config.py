import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))


class Settings:
    MODE: str = os.environ.get('MODE', 'DEV')

    DB_HOST: str = os.environ.get('DB_HOST', 'localhost')
    DB_PORT: int = int(os.environ.get('DB_PORT', '5432'))
    DB_USER: str = os.environ.get('DB_USER', 'restaurant_user')
    DB_PASS: str = os.environ.get('DB_PASS', 'restaurant_password')
    DB_NAME: str = os.environ.get('DB_NAME', 'restaurant_db')

    # Используем SQLite для разработки, если PostgreSQL недоступен
    DB_URL: str = os.environ.get('DB_URL', f'sqlite+aiosqlite:///./restaurant.db')
    
    # Fallback к PostgreSQL если явно указан
    if DB_HOST and DB_USER and not os.environ.get('DB_URL'):
        DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # Настройки производительности базы данных
    DB_ECHO: bool = bool(os.environ.get('DB_ECHO', False))
    DB_POOL_SIZE: int = int(os.environ.get('DB_POOL_SIZE', '50'))
    DB_MAX_OVERFLOW: int = int(os.environ.get('DB_MAX_OVERFLOW', '100'))
    
    # Общие настройки приложения
    DEBUG: bool = bool(os.environ.get('DEBUG', False))


settings = Settings()
