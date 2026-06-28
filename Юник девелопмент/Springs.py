import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

import requests

cookies = {
    'device_view': 'full',
    '_ct_ids': 'aq7dem68%3A69487%3A414072260',
    '_ct_session_id': '414072260',
    '_ct_site_id': '69487',
    'call_s': '___aq7dem68.1781603303.414072260.421585:1181208|2___',
    '_ct': '2900000000272347561',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'cookieConsentStatus': '1',
    '30sec_ap': '36',
    '60sec_ap': '36',
    '90sec_ap': '2',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://springs.house/flats?types%5B%5D=townhouse&price%5Bfrom%5D=64685800&price%5Bto%5D=365840000&square%5Bfrom%5D=64&square%5Bto%5D=216&floor%5Bfrom%5D=1&floor%5Bto%5D=20',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'device_view=full; _ct_ids=aq7dem68%3A69487%3A414072260; _ct_session_id=414072260; _ct_site_id=69487; call_s=___aq7dem68.1781603303.414072260.421585:1181208|2___; _ct=2900000000272347561; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cookieConsentStatus=1; 30sec_ap=36; 60sec_ap=36; 90sec_ap=2',
}

params = {
    'types[]': [
        'flat',
        'townhouse',
    ],
    'price[from]': '1',
    'price[to]': '36584000999',
    'square[from]': '1',
    'square[to]': '9999',
    'floor[from]': '1',
    'floor[to]': '99',
    'sort': 'price-asc',
    'locale': 'ru',
    'offset': '0',
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://springs.house/api/flats.json', params=params, cookies=cookies, headers=headers)

    items = response.json()["data"]

    for i in items:

        url = ''

        date = datetime.date.today()
        project = 'Спрингс'
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
        developer = "UNIQ Development"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = 'вл. 46'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if 'T' in i['number']:
            type = 'Таунхаусы'
        else:
            type = 'Квартиры'
        finish_type = 'Без отделки'
        try:
            room_count = int(i["rooms"])
        except:
            room_count = i["rooms"]
        area = float(i["square"])
        price_per_metr = ''
        old_price = i["price"]
        discount = ''
        price_per_metr_new = ''
        price = i['price']
        section = ''
        try:
            floor = int(i["floor"])
        except:
            floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["offset"] = str(int(params["offset"]) + 12)
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break


save_flats_to_excel(flats, project, developer)

