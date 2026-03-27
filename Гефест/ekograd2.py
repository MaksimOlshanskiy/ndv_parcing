import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests
from functions import save_flats_to_excel
from requests.exceptions import Timeout

cookies = {
    'session': 'd64845250344edf7596194193e65a34e9f2604550a83c5b60ff6fe0b35113318',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://xn--2-7sba2b6akh.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn--2-7sba2b6akh.xn--p1ai/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-host': 'xn--2-7sba2b6akh.xn--p1ai',
    # 'cookie': 'session=d64845250344edf7596194193e65a34e9f2604550a83c5b60ff6fe0b35113318',
}

json_data = {
    'project_id': 'b9bbde2b-8d5e-4a8f-ab26-ada7d5d21a15',
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
page_counter = 1

while True:

    try:
        response = requests.post(
            'https://xn----8sbaf9ahriysl4g.xn--p1ai/api/realty-filter/custom/real-estates',
            cookies=cookies,
            headers=headers,
            json=json_data, timeout=(5, 30))
    except:

        print("Timeout запроса, повтор...")
        time.sleep(3)
        continue

    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''
        date = datetime.date.today()
        project = 'Экоград Новый Катуар'
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
        developer = "Гефест"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['building_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        otdelka = i['finishing_type']
        if otdelka == 'no':
            otdelka = 'Без отделки'
        if not otdelka:
            otdelka = 'Без отделки'
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = i['type'].replace('flat', 'Квартиры')
        room_count = i['rooms']
        area = i['total_area']
        discount = ''
        price_per_metr = ''
        price_per_metr_new = ''
        old_price = i['old_price']
        price = i['price']
        section = i['section_number']
        floor = i['floor_number']
        flat_number = ''

        print(
            f"{project}, отделка: {otdelka}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, otdelka, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break

    print('--------------------------------------------------------------------------------')

    json_data['offset'] = json_data['offset'] + 16
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)