import datetime
import pandas as pd
import os
import requests
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://www.gkvostok2.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.gkvostok2.ru/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

base_params = {
    'gk': 'bu9ece90tp2f0th77xe6sev9',
    'price_min': '49224',
    'price_max': '4374000099',
    'area_min': '14.49',
    'area_max': '999',
    'floor_min': '1',
    'floor_max': '99',
    'ordering': 'price',
    'pagination[page]': '1',
    'pagination[pageSize]': '10',
}

flats = []
page = 1
has_more_data = True

try:
    while has_more_data:
        params = base_params.copy()
        params['pagination[page]'] = str(page)

        response = requests.get('https://cms.gk-matur.ru/api/flats', params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            items = data.get('data', [])

            if not items:
                has_more_data = False
                break

            print(f"Получено {len(items)} записей со страницы {page}")  # Отладочная информация

            for i in items:
                try:
                    date = datetime.date.today()
                    project = 'Восток 2'
                    developer = "Новое время"
                    korpus = i['building']
                    room_count = i['rooms_ammount']
                    type_ = "Квартира"
                    area = i['total_square']
                    price_per_metr = i['cost']
                    old_price = int(price_per_metr * area)
                    try:
                        price = i['discount_price']
                    except:
                        price = int(price_per_metr * area)

                    section = i['section']
                    floor = i['floor']


                    print(
                        f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', float(str(korpus)), '', '', '', '',
                        '', '', type_, 'Предчистовая', room_count, area, price_per_metr, old_price, '',
                        '', price, int(section), int(str(floor)), ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            page += 1

            time.sleep(1)

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            has_more_data = False

except Exception as e:
    print(f"Общая ошибка: {e}")

# Проверяем количество полученных записей
print(f"Всего получено записей: {len(flats)}")

if flats:
    save_flats_to_excel(flats,project,developer)
else:
    print("Нет данных для сохранения")
