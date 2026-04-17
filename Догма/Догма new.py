import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://dogma.ru',
    'priority': 'u=1, i',
    'referer': 'https://dogma.ru/',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
}

json_data = {
    'type': 1,
    'statuses': [
        2,
    ],
    'order': {
        'field': 'order',
        'type': 'asc',
    },
    'project_ids': [
        1,
        2,
    ],
    'cities_id': [],
    'rooms': [],
    'letter_ids': [],
    'deadlines': [],
    'object_tags': [],
    'costs': [
        4839435,
        26699760,
    ],
    'areas': [
        17.63,
        101.52,
    ],
    'floors': [
        2,
        25,
    ],
    'ceiling_heights': [
        0,
        2.72,
    ],
    'limit': 12,
    'offset': 0,
    'group_by': '',
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://service.dogma.ru/api/layouts-filter/v4/objects/filter', headers=headers, json=json_data)
    print(response.status_code)
    items = response.json()['data']['objects']
    if not items:
        break

    for i in items:


        url = ''
        developer = "Догма"
        project = i['project_name']
        korpus = i['letter_name']
        section = ''
        if i['type'] == 1:
            type = 'Квартиры'

        try:
            finish_type = i['finish_types'].replace('Чистовая', 'С отделкой').replace('Черновая', 'Предчистовая')
        except:
            finish_type = 'Без отделки'
        room_count = i['room']
        flat_number = ''
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['cost'])
        except:
            old_price = ''
        try:
            price = int(i['cost_sale'])
        except:
            price = ''
        try:
            floor = i['floor']
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
        try:
            srok_sdachi_old = i['construction_deadline']
        except:
            srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''


        print(
            f"{project}, {url}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type}, срок сдачи: {srok_sdachi_old}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)


    json_data['offset'] = json_data['offset'] + json_data['limit']
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

