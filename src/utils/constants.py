"""Константы приложения ресторанного сервиса заказов."""

from enum import Enum


# ===============================
# СООБЩЕНИЯ ОБ ОШИБКАХ
# ===============================

# Блюда
DISH_NOT_FOUND_MSG = "Блюдо не найдено"
DISH_ALREADY_EXISTS_MSG = "Блюдо с таким именем уже существует"
DISH_INVALID_PRICE_MSG = "Цена блюда должна быть больше нуля"

# Заказы
ORDER_NOT_FOUND_MSG = "Заказ не найден"
ORDER_CANNOT_BE_CANCELLED_MSG = "Отменить заказ можно только в статусе 'в обработке'"
ORDER_INVALID_STATUS_TRANSITION_MSG = "Недопустимый переход статуса заказа"
ORDER_EMPTY_DISHES_MSG = "Заказ должен содержать хотя бы одно блюдо"

# Общие
INVALID_ID_MSG = "Неверный ID"
VALIDATION_ERROR_MSG = "Ошибка валидации данных"
INTERNAL_SERVER_ERROR_MSG = "Внутренняя ошибка сервера"


# ===============================
# СТАТУСЫ ЗАКАЗОВ
# ===============================

class OrderStatus(str, Enum):
    """Статусы заказа с описанием переходов."""
    
    PROCESSING = "в обработке"     # Начальный статус
    PREPARING = "готовится"        # После подтверждения
    READY = "готов"               # Готов к выдаче
    DELIVERING = "доставляется"    # В процессе доставки
    COMPLETED = "завершен"         # Финальный статус
    CANCELLED = "отменен"          # Заказ отменен

    @classmethod
    def get_valid_transitions(cls) -> dict[str, list[str]]:
        """Возвращает допустимые переходы между статусами."""
        return {
            cls.PROCESSING: [cls.PREPARING, cls.CANCELLED],
            cls.PREPARING: [cls.READY, cls.CANCELLED],
            cls.READY: [cls.DELIVERING, cls.COMPLETED],
            cls.DELIVERING: [cls.COMPLETED],
            cls.COMPLETED: [],  # Финальный статус
            cls.CANCELLED: []   # Финальный статус
        }
    
    @classmethod
    def can_transition(cls, from_status: str, to_status: str) -> bool:
        """Проверяет, возможен ли переход между статусами."""
        transitions = cls.get_valid_transitions()
        return to_status in transitions.get(from_status, [])
    
    @classmethod
    def can_be_cancelled(cls, status: str) -> bool:
        """Проверяет, можно ли отменить заказ в данном статусе."""
        return status in [cls.PROCESSING, cls.PREPARING]


# ===============================
# КАТЕГОРИИ БЛЮД
# ===============================

class DishCategory(str, Enum):
    """Категории блюд в ресторане."""
    
    APPETIZERS = "закуски"
    SOUPS = "супы"
    SALADS = "салаты"
    MAIN_COURSES = "основные блюда"
    DESSERTS = "десерты"
    BEVERAGES = "напитки"
    ALCOHOL = "алкоголь"


# ===============================
# ОГРАНИЧЕНИЯ И ЛИМИТЫ
# ===============================

# Блюда
MIN_DISH_PRICE = 0.01           # Минимальная цена блюда
MAX_DISH_PRICE = 99999.99       # Максимальная цена блюда
MAX_DISH_NAME_LENGTH = 100      # Максимальная длина названия блюда
MAX_DISH_DESCRIPTION_LENGTH = 500  # Максимальная длина описания

# Заказы
MIN_ORDER_DISHES = 1            # Минимальное количество блюд в заказе
MAX_ORDER_DISHES = 50           # Максимальное количество блюд в заказе
MAX_CUSTOMER_NAME_LENGTH = 100  # Максимальная длина имени клиента

# Пагинация
DEFAULT_PAGE_SIZE = 20          # Размер страницы по умолчанию
MAX_PAGE_SIZE = 100            # Максимальный размер страницы


# ===============================
# HTTP КОДЫ ОТВЕТОВ
# ===============================

class HTTPStatus:
    """HTTP статус коды для API."""
    
    # 2xx Success
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    
    # 4xx Client Errors  
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    
    # 5xx Server Errors
    INTERNAL_SERVER_ERROR = 500


# ===============================
# СООБЩЕНИЯ ДЛЯ API
# ===============================

# Успешные операции
DISH_CREATED_MSG = "Блюдо успешно создано"
DISH_UPDATED_MSG = "Блюдо успешно обновлено"
DISH_DELETED_MSG = "Блюдо успешно удалено"

ORDER_CREATED_MSG = "Заказ успешно создан"
ORDER_UPDATED_MSG = "Заказ успешно обновлен"
ORDER_CANCELLED_MSG = "Заказ успешно отменен"

# Информационные
NO_DISHES_FOUND_MSG = "Блюда не найдены"
NO_ORDERS_FOUND_MSG = "Заказы не найдены"


# ===============================
# НАСТРОЙКИ БАЗЫ ДАННЫХ
# ===============================

# Строки подключения по умолчанию (можно переопределить в config.py)
DEFAULT_DB_URL = "sqlite:///./restaurant.db"
DEFAULT_TEST_DB_URL = "sqlite:///./test_restaurant.db"

# Настройки пула соединений
DEFAULT_POOL_SIZE = 10
DEFAULT_MAX_OVERFLOW = 20
DEFAULT_POOL_TIMEOUT = 30 