import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

from functions import save_flats_to_excel

cookies = {
    'session': 'c0e7abdbb1b0e6ebbfde455e39a5d62109751ea5cde49ff80079d9e793466d3d',
    '_ym_uid': '178293689454044835',
    '_ym_d': '1782936894',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'tmr_lvid': '6739a4f2aa6bd0d409a23b66781545ac',
    'tmr_lvidTS': '1782936895766',
    'adrdel': '1782936896105',
    'adrcid': 'Aozk9sSis1Nu-el9FQMy6AA',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1783023296136%2C%22sl%22%3A%7B%22224%22%3A1782936896136%2C%221228%22%3A1782936896136%7D%7D',
    '_cmg_cssttGbx8': '1782936897',
    '_comagic_idtGbx8': '10856946002.15027294802.1782936896',
    'domain_sid': 'J4Ir_NmeXoHmugcm8qlw9%3A1782936897351',
    'ab_id': '5b4f104bde146199025dceef57543556cd37878a',
    'tmr_detect': '0%7C1782936930094',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://ice-towers.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://ice-towers.ru/flats?order_by=price&view=cards',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'X-Host': 'ice-towers.ru',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'session=c0e7abdbb1b0e6ebbfde455e39a5d62109751ea5cde49ff80079d9e793466d3d; _ym_uid=178293689454044835; _ym_d=1782936894; _ym_isad=2; _ym_visorc=w; tmr_lvid=6739a4f2aa6bd0d409a23b66781545ac; tmr_lvidTS=1782936895766; adrdel=1782936896105; adrcid=Aozk9sSis1Nu-el9FQMy6AA; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1783023296136%2C%22sl%22%3A%7B%22224%22%3A1782936896136%2C%221228%22%3A1782936896136%7D%7D; _cmg_cssttGbx8=1782936897; _comagic_idtGbx8=10856946002.15027294802.1782936896; domain_sid=J4Ir_NmeXoHmugcm8qlw9%3A1782936897351; ab_id=5b4f104bde146199025dceef57543556cd37878a; tmr_detect=0%7C1782936930094',
}

json_data = {
    'project_id': '542d920e-79ab-4c46-a59b-8de3c282baca',
    'filters': [
        {
            'id': 'status',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                'free',
            ],
        },
    ],
    'order_by': [
        'price',
    ],
    'limit': 16,
    'offset': 0,
}


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

flats = []


while True:
    response = requests.post(
        'https://ice-towers.ru/api/realty-filter/custom/real-estates',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    print(response.status_code)
    data = response.json()
    date = datetime.now().date()

    for i in data:

        url = ''
        developer = "Град"
        project = 'ICE TOWERS'
        korpus = i['building_number']
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = i['rooms_value']
        try:
            area = i['total_area']
        except:
            area = ''
        try:
            old_price = i['old_price']
        except:
            old_price = ''
        try:
            price = i['price']
        except:
            price = ''
        if old_price == 0:
            continue
        section = i['section_number']
        try:
            floor = i['floor_number']
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
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    json_data['offset'] += 16
    if not data:
        break







save_flats_to_excel(flats, project, developer)