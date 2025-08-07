import datetime
import time
import requests
import re

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

# Настройки запроса
base_url = "https://odinburg.ru/api/elector/apartment"
cookies = {}
headers = {
    'accept': 'application/json, text/plain, */*',
    'content-type': 'application/json',
    'origin': 'https://odinburg.ru',
    'referer': 'https://odinburg.ru/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
json_data = {
    'floor': [2, 24],
    'square': [24, 122],
    'price': [6, 27],
    'sort': 'price_asc',
    'offset': 0,
}

project = "Одинбург"
developer = "АФИ"
flats = []
offset = 0
count = 0


def fetch_data(offset):
    json_data['offset'] = offset
    response = requests.post(base_url, json=json_data, cookies=cookies, headers=headers)
    response.raise_for_status()
    return response.json()


try:
    data = fetch_data(offset)
    total = data.get('total', 0)
    print(f"Всего квартир в базе: {total}")

    while offset < total:
        data = fetch_data(offset)
        items = data.get('items', [])

        if not items:
            break

        for i in items:
            count += 1
            date = datetime.date.today()
            korpus = i['corpus']

            if i['whiteBox'] == False:
                finish_type = 'Без отделки'
            else:
                finish_type = 'Предчистовая'

            room_count = i['rooms']

            if room_count == 0:
                room_count = 'студия'

            type = 'Квартира'
            area = i['area']
            old_price = float(i['price']['oldPrice']) * 1000000
            price_per_metr_new = ''
            price = float(i['price']['current']) * 1000000
            section = i['section']
            floor = str(i.get('floor', '')).split('/')[0]

            if old_price == price:
                price = None

            print(
                f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '', '', '',
                      '', korpus, '', '', '', '', '', '', type, finish_type, room_count, float(area), '',
                      int(old_price), '', '',
                      int(price), int(section), int(floor), '']
            flats.append(result)

        offset += len(items)
        print(f"Загружено {len(flats)} из {total}")

        time.sleep(1)

    save_flats_to_excel(flats, project, developer)

    print(f"Успешно сохранено {len(flats)} квартир")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к серверу: {e}")
