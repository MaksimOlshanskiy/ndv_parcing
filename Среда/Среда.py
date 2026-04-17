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
    'scbsid_old': '2746015342',
    'tmr_lvid': '264deae7a4cd3a9d92d563d67bdba7e6',
    'tmr_lvidTS': '1743082464542',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1769524938',
    '_ct': '2800000000228306266',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cookieConsent': 'true',
    '_ymab_param': '7n3oyHKYwV4KvgQquj7MRR5mx1pzRg1g_BfyqE6CNsisLjhJHVZXwDweDHNT2PKBhziRhN2BAA4zdG0p8a6n_DRCTOk',
    'SCBporogAct': '5000',
    'SCBstart': '1772004104519',
    'SCBFormsAlreadyPulled': 'true',
    'c2d_widget_id': '{%221276926d2afb25be0c72792411b38dca%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20e5875d495d7fa049b2a2%5C%22%2C%5C%22client_token%5C%22:%5C%22a1bb3f42109ccb271df048b4d5e741dc%5C%22}%22%2C%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20f75e4028295bdb377648%5C%22%2C%5C%22client_token%5C%22:%5C%2284ef7eb52c9470ca7c469d5900d7e465%5C%22}%22}',
    'smFpId_old_values': '%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%2C%22a7bf202eec91b0745bd47729841d1c7d%22%2C%22cd14d52d59b08c237e2004225d23c665%22%2C%22ab19ac2380782ae239d725bfec8e9f49%22%5D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1775892794217%2C%22sl%22%3A%7B%22224%22%3A1775806394217%2C%221228%22%3A1775806394217%7D%7D',
    'adrdel': '1775806394241',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
    'sma_session_id': '2665703107',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'cted': 'modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846',
    'SCBnotShow': '-1',
    '_ct_ids': '5wfm9jtf%3A67186%3A379886850',
    '_ct_session_id': '379886850',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1775808195.379886850.401330:1377051|2___',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1775806395836',
    'sma_postview_ready': '1',
    'tmr_detect': '0%7C1775806397888',
    'ytm_page_sec_': '50',
    'sma_index_activity': '1628',
    'SCBindexAct': '745',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=production-f2c01e23,sentry-public_key=c6b8c21885354992b64bc31165aa6673,sentry-trace_id=65978104b26b4975a5fbd24ded8aadc2,sentry-sampled=true,sentry-sample_rand=0.5447015417149789,sentry-sample_rate=1',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '65978104b26b4975a5fbd24ded8aadc2-9e92d51ff69ab53a-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': 'adrcid=Ad53EZahiTy4QvZYZHYhh0Q; scbsid_old=2746015342; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; _ym_uid=1743082465444153846; _ym_d=1769524938; _ct=2800000000228306266; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cookieConsent=true; _ymab_param=7n3oyHKYwV4KvgQquj7MRR5mx1pzRg1g_BfyqE6CNsisLjhJHVZXwDweDHNT2PKBhziRhN2BAA4zdG0p8a6n_DRCTOk; SCBporogAct=5000; SCBstart=1772004104519; SCBFormsAlreadyPulled=true; c2d_widget_id={%221276926d2afb25be0c72792411b38dca%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20e5875d495d7fa049b2a2%5C%22%2C%5C%22client_token%5C%22:%5C%22a1bb3f42109ccb271df048b4d5e741dc%5C%22}%22%2C%223078a0f3605e4fd6d146869b6cc7a5b5%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20f75e4028295bdb377648%5C%22%2C%5C%22client_token%5C%22:%5C%2284ef7eb52c9470ca7c469d5900d7e465%5C%22}%22}; smFpId_old_values=%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%2C%22a7bf202eec91b0745bd47729841d1c7d%22%2C%22cd14d52d59b08c237e2004225d23c665%22%2C%22ab19ac2380782ae239d725bfec8e9f49%22%5D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1775892794217%2C%22sl%22%3A%7B%22224%22%3A1775806394217%2C%221228%22%3A1775806394217%7D%7D; adrdel=1775806394241; _ym_visorc=b; _ym_isad=2; sma_session_id=2665703107; SCBfrom=https%3A%2F%2Fyandex.ru%2F; cted=modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846; SCBnotShow=-1; _ct_ids=5wfm9jtf%3A67186%3A379886850; _ct_session_id=379886850; _ct_site_id=67186; call_s=___5wfm9jtf.1775808195.379886850.401330:1377051|2___; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1775806395836; sma_postview_ready=1; tmr_detect=0%7C1775806397888; ytm_page_sec_=50; sma_index_activity=1628; SCBindexAct=745',
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

