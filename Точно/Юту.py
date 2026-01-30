import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1752221103932115499',
    '_ym_d': '1769583420',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    'roistat_visit': '1163569',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    'roistat_phone': '8%20(495)%20189-65-32',
    'roistat_raw_phone': '74951896532',
    'roistat_call_tracking': '1',
    'roistat_phone_replacement': 'null',
    'roistat_phone_script_data': '%5B%7B%22phone%22%3A%228%20(495)%20189-65-32%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274953858334%22%5D%2C%22raw_phone%22%3A%2274951896532%22%7D%5D',
    '___dc': '5787f38d-071a-46a3-83a6-d5146cd78335',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=main,sentry-public_key=0fb6c062c84d17cffe5d163743844f00,sentry-trace_id=0b55f98316b649ef8e269f2fac9abb3e,sentry-sampled=true,sentry-sample_rand=0.8836383942607882,sentry-sample_rate=1',
    'priority': 'u=1, i',
    'referer': 'https://u2.moscow/flats',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '0b55f98316b649ef8e269f2fac9abb3e-875fc677fbad0d25-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1752221103932115499; _ym_d=1769583420; _ym_visorc=w; _ym_isad=2; roistat_visit=1163569; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; roistat_phone=8%20(495)%20189-65-32; roistat_raw_phone=74951896532; roistat_call_tracking=1; roistat_phone_replacement=null; roistat_phone_script_data=%5B%7B%22phone%22%3A%228%20(495)%20189-65-32%22%2C%22css_selectors%22%3A%5B%5D%2C%22replaceable_numbers%22%3A%5B%2274953858334%22%5D%2C%22raw_phone%22%3A%2274951896532%22%7D%5D; ___dc=5787f38d-071a-46a3-83a6-d5146cd78335; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
}

params = {
    'order': 'price',
    'limit': '8',
    'offset': '0',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

session = requests.Session()

while True:

    response = session.get(
        'https://u2.moscow/api/flats/',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    items = response.json()['results']

    for i in items:

        url = ''
        developer = "Точно"
        project = 'U2'
        korpus = '1'
        section = i['section']

        if i['type'] == "flats":
            type = 'Квартиры'
        else:
            type = i['type']

        finish_type = 'Без отделки'
        if i['rooms'] == '0':
            room_count = 'Студия'
        else:
            room_count = i['rooms']
        flat_number = i['number']
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = float(i['original_price'])
        except:
            old_price = ''
        try:
            price = float(i['price'])
        except:
            price = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''


        english = 'U2'
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
    params['offset'] = str(int(params['offset']) + 8)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

