import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'session': '90fc15d235ce6603826c0c0e4f68f6185cec1def6d9e399bbb6914b48e9a8ed9',
    '_ym_uid': '1752221103932115499',
    '_ym_d': '1752221103',
    'roistat_visit': '140277',
    'roistat_first_visit': '140277',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit',
    '___dc': '5787f38d-071a-46a3-83a6-d5146cd78335',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://u2.moscow/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'u2.moscow',
    # 'cookie': 'session=90fc15d235ce6603826c0c0e4f68f6185cec1def6d9e399bbb6914b48e9a8ed9; _ym_uid=1752221103932115499; _ym_d=1752221103; roistat_visit=140277; roistat_first_visit=140277; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; _ym_isad=2; _ym_visorc=w; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit; ___dc=5787f38d-071a-46a3-83a6-d5146cd78335',
}

params = {
    'project_id': '75693214-1a5e-49b9-a1d0-a5376edf431d',
    'status': 'free',
    'offset': '0',
    'limit': '16',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

session = requests.Session()

while True:

    response = session.get(
        'https://u2.moscow/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    items = response.json()

    for i in items:

        url = ''
        developer = "Точно"
        project = 'U2'
        korpus = i['building_number']
        section = i['section_number']

        if i['type'] == 'flat':
            type = 'Квартиры'
        else:
            type = i['type']

        if not i['finishing_type']:
            finish_type = 'Без отделки'
        else:
            finish_type = i['finishing_type']
        if i['rooms_title'] == '0':
            room_count = 'Студия'
        else:
            room_count = i['rooms_title']
        if i['is_euro']:
            room_count += 'е'
        flat_number = i['int_number']
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
        try:
            floor = int(i['floor_number'])
        except:
            floor = ''


        english = 'U2'
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
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

