'''
В будущем проверять корпуса, пока только 1.1 в продаже, появятся другие
'''


import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from Developer_dict import developer_dict, name_dict
from functions import save_flats_to_excel

import requests

cookies = {
    'mk_client_id': 'ae0313f465445845',
    '_ym_uid': '1780173717371636988',
    '_ym_d': '1780173717',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://mega-kashira.ru/chess/',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 'cookie': 'mk_client_id=ae0313f465445845; _ym_uid=1780173717371636988; _ym_d=1780173717; _ym_isad=2; _ym_visorc=w',
}



parsed_flat_count = 0
flats = []


response = requests.get('https://mega-kashira.ru/data/apartments.json', cookies=cookies, headers=headers)

print(response.status_code)

items = response.json()
# total_flat_count = response.json()["count"]



for i in items:

    if i['status'] == 'sold':
        continue

    url = ''
    developer = "РЕКОНСТРУКЦИЯ"
    project = "Мега Кварталы"
    korpus = '2. 1 этап. 1 очередь'
    type = 'Квартиры'
    finish_type = "Без отделки"
    room_count = i["rooms"]
    area = float(i["area"])
    try:
        price = int(i["price_special_sell"])
    except:
        price = ''
    try:
        old_price = int(i["price_sell"])
    except:
        old_price = ''
    if not old_price:
        old_price = price
    section = i["section"]
    try:
        floor = int(i["floor"])
    except:
        floor = ''
    flat_number = i['number']
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
    date = datetime.now().date()

    print(
        f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type}, срок сдачи: {srok_sdachi}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
              mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, url, comment, developer, okrug, district, adress, eskrou, korpus,
              konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

save_flats_to_excel(flats, project, developer)

