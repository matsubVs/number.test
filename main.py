import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from currency_convertor import usd_to_rub
from database.database import DB
from repositories.order import OrderRepository
from schemas.order import OrderModel
from sheets_controller.controller import SheetAccessController as Controller
from tg.sender import send_message

load_dotenv()

DB.model.metadata.create_all(bind=DB.engine)

client = Controller.get_client()
orders_repo = OrderRepository()


def main():
    sheet = Controller.get_sheet(client)
    data = Controller.get_sheet_data(sheet)

    process_data = {}

    for raw_order in data:
        print(raw_order['№'])
        order = {
            "table_row": raw_order["№"],
            "order_number": raw_order["заказ №"],
            "usd_price": raw_order["стоимость,$"],
            "expired_date": raw_order["срок поставки"],
        }
        order["rub_price"] = usd_to_rub(float(order["usd_price"]))

        order_model = OrderModel(**order)

        process_data[order_model.order_number] = order_model

    orders_repo.create_from_dict(process_data)


def order_date_checker():
    orders = orders_repo.get_order_dates()
    today = datetime.date.today()

    for order in orders:
        if order.expired_date < today:
            send_message(order.order_number, order.expired_date)


if __name__ == "__main__":
    blocking_scheduler = BlockingScheduler()
    blocking_scheduler.add_job(main, "interval", seconds=10)

    background_scheduler = BackgroundScheduler()
    background_scheduler.add_job(order_date_checker, 'interval', seconds=24)

    try:
        background_scheduler.start()
        blocking_scheduler.start()
    except Exception as e:
        print(e)
