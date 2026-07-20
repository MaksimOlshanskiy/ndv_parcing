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
    '_ym_uid': '1751363186277125085',
    '_ym_d': '1770968425',
    'scbsid_old': '2746015342',
    '_ym_isad': '2',
    'sma_session_id': '2636194413',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'smFpId_old_values': '%5B%22ab19ac2380782ae239d725bfec8e9f49%22%2C%22cd14d52d59b08c237e2004225d23c665%22%5D',
    '_ym_visorc': 'w',
    '_cmg_csstS0cfD': '1773405616',
    '_comagic_idS0cfD': '12376477526.16918849771.1773405616',
    'sma_index_activity': '4293',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=4558711618e8058ec7b0a8ae88af8a8c4fd7ddea,sentry-public_key=7a3626c309604a21a5401d935bf3f706,sentry-trace_id=30d64c97457b411695156aac03d40489,sentry-transaction=%2Fflat,sentry-sampled=true,sentry-sample_rand=0.8460625889659479,sentry-sample_rate=1',
    'priority': 'u=1, i',
    'referer': 'https://afi-development.com/flat?sortBy=price&sortOrder=asc&page=6',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '30d64c97457b411695156aac03d40489-a45e1171e4d6c88d-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1751363186277125085; _ym_d=1770968425; scbsid_old=2746015342; _ym_isad=2; sma_session_id=2636194413; SCBfrom=https%3A%2F%2Fyandex.ru%2F; smFpId_old_values=%5B%22ab19ac2380782ae239d725bfec8e9f49%22%2C%22cd14d52d59b08c237e2004225d23c665%22%5D; _ym_visorc=w; _cmg_csstS0cfD=1773405616; _comagic_idS0cfD=12376477526.16918849771.1773405616; sma_index_activity=4293',
}
# подставлял айди из project_dict по очереди
params = {
'project': '3b13c636-89c5-11e8-83fb-0cc47aaa4272',
    'type': 'Коммерческое помещение',
    'sortBy': 'price',
    'sortOrder': 'asc',
    'page': '1',
}


project_dict = {
'b4932c9a-caae-11e7-83fb-0cc47aaa4272' : 'Резиденции архитекторов',
"418527a9-56bd-11eb-a9ed-0cc47aaa4272" : "Afi Tower",
"1cc7991d-cb9b-11e7-83fb-0cc47aaa4272" : "Одинбург",
"3b13c636-89c5-11e8-83fb-0cc47aaa4272" : "Сиреневый парк"
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:


    try:
        response = requests.get('https://afi-development.com/api/commerce', params=params, cookies=cookies, headers=headers, timeout=(5, 30))
    except:

        print("Timeout запроса, повтор...")
        time.sleep(3)
        continue

    print(response.status_code)
    items = response.json()["items"]

    for i in items:

        url = ''
        date = datetime.date.today()
        project = project_dict.get(i['project_uid'])
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
        developer = "AFI"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['korpus_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        otdelka = i['finishing_type'].replace('Комфорт', 'С отделкой')
        if not otdelka:
            otdelka = 'Без отделки'
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = i['type'].replace('Квартира', 'Квартиры')
        room_count = i['room_count']
        area = i['square']
        discount = ''
        price_per_metr = ''
        price_per_metr_new = ''
        old_price = i['total_cost']
        price = i['total_cost_discounted']
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

    params['page'] = str(int(params['page']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)