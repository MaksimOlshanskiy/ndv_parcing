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
    'session': 'a62ca16955af823f6a40e4d3bee04337d9f92091589d7be16357d4bad5e53bf5',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://ostov.group',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://ostov.group/flats?complex_id=8533232b-7850-4360-a5f5-eacc0490dd95&complex_id=92d0965e-86be-4cba-a64e-0715b5146854&complex_id=67e3ded6-d11b-4e81-b332-a89a4199ecc8',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'x-host': 'ostov.group',
    # 'cookie': 'session=a62ca16955af823f6a40e4d3bee04337d9f92091589d7be16357d4bad5e53bf5',
}

json_data = {
    'project_id': '570f6e16-c68f-439c-9963-6e5b32b35356',
    'filters': [
        {
            'id': 'status',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                'free',
            ],
        },
        {
            'id': 'complex_id',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                '8533232b-7850-4360-a5f5-eacc0490dd95',
                '92d0965e-86be-4cba-a64e-0715b5146854',
                '67e3ded6-d11b-4e81-b332-a89a4199ecc8',
            ],
        },
    ],
    'order_by': [
        'price',
    ],
    'limit': 16,
    'offset': 15,
}

flats = []
date = datetime.now().date()

while True:

    response = requests.post(
        'https://ostov.group/api/realty-filter/custom/real-estates',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    items = response.json()

    for i in items:

        if not i['status'] == 'free':
            continue

        url = ''
        developer = "Остов"
        project = i['project_name'].replace('Авиатор-2', 'Авиатор').replace('Школьный', 'Школьный (сму-29)')
        korpus = i['building_number']
        if project == 'Авиатор':
            korpus = i['building_number'].replace('Корпус ', '')[0]
        if project == 'Школьный (сму-29)':
            korpus = '1'
        if project == 'Арт':
            korpus = '1'
        type = 'Квартиры'
        finish_type = i['finishing_type']
        room_count = i['rooms']
        try:
            area = float(i['total_area'])
        except:
            area = ''
        try:
            old_price = i['old_price']
        except:
            old_price = ''
        price = i['price']

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
        srok_sdachi_old = i['completion_title'].replace('.', '')
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''

        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]

        flats.append(result)

    if not items:
        break
    json_data['offset'] = json_data['offset'] + 16

save_flats_to_excel(flats, project, developer, kvartirografia=False)
