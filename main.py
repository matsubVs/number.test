import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from utils.parse_sheet_data import parse_data
from database.database import DB
from repositories.order import OrderRepository
from sheets_controller.controller import SheetAccessController as Controller
from tg.sender import send_message

load_dotenv()

DB.model.metadata.create_all(bind=DB.engine)

client = Controller.get_client()
orders_repo = OrderRepository()


def main():
    sheet = Controller.get_sheet(client)
    data = Controller.get_sheet_data(sheet)

    process_data = parse_data(data)

    orders_repo.create_from_dict(process_data)


def order_date_checker():
    orders = orders_repo.get_outdated_orders()

    m_orders = orders.all()

    for order in m_orders:
        send_message(order.order_number, order.expired_date)

    orders_repo.set_notified(orders)



if __name__ == "__main__":
    blocking_scheduler = BlockingScheduler()
    blocking_scheduler.add_job(main, "interval", seconds=10, max_instances=2)

    background_scheduler = BackgroundScheduler()
    background_scheduler.add_job(
        order_date_checker, "interval", seconds=10, max_instances=2
    )

    try:
        background_scheduler.start()
        blocking_scheduler.start()
    except Exception as e:
        print(e)
