import requests


def usd_to_rub(usd: float) -> float:
	data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
	currency = float(data['Valute']['USD']['Value'])

	return usd * currency