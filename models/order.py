from sqlalchemy import Boolean, Column, Date, Float, Integer

from database.database import DB

Model = DB.model


class Order(Model):
    """Модель заказа в базе данных"""

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    table_row = Column(Integer, nullable=False)
    order_number = Column(Integer, index=True, unique=True)
    usd_price = Column(Float, nullable=False)
    rub_price = Column(Float, nullable=False)
    expired_date = Column(Date, nullable=False)
    notified = Column(Boolean, default=False)
