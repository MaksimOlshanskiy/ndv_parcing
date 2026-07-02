import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'qVA6nTA8U0MDlxKqpMSV8cjGTxHLHLZc',
    'BXREALTY_BXRMN_BXMAKER_AUP_GID2': '10130471',
    'BXREALTY_BXRMN_TZ': 'Europe/Moscow',
    'tmr_lvid': '42f2f79d367f5bc6fe6069bcde90f2ed',
    'tmr_lvidTS': '1782900465789',
    '_ga': 'GA1.2.1877251873.1782900468',
    '_gid': 'GA1.2.1160427815.1782900468',
    'domain_sid': 'vRDIRimMVwrPSaYGvTII-%3A1782900469158',
    '_ym_uid': '1782900474338580634',
    '_ym_d': '1782900474',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'callibri_get_request': '1782920330245',
    'v1_referrer_callibri': '',
    'v1_data': '',
    '_gat_UA-101944776-1': '1',
    '_ga_PQXGB1TRSB': 'GS2.2.s1782920332$o4$g0$t1782920332$j60$l0$h0',
    'tmr_detect': '0%7C1782920332734',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://vysotsky.estate',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://vysotsky.estate/zhk/1252203/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=qVA6nTA8U0MDlxKqpMSV8cjGTxHLHLZc; BXREALTY_BXRMN_BXMAKER_AUP_GID2=10130471; BXREALTY_BXRMN_TZ=Europe/Moscow; tmr_lvid=42f2f79d367f5bc6fe6069bcde90f2ed; tmr_lvidTS=1782900465789; _ga=GA1.2.1877251873.1782900468; _gid=GA1.2.1160427815.1782900468; domain_sid=vRDIRimMVwrPSaYGvTII-%3A1782900469158; _ym_uid=1782900474338580634; _ym_d=1782900474; _ym_isad=2; _ym_visorc=w; callibri_get_request=1782920330245; v1_referrer_callibri=; v1_data=; _gat_UA-101944776-1=1; _ga_PQXGB1TRSB=GS2.2.s1782920332$o4$g0$t1782920332$j60$l0$h0; tmr_detect=0%7C1782920332734',
}

data = {
    'sessid': 'dc55c23e637a5a5b6a89c0440096a762',
    'action': 'get_apartments',
    'source': 'trendagent',
    'block_id': '658ba27ed42cb9487f140872',
    'filters[sessid]': 'dc55c23e637a5a5b6a89c0440096a762',
    'filters[source]': 'trendagent',
    'filters[per_page]': '20',
    'filters[page]': '1',
    'filters[block_id]': '658ba27ed42cb9487f140872',
    'filters[show_tredagent]': '',
    'filters[show_iblock]': '',
    'filters[bitrix_complex]': '77425',
    'filters[building_id]': '',
    'filters[finishing]': '',
    'filters[price_min]': '',
    'filters[price_max]': '',
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://vysotsky.estate/api/searchApartments/', params=data, cookies=cookies, headers=headers)
    print(response.status_code)
    print(response.text)


    items = response.json()['data']['apartments']
    print(items)


    for i in items:

        url = ''
        developer = "Еврофармакол"
        project = 'Sole Hill'
        korpus = i['building_name']
        type = 'Квартиры'
        finish_type = i['finishing_name']
        room_count = i['rooms']
        try:
            area = float(i['area_total'])
        except:
            area = i['area_total']

        old_price = int(i['price'].replace('.00', ''))
        price = int(i['price'].replace('.00', ''))
        section = ''
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
        date = datetime.now().date()


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break
    data['filters[page]'] = str(int(data['filters[page]']) + 20)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

