import datetime

from pydantic import BaseModel
from pydantic.class_validators import validator


class OrderModel(BaseModel):
    """Модель заказа для валидации"""

    table_row: int
    order_number: int
    usd_price: float
    rub_price: float
    expired_date: datetime.date
    notified: bool

    class Config:
        orm_mode = True

    @validator("expired_date", pre=True)
    def check_date(cls, v):
        if isinstance(v, str):
            now = datetime.date.today()
            v_date = datetime.datetime.strptime(v, "%d.%m.%Y").date()
            return v_date
        return v
