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
    '_ym_uid': '1753709716674288185',
    '_ym_d': '1753709716',
    'kbUserID': '570629626287568637',
    'session': '980b2696790a0340388a286e49b696dc26138893825ef773e472d026242015ab',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://xn-----elchiocal7aidb7bq1d.xn--p1ai/flats',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'x-host': 'xn-----elchiocal7aidb7bq1d.xn--p1ai',
    # 'cookie': '_ym_uid=1753709716674288185; _ym_d=1753709716; kbUserID=570629626287568637; session=980b2696790a0340388a286e49b696dc26138893825ef773e472d026242015ab; _ym_isad=2; _ym_visorc=w',
}

params = {
    'project_id': '1f155aae-9cbe-43af-8a4b-f48b666d4d4e',
    'status': 'free',
    'offset': '0',
    'limit': '16',
}





flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = session.get(
        'https://xn-----elchiocal7aidb7bq1d.xn--p1ai/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''


        date = datetime.now()
        project = i['project_name']


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
        developer = "Атлантис Скай"
        okrug = ''
        district = ''
        adress = i['address']
        eskrou = ''
        korpus = i['building_int_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
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
    params["offset"] = int(params["offset"]) + 16
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")