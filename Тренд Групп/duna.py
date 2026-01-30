import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://xn--80ahfqq5h.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--80ahfqq5h.xn--p1ai/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
}

json_data = {
    'action': 'objects_list',
    'data': {
        'category': 'flat',
        'activity': 'sell',
        'page': 0,
        'filters': {
            'studio': 'null',
            'rooms': [],
            'restorations': [],
            'promos': [],
            'tags': [],
            'riser_side': [],
            'geo_city': '3430',
            'floors': [],
            'geoLines': [],
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
            'isHot': False,
            'isExclusive': False,
        },
        'complex_id': 4051629,
        'house_id': None,
        'orders': [],
        'complex_search': None,
        'house_search': None,
        'lazy': False,
        'cabinetMode': False,
    },
    'auth_token': None,
    'locale': None,
}

url = 'https://api.macro.sbercrm.com/estate/catalog/?domain=xn--80ahfqq5h.xn--p1ai&check=wzrmC0pFwm-b0tm2tOlZbmKi0ufOjl2brGzj7Ocj9Ke_KlUK-q39_dWaDy7q2q3-rnwxNzY5NTg3OTA2fGRjNDIy&type=catalog&lenisPrevent=true&autoshow=false&inline=true&issetJQuery=0&uuid=b73426c8-0e70-4c73-a93d-3c75b7eba250&cookie_base64=eyJfeW1fdWlkIjoiMTc2OTU4Nzg3NzEyNjc2ODQxMiJ9&time=1769587906&token=52454aea74c417c1b528436bbf7a837b/'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



while True:
    try:
        response = requests.post(url, json=json_data, headers=headers)
        print(response.status_code)
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
        type = i["estate"]["category"]
        if type == 'flat':
            type = 'Квартира'
        area = f'{float(i["estate"]["estate_area"]):.2f}'
        price = f'{float(i["estate"]["estate_price"]):.0f}'
        floor = i["estate"]["estate_floor"]

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

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
