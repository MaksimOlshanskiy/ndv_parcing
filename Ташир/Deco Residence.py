import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    '_ga': 'GA1.1.724058775.1748502134',
    'tmr_lvid': '720b205ffdc022a0ba63c80dc1168e0b',
    'tmr_lvidTS': '1748502134042',
    '_ym_uid': '174850213541426751',
    '_ct_ids': 'pdxt2u4a%3A55550%3A456353568',
    '_ct_session_id': '456353568',
    '_ct_site_id': '55550',
    'call_s': '___pdxt2u4a.1748503933.456353568.288727:921300|2___',
    '_ct': '2300000000298465139',
    '_ym_isad': '2',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_visorc': 'w',
    'domain_sid': 'SBFYXyW3n8MpXTFhnqCAw%3A1748502134938',
    'cted': 'modId%3Dpdxt2u4a%3Bclient_id%3D724058775.1748502134%3Bya_client_id%3D174850213541426751',
    'tmr_detect': '0%7C1748502136601',
    '_ga_51HVC5PZZS': 'GS2.1.s1748502133$o1$g1$t1748502142$j51$l0$h0',
    '_ym_d': '1748502162',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru',
    'priority': 'u=1, i',
    'referer': 'https://deco-residence.ru/filter',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-site': 'deco-residence.ru',
    # 'cookie': '_ga=GA1.1.724058775.1748502134; tmr_lvid=720b205ffdc022a0ba63c80dc1168e0b; tmr_lvidTS=1748502134042; _ym_uid=174850213541426751; _ct_ids=pdxt2u4a%3A55550%3A456353568; _ct_session_id=456353568; _ct_site_id=55550; call_s=___pdxt2u4a.1748503933.456353568.288727:921300|2___; _ct=2300000000298465139; _ym_isad=2; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_visorc=w; domain_sid=SBFYXyW3n8MpXTFhnqCAw%3A1748502134938; cted=modId%3Dpdxt2u4a%3Bclient_id%3D724058775.1748502134%3Bya_client_id%3D174850213541426751; tmr_detect=0%7C1748502136601; _ga_51HVC5PZZS=GS2.1.s1748502133$o1$g1$t1748502142$j51$l0$h0; _ym_d=1748502162',
}

params = {
    'limit': '12',
    'offset': '0',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://deco-residence.ru/api/flat/', params=params, cookies=cookies, headers=headers)
    items = response.json()['results']
    print(items)

    for i in items:


        if i['is_booked']:
            continue
        url = ''
        developer = "Ташир"
        project = 'Deco Residence'
        korpus = '1'
        section = i['section_number']
        if i['type'] == "APARTMENT":
            type = 'Апартаменты'
        finish_type = 'Предчистовая'
        room_count = i['rooms']
        flat_number = i['number']
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['origin_price'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        try:
            floor = int(i['floor_number'])
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
    params['offset'] = str(int(params['offset']) + 12)
    sleep_time = random.uniform(1, 4)
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

