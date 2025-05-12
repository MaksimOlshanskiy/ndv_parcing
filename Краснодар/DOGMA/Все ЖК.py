import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://dogma.ru',
    'priority': 'u=1, i',
    'referer': 'https://dogma.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

json_data = {
    'areas': [
        19.2,
        222.4,
    ],
    'costs': [
        3400000,
        37800000,
    ],
    'deadlines': [],
    'floors': [
        1,
        24,
    ],
    'layout_id': [],
    'letter_ids': [],
    'limit': 100,
    'offset': 0,
    'ids': [],
    'project_ids': [
        8,
        2,
        1,
        3,
    ],
    'rooms': [],
    'statuses': [
        2,
    ],
    'tags': [],
    'types': [
        1,
    ],
    'group_by': '',
    'order': {
        'field': 'cost',
        'type': 'asc',
    },
    'classes': [],
}

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://service.1dogma.ru/api/layouts-filter/v2/objects/filter', headers=headers, json=json_data)
    print(response.status_code)
    print(response)
    if response.status_code != 200:
        break

    items = response.json()['objects']
    if items is None:
        break


    for i in items:

        url = ''
        developer = "DOGMA"
        project = i['project_name']
        korpus = i['letter_name']
        section = ''
        type = ''
        try:
            if i['tags'][0]['text'] == 'С отделкой':
                finish_type = 'С отделкой'
            else:
                finish_type = 'Без отделки'
        except:
            finish_type = 'Без отделки'
        room_count = i['room']
        flat_number = ''
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['cost'])
        except:
            old_price = ''
        try:
            price = int(i['cost_sale'])
        except:
            price = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''


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
    print(f"Квартир загружено:{len(flats)}")
    json_data['offset'] += 100
    sleep_time = random.uniform(0.1, 0.2)
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

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

