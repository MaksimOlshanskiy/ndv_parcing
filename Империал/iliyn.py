import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'origin': 'https://ilin-loft.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://ilin-loft.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

params = {
    'storepartuid': '662416564071',
    'recid': '647076963',
    'c': '1744187673167',
    'getparts': 'true',
    'getoptions': 'true',
    'slice': '1',
    'filters[quantity]': 'y',
    'sort[price]': 'desc',
    'size': '36',
}

url = 'https://store.tildaapi.com/api/getproductslist/'

flats = []

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    item = response.json()

    items = item.get("products", [])

    for i in items:
        date = datetime.date.today()
        project = 'Лофт Ильин'
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
        developer = "Империал"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''

        try:
            korpus = i['brand'].replace(' ', '').replace('корпус', '')
        except:
            flat_number = str(i['title'].replace(' ', '').replace('№', ''))
            flat_parts = flat_number.split('/')
            korpus = flat_parts[1] if len(flat_parts) > 1 else None

        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'апартамент'
        finish_type = 'С отделкой'

        room_count = 'студия'
        area = float(
            i["descr"].replace('Евростудия с отделкой ', '').replace(' м2', '').replace(' ', '').replace(',', '.'))
        price_per_metr = ''
        old_price = i['priceold']
        discount = ''
        price_per_metr_new = ''
        price = float(i["price"])
        section = ''

        flat_number = str(i['title'].replace(' ', '').replace('№', ''))
        floor = flat_number[0] if flat_number[0].isdigit() else None
        flat_number = ''

        if old_price == '':
            old_price = price
            price = None

        print(
            f"{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                  mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
