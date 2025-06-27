import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ct': '2800000000121563453',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_uid': '1743764280660177038',
    '_ym_d': '1743764280',
    'amplitude_id_de5f414583dc2ee7cc70a58b21551c09dom-ideal.ru': 'eyJkZXZpY2VJZCI6IjgwNzI3MWM4LWFmMjQtNGI3YS1iMjNjLTE3NjFkN2Q3MjM3MFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NDI5NTEwNjc1MSwibGFzdEV2ZW50VGltZSI6MTc0NDI5NTEwNjc1MSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9',
    'session': '470659aeac2ad11208750e937d8234a990e122a0bc135134bce636c89170cfb4',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://dom-ideal.ru/flats?status=free&status=booked&offset=96&limit=16',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-host': 'dom-ideal.ru',
    # 'cookie': 'BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ct=2800000000121563453; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_uid=1743764280660177038; _ym_d=1743764280; amplitude_id_de5f414583dc2ee7cc70a58b21551c09dom-ideal.ru=eyJkZXZpY2VJZCI6IjgwNzI3MWM4LWFmMjQtNGI3YS1iMjNjLTE3NjFkN2Q3MjM3MFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NDI5NTEwNjc1MSwibGFzdEV2ZW50VGltZSI6MTc0NDI5NTEwNjc1MSwiZXZlbnRJZCI6MCwiaWRlbnRpZnlJZCI6MCwic2VxdWVuY2VOdW1iZXIiOjB9; session=470659aeac2ad11208750e937d8234a990e122a0bc135134bce636c89170cfb4; _ym_visorc=w; _ym_isad=2',
}

params = {
    'project_id': 'fc84199f-0e86-4840-97ab-d89067f06a79',
    'status': 'free',
    'offset': '0',
    'limit': '16',
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://dom-ideal.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    # if response.json()['isLastPage']:
    #     break
    items = response.json()



    for i in items:
        # if i['status'] != 'available':
        #     continue

        url = ''
        developer = "Альфа Проджект"
        project = 'Идеал'
        korpus = ''
        try:
            if i['type'] == 'flat':
                type = 'Квартира'
        except:
            type = ''
        if i['finishing_type'] == 'fine':
            finish_type = 'С отделкой'
        else:
            finish_type = 'Без отделки'
        room_count = i['rooms']
        try:
            area = float(i['total_area'])
        except:
            area = ''
        try:
            old_price = int(i['old_price'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        section = int(i['section_number'])
        try:
            floor = int(i['floor_number'])
        except:
            floor = ''
        flat_number = i['int_number']

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
    params['offset'] = str(int(params['offset']) + 16)
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

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

