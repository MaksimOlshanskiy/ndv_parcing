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
    'origin': 'https://xn----8sbkbfqycr.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----8sbkbfqycr.xn--p1ai/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}

json_data = {
    'action': 'objects_list',
    'data': {
        'category': 'flat',
        'activity': 'sell',
        'page': 0,
        'filters': {
            'studio': 'null',
            'rooms': [],
            'restorations': [],
            'promos': [],
            'tags': [],
            'riser_side': [],
            'geo_city': None,
            'floors': [],
            'houses_ids': [],
            'type': None,
            'areaFrom': None,
            'areaTo': None,
            'priceFrom': None,
            'priceTo': None,
            'priceM2From': None,
            'priceM2To': None,
            'priceRentFrom': None,
            'priceRentTo': None,
            'priceRentM2From': None,
            'priceRentM2To': None,
            'status': None,
            'isHot': False,
            'isExclusive': False,
        },
        'complex_id': None,
        'house_id': 7541960,
        'orders': [],
        'complex_search': None,
        'house_search': None,
        'lazy': True,
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
        'https://api.macroserver.ru/estate/catalog/?domain=xn----8sbkbfqycr.xn--p1ai&check=8NBiG4NB0aNpg_0r2NdBKhidWwSlKbxlzPryD1GotMlHMpxa5HZYpJE7w_qWpNxgkbIetnwxNzU1NjkzODM2fDYzOGIx&type=catalog&autoshow=true&inline=true&issetJQuery=0&presmode=complex&complexid=7558785&uuid=57aa61b6-648d-4638-b136-56de8721b6b6&cookie_base64=W10%3D&time=1755693836&token=1a05b9114afb837ea70f67df7699d201/',
        headers=headers,
        json=json_data,
    )

    items = response.json()["objects"]



    for i in items:
        if i['status'] != 'available':
            continue

        url = i['id']
        developer = "Альфа Проджект"
        project = 'Идеал'
        korpus = ''
        type = 'Квартиры'
        finish_type = 'С отделкой'
        room_count = extract_digits_or_original(i['rooms'])
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['price'].replace('.0000', ''))
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
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

    if response.json()['isLastPage']:
        break
    json_data['data']['page'] += 1
    print('______________________________________________')
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

