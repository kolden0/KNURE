import requests

BASE_URL = "http://127.0.0.1:8000/items"
AUTH = ('kolden', 'koldenPass')

try:
    response = requests.get(BІASE_URL, auth=AUTH)
    print(response.status_code)
    print(response.json())

    new_item = {
        "name": "Sneakers",
        "price": 120.00,
        "size": "42",
        "color": "White"
    }
    response = requests.post(BASE_URL, json=new_item, auth=AUTH)
    print(response.status_code)
    created_item = response.json()
    print(created_item)
    new_id = created_item['id']

    update_data = {"price": 99.99}
    response = requests.put(f"{BASE_URL}/{new_id}", json=update_data, auth=AUTH)
    print(response.status_code)
    print(response.json())

    response = requests.delete(f"{BASE_URL}/{new_id}", auth=AUTH)
    print(response.status_code)
    print(response.json())

    response = requests.get(f"{BASE_URL}/{new_id}", auth=AUTH)
    print(response.status_code)

except requests.exceptions.ConnectionError:
    print("Connection Error")