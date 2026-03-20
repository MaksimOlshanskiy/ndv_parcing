import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel

cookies = {
    '_ct': '3300000000093639509',
    '_ym_uid': '1770017467752291124',
    '_ym_d': '1773757872',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'jlticukg%3A75994%3A146807752_n376lmui%3A79278%3A75471373_dghtnwqk%3A57630%3A601785632_e5lpwg35%3A79554%3A75471377',
    'cted': 'modId%3Dn376lmui%3Bya_client_id%3D1770017467752291124%7CmodId%3Ddghtnwqk%3Bya_client_id%3D1770017467752291124%7CmodId%3Djlticukg%3Bya_client_id%3D1770017467752291124%7CmodId%3De5lpwg35%3Bya_client_id%3D1770017467752291124',
    'session': 'e68d1f1dee03e4fc9e08153a271d05c377f1158746656b4efdc8581c115bb80d',
    '_ct_session_id': '75471377',
    '_ct_site_id': '79554',
    'call_s': '___jlticukg.1773759676.146807752.489715:1398338|n376lmui.1773759676.75471373.517911:1475225|dghtnwqk.1773759676.601785632.417687:1169994.417689:1170012.422729:1179214|e5lpwg35.1773759676.75471377.518672:1477112|2___',
    '_dsync_vuid_t': '69b965b64840a2-93644006-d9tz',
    'OAuth': '1607320123',
    'wr_visit_id': '1607320123',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://g3.group',
    'priority': 'u=1, i',
    'referer': 'https://g3.group/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-host': 'g3.group',
    # 'cookie': '_ct=3300000000093639509; _ym_uid=1770017467752291124; _ym_d=1773757872; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; _ym_visorc=w; _ct_ids=jlticukg%3A75994%3A146807752_n376lmui%3A79278%3A75471373_dghtnwqk%3A57630%3A601785632_e5lpwg35%3A79554%3A75471377; cted=modId%3Dn376lmui%3Bya_client_id%3D1770017467752291124%7CmodId%3Ddghtnwqk%3Bya_client_id%3D1770017467752291124%7CmodId%3Djlticukg%3Bya_client_id%3D1770017467752291124%7CmodId%3De5lpwg35%3Bya_client_id%3D1770017467752291124; session=e68d1f1dee03e4fc9e08153a271d05c377f1158746656b4efdc8581c115bb80d; _ct_session_id=75471377; _ct_site_id=79554; call_s=___jlticukg.1773759676.146807752.489715:1398338|n376lmui.1773759676.75471373.517911:1475225|dghtnwqk.1773759676.601785632.417687:1169994.417689:1170012.422729:1179214|e5lpwg35.1773759676.75471377.518672:1477112|2___; _dsync_vuid_t=69b965b64840a2-93644006-d9tz; OAuth=1607320123; wr_visit_id=1607320123',
}

json_data = {
    'project_id': '2f413921-bda3-4261-accf-c33260e37c68',
    'filters': [
        {
            'id': 'status',
            'type': 'system',
            'filter_type': 'select',
            'value': [
                'free',
            ],
        },
    ],
    'order_by': [
        'price',
    ],
    'limit': 15,
    'offset': 0,
}

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://g3.group/api/realty-filter/custom/real-estates',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    items = response.json()

    for i in items:

        url = ''
        developer = "G3 Group"
        project = i['project_name'].replace('Театральный', 'G3 Театральный')
        korpus = i['building_number'].replace('Корпус ', '').replace('Дом', '')
        section = ''
        type = i['type']
        if type == 'flat':
            type = 'квартиры'
        finish_type = i['finishing_type']
        if finish_type == 'no':
            finish_type = 'Без отделки'
        if finish_type == 'pre_fine':
            finish_type = 'Предчистовая'
        if finish_type == 'fine':
            finish_type = 'С отделкой'
        room_count = i['rooms_value']
        flat_number = ''
        try:
            area = float(i['total_area'])
        except:
            area = ''
        try:
            old_price = int(i['old_price'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        try:
            floor = i['floor_number']
        except:
            floor = ''


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


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not items:
        break
    json_data['offset'] = json_data['offset'] + json_data['limit']
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer, kvartirografia=False)


