import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    'csrftoken': 'dc18A6B92a8a6c54A6CE76C58f7b45672430faD90924d9e0AaB6328eb67Eb5C2',
    'tmr_lvid': '7c602fbb4b46b557c69fd271bfd44083',
    'tmr_lvidTS': '1744113461164',
    'domain_sid': 'RfVqkNAlnJZxrVhiQ5Spc%3A1744113461292',
    '_cmg_csstiPQdg': '1744113462',
    '_comagic_idiPQdg': '10206793271.14411519501.1744113461',
    'scbsid_old': '2746015342',
    'gtm-session-start': '1744113461644',
    'counter': '1',
    'ab_id': '59bc78365d11c0d9bdd92160239241477342a305',
    '_ym_uid': '1744113462156893317',
    '_ym_d': '1744113462',
    '_ym_isad': '2',
    'sma_session_id': '2254310963',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBnotShow': '-1',
    '_ym_visorc': 'w',
    'SCBstart': '1744113462374',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'tmr_detect': '0%7C1744113463792',
    'sma_index_activity': '1026',
    'SCBindexAct': '772',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'baggage': 'sentry-environment=production,sentry-public_key=01001967108c53564db3c938c080d2fe,sentry-trace_id=a575e2abd79e4055957b50b2ca1c9c02',
    'priority': 'u=1, i',
    'referer': 'https://new-scherbinka.ru/flat',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a575e2abd79e4055957b50b2ca1c9c02-b4d5842addd3951f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-csrftoken': 'dc18A6B92a8a6c54A6CE76C58f7b45672430faD90924d9e0AaB6328eb67Eb5C2',
    # 'cookie': 'csrftoken=dc18A6B92a8a6c54A6CE76C58f7b45672430faD90924d9e0AaB6328eb67Eb5C2; tmr_lvid=7c602fbb4b46b557c69fd271bfd44083; tmr_lvidTS=1744113461164; domain_sid=RfVqkNAlnJZxrVhiQ5Spc%3A1744113461292; _cmg_csstiPQdg=1744113462; _comagic_idiPQdg=10206793271.14411519501.1744113461; scbsid_old=2746015342; gtm-session-start=1744113461644; counter=1; ab_id=59bc78365d11c0d9bdd92160239241477342a305; _ym_uid=1744113462156893317; _ym_d=1744113462; _ym_isad=2; sma_session_id=2254310963; SCBfrom=; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%5D; SCBnotShow=-1; _ym_visorc=w; SCBstart=1744113462374; SCBporogAct=5000; SCBFormsAlreadyPulled=true; tmr_detect=0%7C1744113463792; sma_index_activity=1026; SCBindexAct=772',
}

params = {
    'type': 'flat',
    'limit': '48',
    'offset': '0',
    'order': 'price',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://new-scherbinka.ru/api/properties/', params=params, cookies=cookies, headers=headers)

    items = response.json()["results"]


    for i in items:

        url = ''
        developer = "Квартал Инвестстрой"
        project = 'Новая Щербинка'
        korpus = int(i['building_number'])
        if i['type'] == 'flat':
            type = 'Квартира'
        else:
            type = i['type']
        try:
            if i['features'][0] == 'Отделка: Чистовая':
                finish_type = 'С отделкой'
            elif i['features'][0] == 'Отделка: Нет':
                finish_type = 'Без отделки'
            else:
                finish_type = i['features'][0]
        except:
            finish_type = ''
        room_count = i['rooms']
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['original_price'].replace('.00', ''))
        except:
            old_price = ''
        try:
            price = int(i['price'].replace('.00', ''))
        except:
            price = ''
        section = int(i['section_number'])
        try:
            floor = int(i['floor_number'])
        except:
            floor = ''
        flat_number = int(i['number'])

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

