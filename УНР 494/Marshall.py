import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests
from info import info

all_flats = []


def fetch_data(name, conf):
    flats = []
    count = 1

    response = requests.get(
        conf['url'],
        params=conf['params'],
        headers=conf['headers'],
        cookies=conf['cookies']
    )

    if response.status_code == 200:
        data = response.json()
        items = data.get('apartments', {})

        for i, j in items.items():
            if j.get("st", '') == 0:
                continue

            date = datetime.date.today()
            project = 'Маршал'
            developer = '494 УНР'
            korpus = j.get('b', '')
            if conf['url'] == 'https://xn----8sbavuje7a2e.xn--p1ai/hydra/json/apart.json':
                finish_type = 'С отделкой и доп опциями'
                type = 'Апартаменты'
            else:
                if korpus == 3:
                    finish_type = 'Без отделки'
                else:
                    finish_type = 'Предчистовая'
                type = 'Квартира'
            room_count = j.get('rc', '')
            area = j.get("sq", '')
            old_price = j.get('tc', '')
            price = j.get("sc", '')
            floor = j.get('f', '')

            if price == old_price:
                price = None

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                      '', floor, '']
            flats.append(result)
            count += 1
    else:
        print(f'Ошибка: {response.status_code}')

    time.sleep(0.05)
    return flats


for name, conf in info.items():
    all_flats.extend(fetch_data(name, conf))

# сохраняем всё одним вызовом
save_flats_to_excel(all_flats, 'Маршал', '494УНР')
