import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests


import requests

import requests

from functions import save_flats_to_excel

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://glorax.com',
    'priority': 'u=1, i',
    'referer': 'https://glorax.com/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-session-id': 'N7CYz5roSKGshTKHr4mqSJTNqV0WyzmeZc6R7fGH',
}

params = {
    "page": 1,
    "perPage": 15,
    "order": "price",
    "filter[type]": "apartment",
    "filter[project]": "glorax-premium-belorusskaya",
    "filter[withReserved]": "false"
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    response = requests.get('https://glorax-api-dev.city-digital.ru/api/v1/filter/lots', params=params, headers=headers)
    items = response.json()['data']

    for i in items:

        url = ''
        developer = "Glorax"
        project = i['projectName']
        korpus = i['building']
        if i['type'] == 'apartments':
            type = 'Апартаменты'
        if i['type'] == 'apartments':
            type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = i['rooms']
        try:
            area = i['square']
        except:
            area = ''
        try:
            old_price = float(i['price'])
        except:
            old_price = ''
        try:
            price = float(i['priceOffer'])
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = i['roomNum']


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
    params['page'] += 1


save_flats_to_excel(flats, project, developer)

