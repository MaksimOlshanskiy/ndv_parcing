'''

по очереди по каждому дому 'house_id'

'''

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://xn----jtbbfggcdyc3aqvm.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----jtbbfggcdyc3aqvm.xn--p1ai/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
}

json_data = {
    'action': 'objects_list',
    'data': {
        'category': 'flat',
        'house_id': 7750570,
        'activity': 'sell',
        'cabinetMode': False,
    },
    'auth_token': None,
    'locale': None,
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://api.macroserver.ru/estate/catalog/?domain=xn----jtbbfggcdyc3aqvm.xn--p1ai&check=O4XxZ3x_IwtiWW_h90AJNXusswcJnvp7OPO2BEGWq6zcougpDlKAwUg6ZDy8bffGuZmpn4WpWqD6EHwxNzU4ODg4MDM5fDQ5MDFi&type=catalog&inline=true&issetJQuery=1&uuid=0c26cc2f-e737-48af-97e6-153cc2858eaa&cookie_base64=eyJfeW1fdWlkIjoiMTc0NDI4Mjg0Mzk5NzE4NzQ0MiJ9&time=1758888039&token=ad930a9128a289defa2e25b4021067e7/',
        headers=headers,
        json=json_data,
    )
    print(response.status_code)

    items = response.json()["objects"]



    for i in items:
        if i['status'] == 'booked':
            continue

        url = i['id']
        developer = "РКП"
        project = 'Фрунзенский'
        korpus = ''
        type = 'Квартиры'
        finish_type = 'С отделкой'
        room_count = extract_digits_or_original(i['rooms'])
        try:
            area = float(i['estate']['estate_area'])
        except:
            area = ''
        try:
            old_price = int(i['estate']['estate_price'].replace('.0000', ''))
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        section = ''
        try:
            floor = int(i['estate']['estate_floor'])
        except:
            floor = ''
        flat_number = ''

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
            f"{project}, {url}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if response.json()['isLastPage']:
        break
    else:
        json_data['data']['page'] += 1
        sleep_time = random.uniform(1, 5)
        time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

