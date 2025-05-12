import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

import requests

cookies = {
    'session': '66db614237b50b4410475b0f5728607c2ecf4b1958b901fd7c760dc695522ea1',
    'tmr_lvid': '9d70403686a809f88ffed7e0be97ad87',
    'tmr_lvidTS': '1744123183149',
    '_ym_uid': '1744123184975636231',
    '_ym_d': '1744123184',
    '_ym_isad': '2',
    'domain_sid': 'EN61jaTFwmqrIUj5aoVGH%3A1744123183961',
    '_ym_visorc': 'w',
    'tmr_detect': '0%7C1744123185486',
    '_cmg_cssta5X99': '1744123186',
    '_comagic_ida5X99': '10589670029.14726334554.1744123185',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://triumf-pushkino.ru/flats',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-host': 'triumf-pushkino.ru',
    # 'cookie': 'session=66db614237b50b4410475b0f5728607c2ecf4b1958b901fd7c760dc695522ea1; tmr_lvid=9d70403686a809f88ffed7e0be97ad87; tmr_lvidTS=1744123183149; _ym_uid=1744123184975636231; _ym_d=1744123184; _ym_isad=2; domain_sid=EN61jaTFwmqrIUj5aoVGH%3A1744123183961; _ym_visorc=w; tmr_detect=0%7C1744123185486; _cmg_cssta5X99=1744123186; _comagic_ida5X99=10589670029.14726334554.1744123185',
}

params = {
    'project_id': 'afbd9c73-caa4-4e11-88bd-3d752d7730c8',
    'status': 'free',
    'offset': '0',
    'limit': '48',
    'order_by': 'price',
}




flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://triumf-pushkino.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    items = response.json()


    for i in items:

        url = ''
        developer = "Корпорация ВИТ"
        project = 'Триумф'
        try:
            korpus = int(i['building_int_number'])
        except:
            korpus = ''
        if i['type'] == 'flat':
            type = 'Квартира'
        else:
            type = i['type']
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
        section = ''
        try:
            floor = int(i['floor_number'])
        except:
            floor = ''
        flat_number = int(i['int_number'])

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
    params['offset'] = str(int(params['offset']) + 48)
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

