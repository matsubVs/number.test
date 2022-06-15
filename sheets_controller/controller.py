import gspread
from gspread.worksheet import Worksheet
from gspread import Client
from config import *

from typing import List, Dict


class SheetAccessController:

    @staticmethod
    def get_client() -> Client:
        client = gspread.authorize(CREDENTIALS)

        return client

    @staticmethod
    def get_sheet(client: Client) -> Worksheet:
        sheet = client.open("Копия тестовое").sheet1

        return sheet

    @staticmethod
    def get_sheet_data(sheet: Worksheet) -> List[Dict]:
        return sheet.get_all_records()
