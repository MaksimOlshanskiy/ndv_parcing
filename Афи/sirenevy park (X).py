'''

Проверяем сайт https://afi-park.ru/param/ на количество предложений, вписываем это число в переменную count_of_flats
Часть квартир снимается с неопределённой отделкой. Это не точно, но вроде как это квартиры без отделки.
Они выгружаются как без отделки.

'''


count_of_flats = 342

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
    'PHPSESSID': 'eUZ3RC66imxPVZ6vbllRqUNx8cO31biE',
    '_cmg_csstS0cfD': '1758704848',
    '_comagic_idS0cfD': '11249979726.15617038936.1758704848',
    '_ym_uid': '1742816888674822329',
    '_ym_d': '1758704849',
    '_ym_isad': '2',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Bx-ajax': 'true',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://afi-park.ru',
    'Referer': 'https://afi-park.ru/param/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'PHPSESSID=eUZ3RC66imxPVZ6vbllRqUNx8cO31biE; _cmg_csstS0cfD=1758704848; _comagic_idS0cfD=11249979726.15617038936.1758704848; _ym_uid=1742816888674822329; _ym_d=1758704849; _ym_isad=2',
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
    flats_soup = soup.find_all('div', class_="commercial-box newStyleBox")

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
            finish_type = i.find('div', class_='facingLabel').text.strip()
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
        try:
            old_price = int(i.find('div', class_='G-align-center').text.split('\n')[4].replace(' ', '').replace('₽', ''))
        except:
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(i.find('div', class_='G-align-center').text.split('\n')[2].replace(' ', '').replace('₽', ''))
        except:
            price = ''
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