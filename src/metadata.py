TAG_METADATA = [
    {
        'name': 'Dishes | v1',
        'description': 'Операции с блюдами v1.',
    },
    {
        'name': 'Orders | v1',
        'description': 'Операции с заказами v1.',
    },
    {
        'name': 'Health',
        'description': 'Проверка работоспособности сервиса.',
    },
]

TITLE = 'Restaurant Order Service'
DESCRIPTION = (
    'API сервис для управления заказами еды в ресторане.\n\n'
    'Реализован на FastAPI с использованием Clean Architecture.\n\n'
    'Поддерживает создание и управление блюдами, заказами и статусами заказов.'
)
VERSION = '1.0.0'

ERRORS_MAP = {
    'postgres': 'PostgreSQL connection failed',
    'redis': 'Redis connection failed',
} 