from oauth2client.service_account import ServiceAccountCredentials
import os

path = os.path.dirname(__file__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(
    path + "/secret/secret_key.json", scopes=SCOPES
)
