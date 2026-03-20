import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

from functions import save_flats_to_excel

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://ostov-aviator.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://ostov-aviator.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-widget-uuid': 'e9378d39-6381-4e61-a8d2-1414e2d77ac5',
}


korpus_dict = {1234: '1', 1245: '2'}
project_id_list = ['4fb447e6-1311-4030-8a82-83d6847c9adb', '1d383371-5a9c-4715-a372-653babfe4636',
                   ]

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

flats = []
date = datetime.now().date()

for project_id in project_id_list:

    response = requests.get(f'https://widget-server.m2lab.ru/front/realtys/{project_id}',
                            headers=headers)

    items = response.json()

    for i in items:

        if not i['status'] == 'free' or i['status'] == 'reserv':
            continue
        if i['realEstateType'] != 'living':
            continue

        url = ''
        developer = "Остов"
        project = 'Авиатор'
        korpus = korpus_dict.get(i['externalIdHouse'])
        if i['realEstateType'] == 'living':
            type = 'Квартиры'
        else:
            type = i['realEstateType']
        if not i['decoration']:
            finish_type = 'Без отделки'
        else:
            finish_type = i['decoration']
        room_count = i['roomsCount']
        if room_count == 'studio':
            room_count = '0'
        try:
            area = float(i['sq'])
        except:
            area = ''
        try:
            old_price = round(float(i['price'].replace('.00', '')))
        except:
            old_price = ''
        price = ''

        section = i['section']
        try:
            floor = int(i['floor'])
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

        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]

        flats.append(result)

save_flats_to_excel(flats, project, developer, kvartirografia=False)
