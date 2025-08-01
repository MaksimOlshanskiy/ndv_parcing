"""
отдельно выгрузка с отделкой и отдельно без отделки 'finish_option': '1' - с отделкой, 0 - без отделки
Автоматически, менять ничего не нужно

"""

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from datetime import datetime

from functions import save_flats_to_excel

cookies = {
    '_ga_KSG3KSTJM3': 'GS1.1.1742906448.1.0.1742906448.60.0.0',
    'scbsid_old': '2746015342',
    'tmr_lvid': '3f48638a68eb16526d18a46fbc2effea',
    'tmr_lvidTS': '1742906449205',
    '_ym_uid': '1742906450489206027',
    '_ym_d': '1742906450',
    '_ga': 'GA1.2.680231928.1742906449',
    '_gid': 'GA1.2.1167946476.1742906450',
    '_gat_gtag_UA_129678842_1': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstoKw22': '1742906451',
    '_comagic_idoKw22': '9219217967.13156914412.1742906450',
    'domain_sid': 'gkEk1-PwKSrgGi_7YYiNj%3A1742906451469',
    'tmr_detect': '0%7C1742906451512',
    'sma_session_id': '2237548317',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBstart': '1742906452669',
    'SCBFormsAlreadyPulled': 'true',
    'activity': '2|20',
    'SCBindexAct': '1115',
    'sma_index_activity': '1567',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'priority': 'u=1, i',
    'referer': 'https://vatutinki.ru/flats?type_object=flat',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_ga_KSG3KSTJM3=GS1.1.1742906448.1.0.1742906448.60.0.0; scbsid_old=2746015342; tmr_lvid=3f48638a68eb16526d18a46fbc2effea; tmr_lvidTS=1742906449205; _ym_uid=1742906450489206027; _ym_d=1742906450; _ga=GA1.2.680231928.1742906449; _gid=GA1.2.1167946476.1742906450; _gat_gtag_UA_129678842_1=1; _ym_isad=2; _ym_visorc=w; _cmg_csstoKw22=1742906451; _comagic_idoKw22=9219217967.13156914412.1742906450; domain_sid=gkEk1-PwKSrgGi_7YYiNj%3A1742906451469; tmr_detect=0%7C1742906451512; sma_session_id=2237548317; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBstart=1742906452669; SCBFormsAlreadyPulled=true; activity=2|20; SCBindexAct=1115; sma_index_activity=1567',
}

params = {
    'type_object': 'flat',
    'pereustupka': 'false',
    'secondhand': 'false',
    'order': 'price',
    'finish_option': '1',
    'limit': '48',
    'offset': '0',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for finishing in range(2):

    params['finish_option'] = str(finishing)
    params['offset'] = '0'
    print(params)

    while True:

        response = requests.get('https://vatutinki.ru/api/property/', params=params, cookies=cookies, headers=headers)
        print(response.status_code)
        items = response.json()['results']

        for i in items:

            url = ''
            date = datetime.now()
            project = "Новые Ватутинки"
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
            developer = "Инвест Траст"
            okrug = ''
            district = ''
            adress = f"Мкр-н {i['project']['name']}"
            eskrou = ''
            korpus = i['building']['number']
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартиры'
            if params['finish_option'] == '1':
                finish_type = 'С отделкой'
            elif params['finish_option'] == '0':
                finish_type = 'Без отделки'

            room_count = int(i['rooms'])

            area = float(i['area'])

            price_per_metr = ''
            old_price = round(float(i['price_compare']))
            discount = ''
            price_per_metr_new = ''
            try:
                price = round(float(i["price"]))
            except:
                price = i["price"]
            section = int(i['section']['number'])
            floor = i['floor']['number']
            flat_number = i['number']


            print(
                f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                      klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        if not items:
            break
        params["offset"] = int(params["offset"]) + 48
        sleep_time = random.uniform(1, 4)
        time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)