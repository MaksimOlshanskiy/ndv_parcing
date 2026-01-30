'''

Нужно изменить в data количество на число квартир с сайта!! https://city-story.ru/flats/table/
'''

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ct_site_id': '72805',
    '_ct': '3000000000033078834',
    '_ym_uid': '1742828118827031850',
    '_ym_d': '1742828118',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_isad': '2',
    'cted': 'modId%3Dpgolc3n3%3Bya_client_id%3D1742828118827031850',
    'PHPSESSID': '4FxovjVLkLEOdtW8KntTwMxSMSIOJk1s',
    'MORTGAGE_ID': '1',
    '_ym_visorc': 'w',
    '_ct_ids': 'pgolc3n3%3A72805%3A45908041',
    '_ct_session_id': '45908041',
    'call_s': '___pgolc3n3.1742890699.45908041.453444:1281529.453453:1281617|2___',
    'OAuth': '1310014750',
    'wr_visit_id': '1310014750',
    '_dmp_key_t': 'X/8mWLOUKW1xd2rvJXZyS2BVeuwI4cGwxLeWZC8rsSmI00i7en4UD31AJggoM8iXIEieKJaKSXVrZA==',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://city-story.ru',
    'Referer': 'https://city-story.ru/flats/table/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ct_site_id=72805; _ct=3000000000033078834; _ym_uid=1742828118827031850; _ym_d=1742828118; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_isad=2; cted=modId%3Dpgolc3n3%3Bya_client_id%3D1742828118827031850; PHPSESSID=4FxovjVLkLEOdtW8KntTwMxSMSIOJk1s; MORTGAGE_ID=1; _ym_visorc=w; _ct_ids=pgolc3n3%3A72805%3A45908041; _ct_session_id=45908041; call_s=___pgolc3n3.1742890699.45908041.453444:1281529.453453:1281617|2___; OAuth=1310014750; wr_visit_id=1310014750; _dmp_key_t=X/8mWLOUKW1xd2rvJXZyS2BVeuwI4cGwxLeWZC8rsSmI00i7en4UD31AJggoM8iXIEieKJaKSXVrZA==',
}

params = {
    'c': 'twolines:realty',
    'action': 'params',
    'mode': 'class',
}

data = {
    'post[prog]': 'PROG_M_1',
    'post[sort][PROPERTY_COST]': 'ASC',
    'post[nPageSize]': '88',     #   Нужно изменить данное количество на число квартир с сайта!! https://city-story.ru/flats/table/
    'post[iNumPage]': '1',
}


flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://city-story.ru/bitrix/services/main/ajax.php',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
    )
    print(response.status_code)
    try:
        items = response.json()['data']['elements']
    except:
        break

    for i in items:

        url = f"https://city-story.ru{i["URL"]}"

        date = datetime.date.today()
        project = "Городские истории"
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
        developer = "Центр-Инвест"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = extract_digits_or_original(i["CORPUS_FULL"])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        if i['PROPERTY_FINISH'] == 'WhiteBox':
            finish_type = "Предчистовая"
        else:
            finish_type = i['PROPERTY_FINISH']
        if i["ROOMS_FULL"] == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i["ROOMS_FULL"])

        area = float(i["PROPERTY_SPACE"])
        price_per_metr = ''
        try:
            old_price = int(i['OLD_PRICE'])
        except:
            old_price = i['OLD_PRICE']
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(i['PROPERTY_COST'])
        except:
            price = i['PROPERTY_COST']
        try:
            section = int(i["PROPERTY_SECTION"])
        except:
            section = i["PROPERTY_SECTION"]
        floor = int(i["PROPERTY_FLOOR"])

        try:
            flat_number = int(i['PROPERTY_NUMBER'])
        except:
            flat_number = i['PROPERTY_NUMBER']

        print(
            f"{url}, {project}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    data["post[iNumPage]"] = int(data["post[iNumPage]"]) + 1
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    break


save_flats_to_excel(flats, project, developer)