from typing import Dict, List

from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from database.get_db_session import get_db
from models.order import Order
from schemas.order import OrderModel


class OrderRepository:
    """Хранилище (слой управления) таблицей с заказами"""

    def __init__(self, db: Session = get_db()):
        self.db = db

    def all(self, q_limit: int = 1000) -> List[Order]:
        query = self.db.query(Order)
        return query.limit(q_limit).all()

    def find(self, order_number: int) -> Order:
        query = self.db.query(Order)
        return query.filter(Order.order_number == order_number).first()

    def delete(self, order_number: int) -> None:
        order_object = self.find(order_number)
        exp = order_object.delete()
        exp.execute()

    def update(self, record: Order, update_data: dict):
        for key, value in update_data.items():
            setattr(record, key, value)

    def create(self, order: OrderModel, commit=False) -> Order:

        db_order = Order(
            table_row=order.table_row,
            order_number=order.order_number,
            usd_price=order.usd_price,
            rub_price=order.rub_price,
            expired_date=order.expired_date,
        )

        self.db.add(db_order)

        if commit:
            self.db.commit()
            self.db.refresh(db_order)

        return db_order

    def create_from_dict(self, order_dict: Dict[int, OrderModel]):
        db_data = self.all()

        if not db_data:
            for order in order_dict.values():
                db_order = self.create(order)
            self.db.commit()
        else:
            result = self.compare_data(db_data, order_dict)

    def compare_data(self, db_data: List[Order], sheet_data: Dict[int, OrderModel]):

        data_to_update = []
        for record in db_data:
            if record.order_number in sheet_data.keys():
                order_model = parse_obj_as(OrderModel, record)
                sheet_order_model = sheet_data[order_model.order_number]

                if order_model != sheet_order_model:
                    update_data = sheet_order_model.dict(exclude_unset=True)
                    data_to_update.append([record, update_data])
                    del sheet_data[record.order_number]

                del sheet_data[record.order_number]

            else:
                self.delete(record.order_number)

        for data in data_to_update:
            self.update(data[0], data[1])

        for v in sheet_data.values():
            self.create(v)

        self.db.commit()

        return True

    def get_order_dates(self) -> List[Order]:
        query = self.db.query(Order)
        return query.with_entities(Order.order_number, Order.expired_date).all()
