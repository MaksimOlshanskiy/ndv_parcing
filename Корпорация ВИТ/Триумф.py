import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

import requests

from functions import save_flats_to_excel

cookies = {
    'session': '2e31cfafb8c8ae1bd49825a613b9b134b080d80ec35a2e37e0bf54ed6b6eb348',
    '_ym_uid': '1744123184975636231',
    '_ym_d': '1753352243',
    'tmr_lvid': '9d70403686a809f88ffed7e0be97ad87',
    'tmr_lvidTS': '1744123183149',
    'cted': 'modId%3Dt43gunl9%3Bya_client_id%3D1744123184975636231',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_cssta5X99': '1753352243',
    '_comagic_ida5X99': '11333060459.15556459669.1753352243',
    'domain_sid': 'EN61jaTFwmqrIUj5aoVGH%3A1753352244131',
    'tmr_detect': '0%7C1753352245581',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://triumf-pushkino.ru/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'triumf-pushkino.ru',
    # 'cookie': 'session=2e31cfafb8c8ae1bd49825a613b9b134b080d80ec35a2e37e0bf54ed6b6eb348; _ym_uid=1744123184975636231; _ym_d=1753352243; tmr_lvid=9d70403686a809f88ffed7e0be97ad87; tmr_lvidTS=1744123183149; cted=modId%3Dt43gunl9%3Bya_client_id%3D1744123184975636231; _ym_isad=2; _ym_visorc=w; _cmg_cssta5X99=1753352243; _comagic_ida5X99=11333060459.15556459669.1753352243; domain_sid=EN61jaTFwmqrIUj5aoVGH%3A1753352244131; tmr_detect=0%7C1753352245581',
}

params = {
    'project_id': 'afbd9c73-caa4-4e11-88bd-3d752d7730c8',
    'status': 'free',
    'offset': '0',
    'limit': '16',
    'order_by': 'price',
}


session = requests.Session()

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = session.get(
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
    params['offset'] = str(int(params['offset']) + 16)
    sleep_time = random.uniform(4, 7)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

