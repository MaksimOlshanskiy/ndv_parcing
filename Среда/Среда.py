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
    'scbsid_old': '4097698043',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'tmr_lvid': '9e4f012ecebebed395a49f5cebaaf45d',
    'tmr_lvidTS': '1779896919340',
    '_ym_uid': '1779896922913486643',
    '_ym_d': '1779896922',
    '_ymab_param': 'aY6yGECRVuaAFiOFvaWQENPgnLVUwj9B3kgo6xkgoa4_AW4_48_Y4VEbWloHePktVeNhOEyULVy0VFqqlQgCBn4GWl4',
    'SCBporogAct': '5000',
    'SCBstart': '1779896923488',
    'SCBFormsAlreadyPulled': 'true',
    '_ct': '2800000000271817636',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'c2d_widget_id': '{%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20eaf9e183769516758503%5C%22%2C%5C%22client_token%5C%22:%5C%229b45960607cabedd22f15e27e002abd5%5C%22}%22}',
    'cookieConsent': 'true',
    'ytm_page_sec_': '103',
    'SCBindexAct': '3512',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782914227684%2C%22sl%22%3A%7B%22224%22%3A1782827827684%2C%221228%22%3A1782827827684%7D%7D',
    'adrdel': '1782827828016',
    'cted': 'modId%3D5wfm9jtf%3Bya_client_id%3D1779896922913486643',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_ct_ids': '5wfm9jtf%3A67186%3A415832978',
    '_ct_session_id': '415832978',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1782829626.415832978.401330:1377235|2___',
    'domain_sid': 'uIBrVmueaGb8kYiAkJT5F%3A1782827829821',
    'sma_session_id': '2756261704',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%2269a8c60d87e15c5e811dc898ec400d63%22%2C%220bbaadf22d440f0330d4eed28458fa70%22%2C%2216b392528b52c310080354ac2f9472df%22%5D',
    'tmr_detect': '0%7C1782827830854',
    'sma_postview_ready': '1',
    'SCBindexAct': '4808',
    'sma_index_activity': '1999',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=production-57a4686e,sentry-public_key=c6b8c21885354992b64bc31165aa6673,sentry-trace_id=75be77f4a93c4a7391d5cb6080fec95b,sentry-sampled=false,sentry-sample_rand=0.2573529152571197,sentry-sample_rate=0.05',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '75be77f4a93c4a7391d5cb6080fec95b-b43b66f86f1c3d9d-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=4097698043; adrcid=A0r9KB4fc8duMUv2jPsp-tg; tmr_lvid=9e4f012ecebebed395a49f5cebaaf45d; tmr_lvidTS=1779896919340; _ym_uid=1779896922913486643; _ym_d=1779896922; _ymab_param=aY6yGECRVuaAFiOFvaWQENPgnLVUwj9B3kgo6xkgoa4_AW4_48_Y4VEbWloHePktVeNhOEyULVy0VFqqlQgCBn4GWl4; SCBporogAct=5000; SCBstart=1779896923488; SCBFormsAlreadyPulled=true; _ct=2800000000271817636; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; c2d_widget_id={%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20eaf9e183769516758503%5C%22%2C%5C%22client_token%5C%22:%5C%229b45960607cabedd22f15e27e002abd5%5C%22}%22}; cookieConsent=true; ytm_page_sec_=103; SCBindexAct=3512; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782914227684%2C%22sl%22%3A%7B%22224%22%3A1782827827684%2C%221228%22%3A1782827827684%7D%7D; adrdel=1782827828016; cted=modId%3D5wfm9jtf%3Bya_client_id%3D1779896922913486643; _ym_isad=2; _ym_visorc=b; _ct_ids=5wfm9jtf%3A67186%3A415832978; _ct_session_id=415832978; _ct_site_id=67186; call_s=___5wfm9jtf.1782829626.415832978.401330:1377235|2___; domain_sid=uIBrVmueaGb8kYiAkJT5F%3A1782827829821; sma_session_id=2756261704; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; smFpId_old_values=%5B%2269a8c60d87e15c5e811dc898ec400d63%22%2C%220bbaadf22d440f0330d4eed28458fa70%22%2C%2216b392528b52c310080354ac2f9472df%22%5D; tmr_detect=0%7C1782827830854; sma_postview_ready=1; SCBindexAct=4808; sma_index_activity=1999',
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

