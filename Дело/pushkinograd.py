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
    '_ym_uid': '175585772376206796',
    '_ym_d': '1755857723',
    '_ct_ids': 'qs0dqgxt%3A70020%3A230182873',
    '_ct_session_id': '230182873',
    '_ct_site_id': '70020',
    'call_s': '___qs0dqgxt.1755859522.230182873.432809:1336152|2___',
    '_ct': '2900000000152843206',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    'ab_id': '5b6ce31ffd7178b098634c89d4b14ba407b58416',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dqs0dqgxt%3Bya_client_id%3D175585772376206796',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://pushkino-grad.ru/flats',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-host': 'pushkino-grad.ru',
    # 'cookie': '_ym_uid=175585772376206796; _ym_d=1755857723; _ct_ids=qs0dqgxt%3A70020%3A230182873; _ct_session_id=230182873; _ct_site_id=70020; call_s=___qs0dqgxt.1755859522.230182873.432809:1336152|2___; _ct=2900000000152843206; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; ab_id=5b6ce31ffd7178b098634c89d4b14ba407b58416; _ym_visorc=w; cted=modId%3Dqs0dqgxt%3Bya_client_id%3D175585772376206796',
}

params = {
    'project_id': '73d58f3c-1035-41ef-87b8-acf90f6845b3',
    'status': 'free',
    'offset': '0',
    'limit': '14',
    'order_by': 'price',
}







flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = requests.get(
        'https://pushkino-grad.ru/api/realty-filter/residential/real-estates',
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
        developer = "Дело"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['building_int_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        if i['finishing_type'] == "white_box":
            finish_type = 'Предчистовая'
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
    params["offset"] = str(int(params["offset"]) + 14)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)