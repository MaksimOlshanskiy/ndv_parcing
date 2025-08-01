import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from datetime import datetime

from functions import save_flats_to_excel

cookies = {
    'tmr_lvid': 'e03afeb716bb930a5f929477c3aa10ca',
    'tmr_lvidTS': '1751012855779',
    '_ym_uid': '1751012856942661701',
    '_ym_d': '1753877594',
    '_ym_isad': '2',
    '_ga': 'GA1.1.1221661647.1753877594',
    '_ym_visorc': 'w',
    '_cmg_cssta5xp1': '1753877595',
    '_comagic_ida5xp1': '10908543906.15221940731.1753877595',
    'domain_sid': 'SSbQ2IZYnfJytRHce3mZo%3A1753877595795',
    'tmr_detect': '0%7C1753877596193',
    'scbsid_old': '2746015342',
    'session': 'b31a2c1a9cf79bd57e6b88a27223e70798c47656155c40d1ffc716b7f8014b6a',
    'sma_session_id': '2375670920',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d9eadf726ef363c2da5f2fae87307f58%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1753877612777',
    'SCBFormsAlreadyPulled': 'true',
    '_ga_5FJ6N7LPL7': 'GS2.1.s1753877594$o1$g1$t1753877616$j38$l0$h0',
    'sma_index_activity': '1479',
    'SCBindexAct': '1279',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://accenty.ru/flats?offset=14&limit=16',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'accenty.ru',
    # 'cookie': 'tmr_lvid=e03afeb716bb930a5f929477c3aa10ca; tmr_lvidTS=1751012855779; _ym_uid=1751012856942661701; _ym_d=1753877594; _ym_isad=2; _ga=GA1.1.1221661647.1753877594; _ym_visorc=w; _cmg_cssta5xp1=1753877595; _comagic_ida5xp1=10908543906.15221940731.1753877595; domain_sid=SSbQ2IZYnfJytRHce3mZo%3A1753877595795; tmr_detect=0%7C1753877596193; scbsid_old=2746015342; session=b31a2c1a9cf79bd57e6b88a27223e70798c47656155c40d1ffc716b7f8014b6a; sma_session_id=2375670920; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%22d9eadf726ef363c2da5f2fae87307f58%22%5D; SCBporogAct=5000; SCBstart=1753877612777; SCBFormsAlreadyPulled=true; _ga_5FJ6N7LPL7=GS2.1.s1753877594$o1$g1$t1753877616$j38$l0$h0; sma_index_activity=1479; SCBindexAct=1279',
}

params = {
    'project_id': '5301ae32-6f20-4f6d-aace-09f108e6ec46',
    'status': 'free',
    'offset': '0',
    'limit': '16',
    'order_by': 'price',
}





flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = session.get(
        'https://accenty.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''


        date = datetime.now()
        project = i['project_name']


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
        developer = "PLUS Development"
        okrug = ''
        district = ''
        adress = i['address']
        eskrou = ''
        korpus = i['building_int_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['type'] == 'flat':
            type = 'Квартира'
        else:
            type = i['type']
        if i['finishing_type'] == "pre_fine":
            finish_type = 'Предчистовая'
        elif i['finishing_type'] == "fine":
            finish_type = 'С отделкой'
        else:
            finish_type = 'Без отделки'

        room_count = i['rooms']

        area = float(i['total_area'])

        price_per_metr = ''
        old_price = i['old_price']
        discount = ''
        price_per_metr_new = ''
        price = i["price"]

        section = int(i['section_number'])
        floor = int(i['floor_number'])
        flat_number = i['number']



        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break
    params["offset"] = int(params["offset"]) + 16
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)