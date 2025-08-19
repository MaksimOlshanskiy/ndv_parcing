'''

Проверяем сайт https://afi-park.ru/param/ на количество предложений, вписываем это число в переменную count_of_flats
Часть квартир снимается с неопределённой отделкой. Это не точно, но вроде как это квартиры без отделки.
Они выгружаются как без отделки.

'''


count_of_flats = 450

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
    'PHPSESSID': 'F7L59dlf7VkWnKp7Vo32KnePo2pBhQ7j',
    '_cmg_csstS0cfD': '1755522598',
    '_comagic_idS0cfD': '11024933896.15356351591.1755522598',
    'cookies_policy': 'true',
    'cookies_promo': 'true',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://afi-park.ru/param/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'PHPSESSID=F7L59dlf7VkWnKp7Vo32KnePo2pBhQ7j; _cmg_csstS0cfD=1755522598; _comagic_idS0cfD=11024933896.15356351591.1755522598; cookies_policy=true; cookies_promo=true',
}

params = {
    'PAGEN_1': '1',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while len(flats) < count_of_flats:

    response = requests.get('https://afi-park.ru/param/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    flats_soup = soup.find_all('a', class_="commercial-box newStyleBox loadMoreItem")
    for i in flats_soup:
        elements = i.find_all('div', class_="commercial-item-properties-element")
        elems = []
        for j in elements:
            if j.text != '':
                j = j.text.split('\n')
                for e in j:
                    if e != '':
                        elems.append(e)

        url = ''
        date = datetime.date.today()
        project = "Сиреневый парк"
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
        developer = "АФИ"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = elems[2]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        try:
            finish_type = i.find('div', class_='facingLabel').text
            if finish_type == 'без отделки':
                finish_type = 'Без отделки'
            elif finish_type == 'предчистовая':
                finish_type = 'Предчистовая'
            elif finish_type == 'комфорт':
                finish_type = 'С отделкой'
            elif finish_type == 'чистовая':
                finish_type = 'С отделкой'
        except:
            finish_type = 'Без отделки'
        room_count = elems[8]
        area = float(elems[4].replace('м²', ''))
        price_per_metr = ''
        old_price = int(i.find('div', class_='G-align-center').text.split('\n')[3].replace(' ', '').replace('₽', ''))
        discount = ''
        price_per_metr_new = ''
        price = int(i.find('div', class_='G-align-center').text.split('\n')[1].replace(' ', '').replace('₽', ''))
        section = ''
        floor = ''
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

    params['PAGEN_1'] = str(int(params['PAGEN_1']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)