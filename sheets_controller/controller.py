from typing import Dict, List

import gspread
from gspread import Client
from gspread.worksheet import Worksheet

from config import *


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
