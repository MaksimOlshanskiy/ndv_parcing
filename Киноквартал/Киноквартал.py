import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'session': 'c02def3adb1df7a7c2afc03f8957cc113038213a736bb7dda7f28cce4f6a4bd9',
    '_ym_uid': '174411617377976528',
    '_ym_d': '1753350977',
    '_ym_isad': '2',
    'cted': 'modId%3Djs5ahoyi%3Bya_client_id%3D174411617377976528',
    '_ym_visorc': 'w',
    '_ct_ids': 'js5ahoyi%3A72072%3A122145867',
    '_ct_session_id': '122145867',
    '_ct_site_id': '72072',
    'call_s': '___js5ahoyi.1753352777.122145867.449093:1267841|2___',
    '_ct': '3000000000085636699',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://kino-kvartal.ru/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'kino-kvartal.ru',
    # 'cookie': 'session=c02def3adb1df7a7c2afc03f8957cc113038213a736bb7dda7f28cce4f6a4bd9; _ym_uid=174411617377976528; _ym_d=1753350977; _ym_isad=2; cted=modId%3Djs5ahoyi%3Bya_client_id%3D174411617377976528; _ym_visorc=w; _ct_ids=js5ahoyi%3A72072%3A122145867; _ct_session_id=122145867; _ct_site_id=72072; call_s=___js5ahoyi.1753352777.122145867.449093:1267841|2___; _ct=3000000000085636699; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae',
}

params = {
    'project_id': 'dccdada0-9c61-4e54-85aa-cdf4802414c0',
    'status': 'free',
    'offset': '0',
    'limit': '16',
    'order_by': 'price',
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

session = requests.Session()

while True:

    response = session.get(
        'https://kino-kvartal.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
        timeout=None
    )

    items = response.json()


    for i in items:

        url = ''
        developer = "Киноквартал"
        project = 'Киноквартал'
        korpus = i['building_int_number']
        type = 'Квартиры'
        if i['finishing_type'] == 'no':
            finish_type = 'Без отделки'
        elif i['finishing_type'] == 'fine':
            finish_type = 'С отделкой'
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
    sleep_time = random.uniform(3, 6)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

