from schemas.order import OrderModel
from sheets_controller.controller import SheetAccessController as Controller
from database.database import DB
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
from currency_convertor import usd_to_rub
from repositories.order import OrderRepository


load_dotenv()

DB.model.metadata.create_all(bind=DB.engine)

client = Controller.get_client()
orders_repo = OrderRepository()


def main():
	sheet = Controller.get_sheet(client)
	data = Controller.get_sheet_data(sheet)

	process_data = []

	for raw_order in data:
		order = {'table_row': raw_order['№'], 'order_number': raw_order['заказ №'],
		         'usd_price': raw_order['стоимость,$'], 'expired_date': raw_order['срок поставки']}
		order['rub_price'] = usd_to_rub(float(order['usd_price']))

		order_model = OrderModel(**order)
		process_data.append(OrderModel(**order))



	orders_repo.create_from_list(process_data)


if __name__ == '__main__':
	scheduler = BlockingScheduler()
	scheduler.add_job(main, "interval", seconds=10)
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		pass