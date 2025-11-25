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
    '_ym_uid': '1744283513806407615',
    '_ym_d': '1762783264',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstpyx3O': '1762783265',
    '_comagic_idpyx3O': '11586467251.16005647306.1762783264',
    'session': '049c62211fe118af690a73f72df4fa841368309db7895a96e86bc4fe6bde40e1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://novie-ostrovtzi.ru',
    'priority': 'u=1, i',
    'referer': 'https://novie-ostrovtzi.ru/flats',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-host': 'novie-ostrovtzi.ru',
    # 'cookie': '_ym_uid=1744283513806407615; _ym_d=1762783264; _ym_isad=2; _ym_visorc=w; _cmg_csstpyx3O=1762783265; _comagic_idpyx3O=11586467251.16005647306.1762783264; session=049c62211fe118af690a73f72df4fa841368309db7895a96e86bc4fe6bde40e1',
}

json_data = {
    'project_id': 'a2a4fd3d-040a-42b7-931f-c22f9a140507',
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
    'order_by': None,
    'limit': 16,
    'offset': 0,
}






flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = requests.post(
        'https://novie-ostrovtzi.ru/api/realty-filter/custom/real-estates',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''


        date = datetime.now()
        project = 'Новые Островцы'


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
        developer = "РТД Групп"
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
    json_data["offset"] = int(json_data["offset"]) + 16
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)