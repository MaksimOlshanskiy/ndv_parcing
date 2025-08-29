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
    'session': 'ec50441af31aaf598e7619664d36e35b73bc893675c799cf75c1f07e817bebdc',
    '_ym_uid': '1756104893634256962',
    '_ym_d': '1756104893',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dm32s11lc%3Bya_client_id%3D1756104893634256962',
    '_ct_ids': 'm32s11lc%3A63521%3A292794777',
    '_ct_session_id': '292794777',
    '_ct_site_id': '63521',
    '_ct': '2600000000199312855',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'call_s': '___m32s11lc.1756106733.292794777.357572:1133105|2___',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://rigahills.ru/flats?offset=14&limit=15',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-host': 'rigahills.ru',
    # 'cookie': 'session=ec50441af31aaf598e7619664d36e35b73bc893675c799cf75c1f07e817bebdc; _ym_uid=1756104893634256962; _ym_d=1756104893; _ym_isad=2; _ym_visorc=w; cted=modId%3Dm32s11lc%3Bya_client_id%3D1756104893634256962; _ct_ids=m32s11lc%3A63521%3A292794777; _ct_session_id=292794777; _ct_site_id=63521; _ct=2600000000199312855; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; call_s=___m32s11lc.1756106733.292794777.357572:1133105|2___',
}


params = {
    'project_id': '3933e790-9a3e-47a7-8d25-2f0c1eb6440b',
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
        'https://rigahills.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    items = response.json()


    for i in items:

        url = ''
        developer = "Юнион"
        project = 'Riga Hills'
        korpus = i['building_int_number']
        type = i['type'].replace('flat', 'Квартиры')
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
            price = int(i['price'])
            if old_price == '0':
                old_price = price
                price = 0
            if not old_price and not price:
                continue
        except:
            old_price = ''
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
    sleep_time = random.uniform(1, 2)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

