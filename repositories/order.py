import datetime
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
        """Все записи из БД"""
        query = self.db.query(Order)
        return query.limit(q_limit).all()

    def find(self, order_number: int) -> Order:
        """Поиск по номеру заказа"""
        query = self.db.query(Order)
        return query.filter(Order.order_number == order_number)

    def delete(self, order_number: int) -> None:
        """Удаление по номеру заказа"""
        order_object = self.find(order_number)
        exp = order_object.delete()

    def update(self, order_number: int, update_data: dict):
        """Обновление заказа по его номеру"""
        query = self.find(order_number)
        query.update(update_data)

    def create(self, order: OrderModel, commit=False) -> Order:
        """Создание заказа"""
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
        """Создание заказов из словаря с заказами (pydantic model)"""
        db_data = self.all()

        if not db_data:
            for order in order_dict.values():
                db_order = self.create(order)
            self.db.commit()
        else:
            result = self.compare_data(db_data, order_dict)

    def compare_data(
        self, db_data: List[Order], sheet_data: Dict[int, OrderModel]
    ) -> bool:
        """Сопоставление данных из таблицы с данными из БД
        1. Если запись не изменилась в таблице и есть в БД - удаляем из табличного списка
        2. Если нет, вносим изменения в заказ из бд, потом удаляем
        3. Если номера заказа нет в бд, но есть в таблице - добавляем в бд
        4. Если номера заказа нет в таблице, но есть в бд - удаляем из бд"""

        for record in db_data:
            if record.order_number in sheet_data.keys():
                order_model = parse_obj_as(OrderModel, record)
                sheet_order_model = sheet_data[order_model.order_number]

                order_model.notified = False

                if order_model != sheet_order_model:
                    update_data = sheet_order_model.dict(exclude_unset=True)
                    self.update(record.order_number, update_data)

                    del sheet_data[record.order_number]
                    continue

                del sheet_data[record.order_number]

            else:
                self.delete(record.order_number)

        for v in sheet_data.values():
            self.create(v)

        self.db.commit()

        return True

    def get_outdated_orders(self) -> Query:
        """Получение просроченых поставок"""
        query = self.db.query(Order)
        today = datetime.date.today()
        orders = query.filter(Order.notified == False).filter(
            Order.expired_date < today
        )

        return orders

    def set_notified(self, orders: Query):
        """Установка маркера, что уведомление о просроченной поставке отправлено"""
        orders.update({"notified": True}, synchronize_session=False)

        self.db.commit()
