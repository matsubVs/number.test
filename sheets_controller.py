import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

SCOPES = [
	'https://www.googleapis.com/auth/spreadsheets',
	'https://www.googleapis.com/auth/drive'
]

CREDENTIALS =  ServiceAccountCredentials.from_json_keyfile_name(
	os.path.join('/google-sheets', "/secret", "secret_key.json"),
	scopes=SCOPES
)

