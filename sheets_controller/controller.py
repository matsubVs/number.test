from typing import Dict, List

import gspread
from gspread import Client
from gspread.worksheet import Worksheet

from config import *


class SheetAccessController:
    @staticmethod
    def get_client() -> Client:
        """Получение google-клиента"""
        client = gspread.authorize(CREDENTIALS)

        return client

    @staticmethod
    def get_sheet(client: Client) -> Worksheet:
        """Получение таблицы"""
        sheet = client.open(os.getenv("SHEET_FILE_NAME")).sheet1

        return sheet

    @staticmethod
    def get_sheet_data(sheet: Worksheet) -> List[Dict]:
        """Получение всех записей из таблицы"""
        return sheet.get_all_records()
