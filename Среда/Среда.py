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
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769611335951%2C%22sl%22%3A%7B%22224%22%3A1769524935951%2C%221228%22%3A1769524935951%7D%7D',
    'adrdel': '1769524936318',
    'scbsid_old': '2746015342',
    'tmr_lvid': '264deae7a4cd3a9d92d563d67bdba7e6',
    'tmr_lvidTS': '1743082464542',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1769524938',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': '5wfm9jtf%3A67186%3A338612856',
    '_ct_session_id': '338612856',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1769526738.338612856.401330:1377143|2___',
    '_ct': '2800000000228306266',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cted': 'modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1769524939529',
    'tmr_detect': '0%7C1769524939710',
    'cookieConsent': 'true',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-public_key=96bd819503c5a55dbc59c84ba1c5cb3f,sentry-trace_id=5df4b25e0659f392da7c5103b65338d4,sentry-transaction=GET%20%2Fflats%2Fsreda-na-kutuzovskom,sentry-sampled=true,sentry-sample_rand=0.023243595780664483,sentry-sample_rate=1',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats/sreda-na-kutuzovskom?filtersFlat=%7B%22default%22%3A0%7D&gridType=list',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '5df4b25e0659f392da7c5103b65338d4-9ae272df2a425726-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    # 'cookie': 'adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769611335951%2C%22sl%22%3A%7B%22224%22%3A1769524935951%2C%221228%22%3A1769524935951%7D%7D; adrdel=1769524936318; scbsid_old=2746015342; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; _ym_uid=1743082465444153846; _ym_d=1769524938; _ym_isad=2; _ym_visorc=w; _ct_ids=5wfm9jtf%3A67186%3A338612856; _ct_session_id=338612856; _ct_site_id=67186; call_s=___5wfm9jtf.1769526738.338612856.401330:1377143|2___; _ct=2800000000228306266; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cted=modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1769524939529; tmr_detect=0%7C1769524939710; cookieConsent=true',
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
        try:
            old_price = round(int(i['price']) * 100 / (100-i['discount']))
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
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
        srok_sdachi = i['settlement_date']
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
    params['offset'] = str(int(params['offset']) + 500)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

