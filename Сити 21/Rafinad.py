import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'PHPSESSID': 'o6uttwvgxYszRZaCmbhmN5o7FoMFoIyp',
    '_ym_uid': '1742306840508857028',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

base_url = 'https://dom-rafinad.ru/ajax/get_flats_example.json'

flats = []
page = 1
count = 1
limit = 12  # Количество квартир на странице
max_pages = 8  # Ограничение в 8 страниц (по API)

while page <= max_pages:
    offset = (page - 1) * limit
    params = {
        'sort': 'price',
        'sort_order': 'asc',
        'price_from': '7051141',
        'price_to': '14386535',
        'area_from': '34',
        'area_to': '65',
        'floor_from': '1',
        'floor_to': '8',
        'action': 'get_flats',
        'limit': str(limit),
        'offset': str(offset),
    }

    response = requests.get(base_url, params=params, cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        break

    item = response.json()
    items = item.get("flats", [])

    if not items:
        print("Квартиры закончились.")
        break

    print(f"Страница {page}, offset {offset}, квартир: {len(items)}")

    for i in items:
        date = datetime.date.today()
        project = 'Рафинад'
        developer = 'Сити21'
        korpus = i.get("bld", "")
        room_count = i.get("rooms", "")
        type = 'Квартира'
        finish_type = 'Предчистовая' if i.get("finish_pred", 0) else 'Без отделки'
        area = i.get("area", "")
        old_price = i.get("oldPrice", "")
        price = i.get("price", "")
        section = i.get("section", "")
        floor = i.get("floor", "")

        if old_price == '':
            old_price = price
            price = None

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        count += 1

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                  section, floor, '']
        flats.append(result)

    # Увеличиваем номер страницы
    page += 1

    # Задержка между запросами
    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
