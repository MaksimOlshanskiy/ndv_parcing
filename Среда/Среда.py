'''

Нужно обновлять cookie и headers

'''

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
    'c2d_widget_id': '{%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%200c8e470f8193ede1d740%5C%22%2C%5C%22client_token%5C%22:%5C%229099f98bfa0b0591e6a8aefed47d824b%5C%22}%22}',
    'scbsid_old': '16031261345',
    '_ct': '2800000000287088500',
    '_ct_client_global_id': '089407ce-d8b4-596e-88ef-eee2bfcb3172',
    'cookieConsent': 'true',
    'smFpId_old_values': '%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%2C%22d3e51c94ece420479e1f2820408383b2%22%5D',
    '_ct_ids': '5wfm9jtf%3A67186%3A426824329',
    '_ct_session_id': '426824329',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1785172138.426824329.401330:1377112|2___',
    'sma_session_id': '2787401613',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1785170339646',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'SCBindexAct': '410',
    'sma_index_activity': '610',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=production-d12414d2,sentry-public_key=c6b8c21885354992b64bc31165aa6673,sentry-trace_id=751ee3df8de59a2054042759fa1fc847,sentry-transaction=generateMetadata%20%2Flayout,sentry-sample_rand=0.5504133054508178',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats/sreda-na-kutuzovskom?filtersFlat=%7B%22default%22%3A0%7D&gridType=list',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '751ee3df8de59a2054042759fa1fc847-ad2b20104670f3e9-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    # 'cookie': 'c2d_widget_id={%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%200c8e470f8193ede1d740%5C%22%2C%5C%22client_token%5C%22:%5C%229099f98bfa0b0591e6a8aefed47d824b%5C%22}%22}; scbsid_old=16031261345; _ct=2800000000287088500; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; cookieConsent=true; smFpId_old_values=%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%2C%22d3e51c94ece420479e1f2820408383b2%22%5D; _ct_ids=5wfm9jtf%3A67186%3A426824329; _ct_session_id=426824329; _ct_site_id=67186; call_s=___5wfm9jtf.1785172138.426824329.401330:1377112|2___; sma_session_id=2787401613; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBstart=1785170339646; SCBporogAct=5000; sma_postview_ready=1; SCBindexAct=410; sma_index_activity=610',
}


params = {
    'default': '1',
    'limit': '500',
    'offset': '0',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://sreda.ru/api/flat/search', params=params, cookies=cookies, headers=headers)
    print(response.status_code)


    items = response.json()['data']['list']


    for i in items:

        url = ''
        developer = "Среда"
        project = i['name']
        korpus = i['bulk_name'].replace('Корпус', '').strip()
        type = 'Квартиры'
        if i['finish']['isFinish'] is True:
            finish_type = 'С отделкой'
        elif i['finish']['isFinish'] is True and i['finish']['furniture'] is True:
            finish_type = 'С отделкой и доп опциями'
        elif i['finish']['whiteBox'] is True:
            finish_type = 'Предчистовая'
        else:
            finish_type = 'Без отделки'
        room_count = i['rooms']
        try:
            area = float(i['area'])
        except:
            area = i['area']

        discounts = i.get('discount_on_benefits') or []
        if discounts and discounts[0].get('discount'):
            old_price = i['mortgage_informer']['benefit']['benefitPrice']
            price = int(i['price'])
        else:
            old_price = int(i['price'])
            price = old_price

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
        srok_sdachi_old = i['settlement_date']
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
    params['offset'] = str(int(params['offset']) + 500)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

