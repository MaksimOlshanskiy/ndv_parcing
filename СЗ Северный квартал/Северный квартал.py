import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel

cookies = {
    'adtech_uid': '214794ef-4622-4548-95f2-0db0cca9bd52%3Asever-kvartal.ru',
    'top100_id': 't1.7747315.2147026845.1765541465093',
    '_ym_uid': '175915455051903024',
    '_ym_d': '1765541466',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'session': 'd902384f2ef88cdbbbe400f38438f45199bf8f2a732021474648d6555cf1351d',
    't3_sid_7747315': 's1.1041147207.1765541465093.1765545407645.1.34.4.1..',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://sever-kvartal.ru',
    'priority': 'u=1, i',
    'referer': 'https://sever-kvartal.ru/flats?view=cards&offset=30&limit=16',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'x-host': 'sever-kvartal.ru',
    # 'cookie': 'adtech_uid=214794ef-4622-4548-95f2-0db0cca9bd52%3Asever-kvartal.ru; top100_id=t1.7747315.2147026845.1765541465093; _ym_uid=175915455051903024; _ym_d=1765541466; _ym_isad=2; _ym_visorc=w; session=d902384f2ef88cdbbbe400f38438f45199bf8f2a732021474648d6555cf1351d; t3_sid_7747315=s1.1041147207.1765541465093.1765545407645.1.34.4.1..',
}

json_data = {
    'project_id': 'cb7f3994-6380-4948-8aae-c3ce47e840c2',
    'order_by': None,
    'limit': 14,
    'offset': 0,
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://sever-kvartal.ru/api/realty-filter/custom/real-estates',
                             cookies=cookies,
                             headers=headers,
                             json=json_data)
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''
        developer = "СЗ Северный квартал"
        project = 'Северный квартал'
        korpus = i['building_int_number']
        section = ''
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = i['rooms']
        flat_number = ''
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
            floor = int()
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

    json_data['offset'] = str(int(json_data['offset']) + 14)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer, kvartirografia=False)

