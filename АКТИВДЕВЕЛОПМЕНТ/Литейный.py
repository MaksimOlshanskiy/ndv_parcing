"""

Прописываем максимальные номера страниц в max_page_dict

"""


import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'yvB5Jizw6csReKv41uyrHjA9ONVFj8dh',
    '_ym_uid': '1747643054601740949',
    '_ym_d': '1754549566',
    '_ym_isad': '2',
    'tmr_lvid': '68102bbf442092ef73d75c69322d23d9',
    'tmr_lvidTS': '1747643053742',
    'domain_sid': '864SoJI-pbqFHHVg6zB07%3A1754549567559',
    'tmr_detect': '0%7C1754550020500',
}

headers = {
    'accept': 'text/html, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://liteyniy.life',
    'priority': 'u=1, i',
    'referer': 'https://liteyniy.life/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=yvB5Jizw6csReKv41uyrHjA9ONVFj8dh; _ym_uid=1747643054601740949; _ym_d=1754549566; _ym_isad=2; tmr_lvid=68102bbf442092ef73d75c69322d23d9; tmr_lvidTS=1747643053742; domain_sid=864SoJI-pbqFHHVg6zB07%3A1754549567559; tmr_detect=0%7C1754550020500',
}

data = {
    'price_from': '7780000',
    'price_to': '18990000',
    'area_from': '38',
    'area_to': '108',
    'ajax_mode': 'y',
    'sort': '',
    'page': '1',
    'view_mode': 'view_table',
    'section_filters': '',
    'floor_filters': '',
    'room_filters': '',
    'house_id': '260',
}


flats = []
buildings_ids = ['13', '16']
buildings_ids_dict = {'13' : 'Литейная 18', '16' : 'Народная 15'}
max_page_dict = {'13' : '8', '16' : '11'}


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

for buildings_id in buildings_ids:
    data['section_filters'] = buildings_id
    data['page'] = '1'

    while True:

        response = requests.post(
            'https://liteyniy.life/include/mainpage/ajax_flat_choice.php',
            cookies=cookies,
            headers=headers,
            data=data,
        )
        print(response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')


        flats_soup = soup.find_all('tr')

        for i in flats_soup:

            if i.text == '№ЭтажКомнатПлощадьЦена':
                continue

            url = ''
            date = datetime.date.today()
            project = 'Литейный'
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
            developer = "АКТИВДЕВЕЛОПМЕНТ"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = buildings_ids_dict.get(data['section_filters'])
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            finish_type = 'Без отделки'
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартиры'
            room_count = str(i.text.split('\n')[3])
            area = float(i.text.split('\n')[4].replace(' м2', ''))
            old_price = int(i.text.split('\n')[5].replace(' р.', '').replace(' ', ''))
            discount = ''
            price_per_metr = ''
            price_per_metr_new = ''
            price = ''
            section = ''
            floor = ''
            flat_number = ''

            print(
                f"{project}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv,
                      klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)


        print('--------------------------------------------------------------------------------')


        max_page = max_page_dict.get(data['section_filters'])
        data['page'] = str(int(data['page']) + 1)
        print(data['page'])
        print(max_page)
        if data['page'] == max_page:
            break

        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)