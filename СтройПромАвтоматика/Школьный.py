import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from functions import save_flats_to_excel

import requests

cookies = {
    'csrf_cookie_name': 'cc3f9c5caf226d35f60f1456086378bd',
    '_ym_uid': '1744285458723468304',
    '_ym_d': '1764140961',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'ccc': 'a13eee6b347017665dc5bc9e1201469b8402af5e',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://zvnd.ru',
    'Referer': 'https://zvnd.ru/projects/zhk-vostochnyy/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'csrf_cookie_name=cc3f9c5caf226d35f60f1456086378bd; _ym_uid=1744285458723468304; _ym_d=1764140961; _ym_isad=2; _ym_visorc=w; ccc=a13eee6b347017665dc5bc9e1201469b8402af5e',
}

data = {
    'projectId': '0',
    'offset': '0',
    'filters': 'type=1&multi=1&projects%5B%5D=1&smin=20&smax=103&pmin=3%20202%20800&pmax=14%20336%20000',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://zvnd.ru/search/getObjects/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['html']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_='obj-body')
    for i in flats_soup:

        item = list(i.stripped_strings)

        url = ''
        date = datetime.date.today()
        project = 'Школьный (Стройпромавтоматика)'
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
        developer = "Стройпромавтоматика"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = item[3].replace('Корпус ', '')
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = item[0].split('-')[0]
        area = float(item[1].replace(' м²', ''))
        price_per_metr = ''
        old_price = int(item[7].replace(' ', '').replace('₽', ''))
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = item[4].replace('Секция ', '')
        floor = item[5].replace('Этаж ', '')
        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

    data['offset'] = str(int(data['offset']) + 21)
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer, kvartirografia=False)