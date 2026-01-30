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
    'session': 'badef3b7e2815e8958652b032509f632259b3d487ac8506d3e550cbde4ede710',
    '_ym_uid': '1748431749359850676',
    '_ym_d': '1753886480',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_cssts_GL1': '1753886481',
    '_comagic_ids_GL1': '9668485157.13685749282.1753886480',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://xn--80afccr4aeu.xn--b1agpqkk.xn--p1ai/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'xn--80afccr4aeu.xn--b1agpqkk.xn--p1ai',
    # 'cookie': 'session=badef3b7e2815e8958652b032509f632259b3d487ac8506d3e550cbde4ede710; _ym_uid=1748431749359850676; _ym_d=1753886480; _ym_isad=2; _ym_visorc=w; _cmg_cssts_GL1=1753886481; _comagic_ids_GL1=9668485157.13685749282.1753886480',
}

params = {
    'project_id': '799f300e-ca5f-49aa-9541-f0d38f312e49',
    'status': 'free',
    'offset': '0',
    'limit': '16',
}




flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = session.get(
        'https://xn--80afccr4aeu.xn--b1agpqkk.xn--p1ai/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''


        date = datetime.now()
        project = 'Одинград. Квартал семейный'


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
        developer = "Вектор"
        okrug = ''
        district = ''
        adress = i['address']
        eskrou = ''
        korpus = i['building_int_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = i['completion_title']
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