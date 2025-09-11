import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1757078189201779430',
    '_ym_d': '1757078189',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstpyx3O': '1757078190',
    '_comagic_idpyx3O': '11134599871.15483538741.1757078190',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://om-development.ru/flats?complex_id=881b6cc9-4f93-4a8d-bf41-0f45056c02db',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'x-host': 'om-development.ru',
    # 'cookie': '_ym_uid=1757078189201779430; _ym_d=1757078189; _ym_isad=2; _ym_visorc=w; _cmg_csstpyx3O=1757078190; _comagic_idpyx3O=11134599871.15483538741.1757078190',
}

params = {
    'project_id': '9ca5a862-f2e6-4b3d-8bcf-30e080b8f5d1',
    'status': 'free',
    'offset': '0',
    'limit': '16',
    'complex_id': '881b6cc9-4f93-4a8d-bf41-0f45056c02db',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://om-development.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    items = response.json()


    for i in items:

        url = ''
        developer = "OM Development"
        project = 'Станиславский'
        korpus = i['building_int_number']
        type = 'Квартиры'
        if i['finishing_type'] == 'no':
            finish_type = 'Без отделки'
        elif i['finishing_type'] == 'fine':
            finish_type = 'С отделкой'
        elif i['finishing_type'] == 'white_box':
            finish_type = 'Предчистовая'
        else:
            finish_type = i['finishing_type']
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
        srok_sdachi = i['completion_title']
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

save_flats_to_excel(flats, project, developer)

