import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_inr_history():
    data = []
    today = datetime.now()

    for i in range(30):
        date_query = today - timedelta(days=i)
        date_str = date_query.strftime("%Y%m%d")

        url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=INR&date={date_str}&json"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                result = response.json()
                if result:
                    data.extend(result)
        except Exception:
            pass

    return data


def plot_currency(data):
    if not data:
        return

    data.sort(key=lambda x: datetime.strptime(x['exchangedate'], "%d.%m.%Y"))

    dates = []
    rates = []

    for item in data:
        date_obj = datetime.strptime(item['exchangedate'], "%d.%m.%Y")
        dates.append(date_obj.strftime("%d.%m"))
        rates.append(item['rate'])

    plt.figure(figsize=(12, 6))
    plt.plot(dates, rates, marker='o', linestyle='-', color='r', label='INR Rate')

    plt.title('INR Exchange Rate (Last 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('UAH')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    history = get_inr_history()
    plot_currency(history)