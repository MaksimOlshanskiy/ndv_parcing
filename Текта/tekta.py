import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Конфигурация
cookies = {
    'hl': 'ru',
    'mindboxDeviceUUID': '47c7cae1-5c38-4490-9fcc-32906301e64b',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
}

params = {
    'area[from]': '1',
    'area[to]': '999.5',
    'floor[from]': '1',
    'floor[to]': '99',
    'price[from]': '150000',
    'price[to]': '1092000000',
    'status': 'on',
    'sort': 'price-asc',
    'project': 'all',
    'type': 'flat',
    'locale': 'ru',
    'offset': '0',
}

base_url = 'https://tekta.ru/api/search'

flats = []
offset = 0
limit = 10
count = 0
developer = "Текта"

while True:
    params['offset'] = offset

    response = requests.get(base_url, params=params, cookies=cookies, headers=headers)

    if response.status_code != 200:
        print(f'Ошибка: {response.status_code}')
        break

    data = response.json()
    items = data.get("data", [])

    if not items:
        print("Данные закончились, завершаю обработку.")
        break

    for i in items:
        count += 1
        date = datetime.date.today()
        project = i["project"]
        english = ''
        promzona = ''
        mestopolozhenie = ''
        subway = ''
        distance_to_subway = ''
        time_to_subway = ''
        mck = ''
        distance_to_mck = ''
        time_to_mck = ''
        bkl = ''
        distance_to_bkl = ''
        time_to_bkl = ''
        status = ''
        start = ''
        comment = ''
        developer = "Текта"
        okrug = i["locationText"]
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["building"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = "Квартира"
        if i["decor"] == False:
            finish_type = 'Без отделки'
        else:
            finish_type = 'Предчистовая'
        room_count = i["roomCount"]
        area = i["area"]
        price_per_metr = ''
        old_price = i["originalPrice"]
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        section = ''
        floor = i["floor"]
        flat_number = ''

        if old_price == price:
            price = None

        print(
            f"{count} | {project}, {finish_type}, тип: {type}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [
            date, project, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", developer, okrug, "", "", "",
            korpus,
            "", "", "", "", "", "", "Квартира", finish_type, room_count, area, "", old_price, "", "", price, "", floor,
            ""
        ]
        flats.append(result)

    # Увеличиваем offset для следующего запроса
    offset += limit
    time.sleep(0.1)  # Задержка между запросами

save_flats_to_excel(flats, 'all', developer)
