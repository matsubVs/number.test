import gspread
from gspread.worksheet import Worksheet
from gspread import Client
from config import *


class SheetAccessController:

    def __init__(self):
        self.client = self.get_client()
        self.sheet = self.get_sheet(self.client)
        self.data = self.get_sheet_data(self.sheet)


    @staticmethod
    def get_client() -> Client:
        client = gspread.authorize(CREDENTIALS)

        return client

    @staticmethod
    def get_sheet(client: Client) -> Worksheet:
        sheet = client.open("Копия тестовое").sheet1

        return sheet

    @staticmethod
    def get_sheet_data(sheet: Worksheet) -> dict:
        return sheet.get_all_records()
