from utils.currency_convertor import usd_to_rub
from schemas.order import OrderModel


def parse_data(sheet_data):
    process_data = {}

    for raw_order in sheet_data:
        order = {
            "table_row": raw_order["№"],
            "order_number": raw_order["заказ №"],
            "usd_price": raw_order["стоимость,$"],
            "expired_date": raw_order["срок поставки"],
        }
        order["rub_price"] = usd_to_rub(float(order["usd_price"]))

        order_model = OrderModel(**order)

        process_data[order_model.order_number] = order_model

    return process_data
