'''

по очереди по каждому дому 'house_id'

'''

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://xn--h1aafhhcesj.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--h1aafhhcesj.xn--p1ai/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
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
            'restorations': [
                276,
            ],
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
        'complex_id': None,
        'house_id': 3147458,    # 7095059
        'orders': [],
        'complex_search': None,
        'house_search': None,
        'lazy': True,
        'cabinetMode': False,
    },
    'auth_token': None,
    'locale': None,
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://api.macroserver.ru/estate/catalog/?domain=xn--h1aafhhcesj.xn--p1ai&check=toQdDaB-5SM-IFhFuTSiFWydI9EAfWV3pHRAGBPI6LqXST-96LDk9D_nNgZjIlJsVc-9fDE3NDQyOTQ5MTZ8N2I0OTE&type=catalog&inline=true&issetJQuery=0&presmode=complex&complexid=3147490&uuid=9237f7af-3c5a-4841-bfc3-7eb5e0abaffc&cookie_base64=eyJfeW1fdWlkIjoiMTc0NDI5NDY0NjY3MjUwMTA1MyJ9&time=1744294916&token=3dbab31d00221254978f172118093a8b/',
        headers=headers,
        json=json_data,
    )
    if response.json()['isLastPage']:
        break
    items = response.json()["objects"]



    for i in items:
        if i['status'] != 'available':
            continue

        url = i['id']
        developer = "Галакс"
        project = 'Истомкино'
        korpus = ''
        type = 'Квартиры'
        finish_type = 'С отделкой'
        room_count = extract_digits_or_original(i['rooms'])
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int()
        except:
            old_price = ''
        try:
            price = int(i['price'].replace('.0000', ''))
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = ''

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
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''



        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not items:
        break
    json_data['data']['page'] += 1
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

df = pd.DataFrame(flats, columns=['Дата обновления',
 'Название проекта',
 'на англ',
 'промзона',
 'Местоположение',
 'Метро',
 'Расстояние до метро, км',
 'Время до метро, мин',
 'МЦК/МЦД/БКЛ',
 'Расстояние до МЦК/МЦД, км',
 'Время до МЦК/МЦД, мин',
 'БКЛ',
 'Расстояние до БКЛ, км',
 'Время до БКЛ, мин',
 'статус',
 'старт',
 'Комментарий',
 'Девелопер',
 'Округ',
 'Район',
 'Адрес',
 'Эскроу',
 'Корпус',
 'Конструктив',
 'Класс',
 'Срок сдачи',
 'Старый срок сдачи',
 'Стадия строительной готовности',
 'Договор',
 'Тип помещения',
 'Отделка',
 'Кол-во комнат',
 'Площадь, кв.м',
 'Цена кв.м, руб.',
 'Цена лота, руб.',
 'Скидка,%',
 'Цена кв.м со ск, руб.',
 'Цена лота со ск, руб.',
 'секция',
 'этаж',
 'номер'])



# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}-с-1.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

