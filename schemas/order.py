import datetime

from pydantic import BaseModel
from pydantic.class_validators import validator


class OrderModel(BaseModel):
    """Модель заказа для валидации"""

    order_number: int
    usd_price: float
    rub_price: float
    expired_date: datetime.date

    # class Config:
    #     orm_mode = True

    @validator("order_number", "expired_date", pre=True)
    def check_date(cls, v):
        now = datetime.date.today()
        print(v)
        return datetime.datetime.strptime(v, "%d.%m.%Y").date()
