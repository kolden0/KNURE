from bottle import route, run, request
import requests
from datetime import datetime, timedelta

@route('/currency')
def currency_nbu():
    base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    target_date = None

    if 'today' in request.query:
        target_date = datetime.now()
    elif 'yesterday' in request.query:
        target_date = datetime.now() - timedelta(days=1)
    else:
        return "?today or ?yesterday"

    date_str = target_date.strftime("%Y%m%d")

    try:
        response = requests.get(f"{base_url}?valcode=INR&date={date_str}&json")
        data = response.json()

        if data:
            rate = data[0]['rate']
            date_val = data[0]['exchangedate']
            return f"INR {date_val}: {rate}"
        else:
            return "INR data not found"

    except Exception as e:
        return f"Connect found: {e}"


if __name__ == '__main__':
    run(host='localhost', port=8000)