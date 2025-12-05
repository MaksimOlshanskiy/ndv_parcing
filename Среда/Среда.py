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
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%229d3c150d063b8304ca161a15bac1d838%22%5D',
    '_ym_uid': '1743082465444153846',
    '_ym_d': '1762787006',
    'SCBstart': '1762787006207',
    '_ct': '2800000000198769450',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'SCBFormsAlreadyPulled': 'true',
    'c2d_widget_id': '{%221276926d2afb25be0c72792411b38dca%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20dd871de838752375b1ea%5C%22%2C%5C%22client_token%5C%22:%5C%2241fc29bf3518bd3eb38a06e58f06a242%5C%22}%22}',
    'cookieConsent': 'true',
    'SCBindexAct': '2035',
    '__js_p_': '535,86400,1,0,0',
    '__jhash_': '935',
    '__jua_': 'Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36',
    '__hash_': 'b091d93477f2398887a78334b369deb4',
    '__lhash_': 'bf15be3fd4b6bce5a1e7a9331b5f63ea',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764831938732%2C%22sl%22%3A%7B%22224%22%3A1764745538732%2C%221228%22%3A1764745538732%7D%7D',
    'adrdel': '1764745539072',
    'cted': 'modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846',
    '_ct_ids': '5wfm9jtf%3A67186%3A307674670',
    '_ct_session_id': '307674670',
    '_ct_site_id': '67186',
    'call_s': '___5wfm9jtf.1764747340.307674670.401330:1377120|2___',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': 'rz11zN0wchT0nNAfs1mRu%3A1764745542119',
    'tmr_detect': '0%7C1764745542260',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://sreda.ru/flats/sreda-na-kutuzovskom?filtersFlat=%7B%22default%22%3A0%7D&gridType=list',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'adrcid=Ad53EZahiTy4QvZYZHYhh0Q; scbsid_old=2746015342; tmr_lvid=264deae7a4cd3a9d92d563d67bdba7e6; tmr_lvidTS=1743082464542; SCBporogAct=5000; smFpId_old_values=%5B%229d3c150d063b8304ca161a15bac1d838%22%5D; _ym_uid=1743082465444153846; _ym_d=1762787006; SCBstart=1762787006207; _ct=2800000000198769450; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; SCBFormsAlreadyPulled=true; c2d_widget_id={%221276926d2afb25be0c72792411b38dca%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20dd871de838752375b1ea%5C%22%2C%5C%22client_token%5C%22:%5C%2241fc29bf3518bd3eb38a06e58f06a242%5C%22}%22}; cookieConsent=true; SCBindexAct=2035; __js_p_=535,86400,1,0,0; __jhash_=935; __jua_=Mozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F142.0.0.0%20Safari%2F537.36; __hash_=b091d93477f2398887a78334b369deb4; __lhash_=bf15be3fd4b6bce5a1e7a9331b5f63ea; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764831938732%2C%22sl%22%3A%7B%22224%22%3A1764745538732%2C%221228%22%3A1764745538732%7D%7D; adrdel=1764745539072; cted=modId%3D5wfm9jtf%3Bya_client_id%3D1743082465444153846; _ct_ids=5wfm9jtf%3A67186%3A307674670; _ct_session_id=307674670; _ct_site_id=67186; call_s=___5wfm9jtf.1764747340.307674670.401330:1377120|2___; _ym_isad=2; _ym_visorc=w; domain_sid=rz11zN0wchT0nNAfs1mRu%3A1764745542119; tmr_detect=0%7C1764745542260',
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

