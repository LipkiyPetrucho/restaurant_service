from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import text
from src.database import Base
from src.utils.custom_types import integer_pk, str_required, str_optional, float_price

class Dish(Base):
    __tablename__ = "dishes"
    
    # Кастомные настройки отображения - показываем id, name, price
    repr_cols = ('id', 'name', 'price')
    
    id: Mapped[integer_pk]
    name: Mapped[str_required]
    description: Mapped[str_optional]
    price: Mapped[float_price]
    category: Mapped[str_required]
    
    # Обратные связи создаются автоматически через DishRelatedMixin
    # orders, menus, promotions и т.д. будут добавлены динамически

    def get_related_objects(self, model_class):
        """Универсальный метод для получения объектов, связанных с этим блюдом."""
        # Формируем имя промежуточной таблицы
        table_name = model_class.__tablename__
        association_table = f"{table_name[:-1]}_dish"
        
        # Выполняем запрос через промежуточную таблицу
        from sqlalchemy.orm import sessionmaker
        session = sessionmaker.object_session(self)
        if session:
            return session.query(model_class).join(
                text(f"{association_table}"),
                text(f"{model_class.__tablename__}.id = {association_table}.{table_name[:-1]}_id")
            ).filter(
                text(f"{association_table}.dish_id = :dish_id")
            ).params(dish_id=self.id).all()
        return []
    
    def get_orders(self):
        """Получить все заказы, содержащие это блюдо."""
        from src.models.order import Order
        return self.get_related_objects(Order)
    
    # При добавлении новых моделей с DishRelatedMixin можно добавить:
    # def get_menus(self):
    #     from src.models.menu import Menu
    #     return self.get_related_objects(Menu)
    #
    # def get_promotions(self):
    #     from src.models.promotion import Promotion  
    #     return self.get_related_objects(Promotion)
