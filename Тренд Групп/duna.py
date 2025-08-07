import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://xn--80ahfqq5h.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--80ahfqq5h.xn--p1ai/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

json_data = {
    'action': 'objects_list',
    'data': {
        'category': 'flat',
        'activity': 'sell',
        'page': 1,
        'filters': {
            'studio': 'null',
            'rooms': [],
            'restorations': [],
            'promos': [],
            'tags': [],
            'riser_side': [],
            'geo_city': None,
            'floors': [],
            'houses_ids': [],
            'type': None,
            'areaFrom': None,
            'areaTo': None,
            'priceFrom': None,
            'priceTo': None,
            'priceM2From': None,
            'priceM2To': None,
            'priceRentFrom': None,
            'priceRentTo': None,
            'priceRentM2From': None,
            'priceRentM2To': None,
            'status': None,
        },
        'complex_id': 4051629,
        'house_id': None,
        'orders': [
            {
                'field': 'price',
                'direction': 'asc',
            },
        ],
        'complex_search': None,
        'house_search': [],
        'cabinetMode': False,
    },
    'auth_token': None,
    'locale': None,
}

url = 'https://api.macro.sbercrm.com/estate/catalog/?domain=xn--80ahfqq5h.xn--p1ai&check=wzrmC0pFwm-b0tm2tOlZbmKi0ufOjl2brGzj7Ocj9Ke_KlUK-q39_dWaDy7q2q3-rnwxNzQyMzgyNjk2fGI5ZDhi&type=catalog&autoshow=false&inline=true&presmode=complex&complexid=4051629&presMode=complex&complexId=4051629&fromApi=true&domain_config=%5Bobject+Object%5D&domain_config_overwrite=%5Bobject+Object%5D&issetJQuery=1&uuid=744bf420-db98-4455-96df-9cd6ee741451&cookie_base64=eyJfZ2EiOiJHQTEuMS4xODkzMjg2NzgzLjE3NDIzODI2OTMiLCJfeW1fdWlkIjoiMTc0MjM4MjY5NDY3NTA2ODEyNCJ9&time=1742382696&token=3183e0e31046220ef577675e46c4cf10/'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



while True:
    try:
        response = requests.get(url, json=json_data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        break

    item = response.json()


    items = item.get("objects", [])

    for i in items:
        date = datetime.date.today()
        project = "Дюна"
        developer = 'Тренд групп'

        text = str(i["house_title"])
        cleaned_text = text.replace("&nbsp;", " ")
        parts = [part.strip() for part in cleaned_text.split(",")]
        korpus = int(parts[-1].replace('корпус&nbsp', ''))

        room_count = i["estate"]["estate_rooms"]
        type = i["category"]
        if type == 'flat':
            type = 'Квартира'
        area = f'{float(i["area"]):.2f}'
        price = f'{float(i["price"]):.0f}'
        floor = i["floor"]

        print(
            f"{count} | {i['flatnum']} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, 'Предчистовая', room_count, area, '', int(price), '', '', '',
                  '', floor, '']
        flats.append(result)
        count += 1

    # Проверяем, является ли текущая страница последней
    if item.get("isLastPage", False):  # Если isLastPage == True, завершаем цикл
        print("Достигнута последняя страница.")
        break

    # Увеличиваем номер страницы
    json_data['data']['page'] += 1

    time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
