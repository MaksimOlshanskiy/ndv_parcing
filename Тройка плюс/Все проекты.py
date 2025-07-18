import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://troikapluz.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://troikapluz.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}





project_ids_dict = {1164: 'Краснофлотский', 1165: 'Молодежный', 1168: 'Солнечный', 1172: 'Солнечный',
                    1184: 'Солнечный', 1170: 'Солнечный', 1174: 'Истомкино Парк',
                    1207: 'Портал', 1186: 'Ступино'}
korpus_dict = {1168: 'А', 1172: 'Б',
               1184: 'В', 1170: 'Г'}
project_id_list = ['6189b0f3-5afb-45fe-a904-9669921feb66', '03bf760d-27b6-4a76-b506-bed8747c7ee2',
                   'fb583e70-2b9e-4349-b91e-1b33db07dc29', '0ec2b42f-5a70-405b-8206-c4ded87d4521',
                   '3893bf57-1bb3-4cc5-aa13-a46b4638358b', '5cb71a23-587a-48df-b005-ee0c64a22eaa',
                   'd4b9079f-d5fb-4fcf-9928-10d11231dd9e', 'a0abff8a-4c49-4d67-a74f-8381de794555',
                   '873b989a-ceed-4e80-baf6-b0afe98246bd']

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

flats = []
date = datetime.now().date()

for project_id in project_id_list:

    response = requests.get(f'https://widget-server.m2lab.ru/front/realtys/{project_id}',
                            headers=headers)
    items = response.json()

    for i in items:

        if not i['status'] == 'free':
            continue

        url = ''
        developer = "Тройка плюс"
        project = project_ids_dict.get(i['externalIdHouse'])
        korpus = korpus_dict.get(i['externalIdHouse'])
        if not korpus:
            korpus = '1'
        if i['realEstateType'] == 'living':
            type = 'Квартиры'
        else:
            type = i['realEstateType']
        if not i['decoration']:
            finish_type = 'Без отделки'
        else:
            finish_type = i['decoration']
        room_count = i['roomsCount']
        if room_count == 'studio':
            room_count = '0'
        try:
            area = float(i['sq'])
        except:
            area = ''
        try:
            old_price = int(i['price'].replace('.00', ''))
        except:
            old_price = ''
        price = ''

        section = i['section']
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = i['number']
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
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]

        flats.append(result)

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

filename = f"{developer}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
