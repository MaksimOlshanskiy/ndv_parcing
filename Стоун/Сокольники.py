import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    'abgroup': 'B',
    '_ym_uid': '1743402914697638259',
    '_ym_d': '1743402914',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ga': 'GA1.1.997974877.1743402914',
    'scbsid_old': '2746015342',
    '_cmg_cssty4CyW': '1743402915',
    '_comagic_idy4CyW': '10524067984.14652705469.1743402914',
    'sma_session_id': '2244207952',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1743402941094',
    'sma_postview_ready': '1',
    '_ga_JRHY2GHQN0': 'GS1.1.1743402914.1.1.1743402953.21.0.1066333902',
    'SCBindexAct': '54',
    'sma_index_activity': '6508',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Referer': 'https://stone.ru/catalog/residential?filter[status]=1&filter[direction]=2',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'abgroup=B; _ym_uid=1743402914697638259; _ym_d=1743402914; _ym_isad=2; _ym_visorc=w; _ga=GA1.1.997974877.1743402914; scbsid_old=2746015342; _cmg_cssty4CyW=1743402915; _comagic_idy4CyW=10524067984.14652705469.1743402914; sma_session_id=2244207952; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBporogAct=5000; SCBstart=1743402941094; sma_postview_ready=1; _ga_JRHY2GHQN0=GS1.1.1743402914.1.1.1743402953.21.0.1066333902; SCBindexAct=54; sma_index_activity=6508',
}

params = {
    "filter[status]": 1,
    "filter[direction]": 2,
    "filter[projects]": 8,
    "sort": "lots.selling_price",
    "page": 1
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://stone.ru/api/lots',
        cookies=cookies,
        headers=headers,
        params=params
    )

    items = response.json()["data"]


    for i in items:

        url = ''
        developer = "Стоун"
        project = 'Сокольники'
        korpus = i['housing']
        type = i['type_name']
        finish_type = ''
        room_count = i['bedrooms_count']
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['selling_price_before_discount'])
        except:
            old_price = ''
        try:
            price = int(i['selling_price'])
        except:
            price = ''
        section = int(i['section'])
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
        adress = i['address']
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = i['project']['catalog_features'][0]['val']
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
    params['page'] += 1
    sleep_time = random.uniform(1, 3)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Стоун"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

