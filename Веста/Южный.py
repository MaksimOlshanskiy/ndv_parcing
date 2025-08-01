'''

нужно менять 'access_token'

'''


from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import requests

from functions import save_flats_to_excel

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
}

params = {
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'houseId': '103974',
    'limit': '10',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
    'access_token': '458a64db7d5eaac5db44ec9373d7f7174769fad23caca7c0d8576ff23120995b',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://pb2956.profitbase.ru/api/v4/json/property', params=params, headers=headers)

    items = response.json()['data']['properties']


    for i in items:

        url = ''
        developer = "Веста"
        project = 'Южный (Павловский Посад)'
        korpus = ''
        type = 'Квартиры'
        if i['attributes']['facing'] == 'нет':
            finish_type = 'Без отделки'
        else:
            finish_type = i['attributes']['facing']
        room_count = i['rooms_amount']
        try:
            area = float(i['area']['area_total'])
        except:
            area = ''
        try:
            old_price = int(i['price']['value'])
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        section = i['section']
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

    if not items:
        break
    params['offset'] = str(int(params['offset']) + 10)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

