from typing import List, Dict

from sqlalchemy.orm import Session

from database.get_db_session import get_db
from models.order import Order
from schemas.order import OrderModel


class OrderRepository:
    """Хранилище (слой управления) таблицей с вопросами"""
    def __init__(self, db: Session = get_db()):
        self.db = db

    def all(self, q_limit: int = 100) -> List[Order]:
        query = self.db.query(Order)
        return query.limit(q_limit).all()

    def find(self, order_number: int) -> Order:
        query = self.db.query(Order)
        return query.filter(Order.order_number == order_number).first()

    def create(self, order: OrderModel) -> Order:

        db_order = Order(
            order_number=order.order_number,
            usd_price=order.usd_price,
            rub_price=order.rub_price,
            expired_date=order.expired_date,
        )

        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)

        return db_order

    def create_from_list(self, order_list: List[OrderModel]):
        ...
