import datetime
import time
import requests
import random
from functions import save_flats_to_excel
from info_1DSK import info


flats = []
count = 1

for key, data in info.items():
    headers = data['headers']
    params = data['params']
    cookies = data['cookies']

    response = requests.get('https://www.dsk1.ru/api/v3/flats/all', params=params, cookies=cookies, headers=headers)
    items = response.json()

    for i in items:
        url = i["externalId"]
        date = datetime.date.today()
        project = i["project"]["title"]
        developer = "ДСК-1"
        korpus = str(i["corpus"]["number"].replace(',','.'))
        type = i["crmObjectType"]

        if type == 'Студия':
            room_count = 'Студия'
            type = 'Квартира'
        else:
            room_count = int(i["crmRoomsQty"])

        finish_type = ''

        for j in i['labels']:
            if 'отделк' in j['title'].lower():
                finish_type = j['title']

        if finish_type == 'Отделка White Box + с/у под ключ' or finish_type == 'Отделка White Box':
            finish_type = 'Предчистовая'
        elif finish_type == 'Чистовая отделка':
            finish_type = 'С отделкой'

        area = i["areaTotal"]
        old_price = i["priceWoDiscount"]
        price = i["price"]
        section = i["section"]["number"]
        floor = int(i["floor"]["number"])

        if old_price == price:
            price = None

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, отделка: {finish_type}")

        result = [
            date, project, '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', developer,
            '', '', '', '', korpus, '', '', '', '', '',
            '', type, finish_type, room_count, area, '', old_price, '', '',
            price, section, floor, ''
        ]
        flats.append(result)
        count += 1

    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)  # Задержка между запросами

save_flats_to_excel(flats, 'all', developer)
