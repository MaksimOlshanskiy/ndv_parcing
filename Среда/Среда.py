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
    '__js_p_': '530,86400,1,0,0',
    '__jhash_': '227',
    '__jua_': 'Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F138.0.0.0%20Safari%2F537.36',
    '__hash_': 'd6b2419ab0684ef59792d0aa8e6742f4',
    '__lhash_': '2224f29c577a35592fdfc3c250e054ec',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753776935906%2C%22sl%22%3A%7B%22224%22%3A1753690535906%2C%221228%22%3A1753690535906%7D%7D',
    'adrdel': '1753690536253',
    '_ga_CW8DX22VWK': 'GS2.1.s1753690537$o1$g0$t1753690537$j60$l0$h0',
    '_ga': 'GA1.1.970088777.1753690538',
    'tmr_lvid': '264deae7a4cd3a9d92d563d67bdba7e6',
    'tmr_lvidTS': '1743082464542',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1753690539',
    'scbsid_old': '2746015342',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': '5wfm9jtf%3A67186%3A241297163',
    '_ct_session_id': '241297163',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1753692337.241297163.401330:1377215|2___',
    '_ct': '2800000000162151209',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'tmr_detect': '0%7C1753690540182',
    'cted': 'modId%3D5wfm9jtf%3Bclient_id%3D970088777.1753690538%3Bya_client_id%3D1743082465444153846',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1753690541119',
    'cookieConsent': 'true',
    'sma_session_id': '2373062359',
    'SCBfrom': 'https%3A%2F%2Fsreda.ru%2Fflats%3FfiltersFlat%3D%257B%2522default%2522%253A0%252C%2522block_id_list%2522%253A%255B%25222192%2522%255D%257D%26gridType%3Dlist',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1753690544695',
    'sma_postview_ready': '1',
    'sma_index_activity': '94',
    'SCBindexAct': '94',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats/sreda-na-kutuzovskom?filtersFlat=%7B%22default%22%3A0%7D&gridType=list&utm_source=google.com&utm_medium=organic&utm_campaign=google.com&utm_referrer=google.com',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '__js_p_=530,86400,1,0,0; __jhash_=227; __jua_=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F138.0.0.0%20Safari%2F537.36; __hash_=d6b2419ab0684ef59792d0aa8e6742f4; __lhash_=2224f29c577a35592fdfc3c250e054ec; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753776935906%2C%22sl%22%3A%7B%22224%22%3A1753690535906%2C%221228%22%3A1753690535906%7D%7D; adrdel=1753690536253; _ga_CW8DX22VWK=GS2.1.s1753690537$o1$g0$t1753690537$j60$l0$h0; _ga=GA1.1.970088777.1753690538; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; _ym_uid=1743082465444153846; _ym_d=1753690539; scbsid_old=2746015342; _ym_isad=2; _ym_visorc=w; _ct_ids=5wfm9jtf%3A67186%3A241297163; _ct_session_id=241297163; _ct_site_id=67186; call_s=___5wfm9jtf.1753692337.241297163.401330:1377215|2___; _ct=2800000000162151209; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; tmr_detect=0%7C1753690540182; cted=modId%3D5wfm9jtf%3Bclient_id%3D970088777.1753690538%3Bya_client_id%3D1743082465444153846; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1753690541119; cookieConsent=true; sma_session_id=2373062359; SCBfrom=https%3A%2F%2Fsreda.ru%2Fflats%3FfiltersFlat%3D%257B%2522default%2522%253A0%252C%2522block_id_list%2522%253A%255B%25222192%2522%255D%257D%26gridType%3Dlist; SCBnotShow=-1; smFpId_old_values=%5B%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D; SCBporogAct=5000; SCBstart=1753690544695; sma_postview_ready=1; sma_index_activity=94; SCBindexAct=94',
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

