import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

import requests

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1742894343511268445',
    '_ym_d': '1742894343',
    '_ga_8NEY7ZCFSK': 'GS1.1.1742894342.1.1.1742894342.0.0.0',
    'scbsid_old': '2746015342',
    '_ym_visorc': 'w',
    '_ga': 'GA1.2.419505434.1742894343',
    '_gid': 'GA1.2.818451609.1742894343',
    '_gat_UA-190626972-1': '1',
    '_ct_ids': '7bg7n3k9%3A42863%3A564202147',
    '_ct_session_id': '564202147',
    '_ct_site_id': '42863',
    'call_s': '___7bg7n3k9.1742896142.564202147.194185:1091880|2___',
    '_ct': '1700000000371044541',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cted': 'modId%3D7bg7n3k9%3Bclient_id%3D419505434.1742894343%3Bya_client_id%3D1742894343511268445',
    '_ym_isad': '2',
    '_ga_L94SD4V55J': 'GS1.1.1742894342.1.1.1742894364.38.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': '',
    'priority': 'u=1, i',
    'referer': 'https://lunar.moscow/flats?order=price',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1742894343511268445; _ym_d=1742894343; _ga_8NEY7ZCFSK=GS1.1.1742894342.1.1.1742894342.0.0.0; scbsid_old=2746015342; _ym_visorc=w; _ga=GA1.2.419505434.1742894343; _gid=GA1.2.818451609.1742894343; _gat_UA-190626972-1=1; _ct_ids=7bg7n3k9%3A42863%3A564202147; _ct_session_id=564202147; _ct_site_id=42863; call_s=___7bg7n3k9.1742896142.564202147.194185:1091880|2___; _ct=1700000000371044541; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cted=modId%3D7bg7n3k9%3Bclient_id%3D419505434.1742894343%3Bya_client_id%3D1742894343511268445; _ym_isad=2; _ga_L94SD4V55J=GS1.1.1742894342.1.1.1742894364.38.0.0',
}

params = {
    'calltouch_tm': 'yd_c:74182020_gb:4906919036_ad:12323454679_ph:38694245598_st:search_pt:premium_p:1_s:none_dt:mobile_reg:11030_ret:38694245598_apt:none',
    'etext': '2202.HHfizz7nNvli1VncYh55EfQ5-mRlROBxnlvEZ_xjMAYpEM8vbqZR51t_fia1E5ND2lYsJ7DpITPp7G4kfwH5EEpSdiGnD0OnKjf5WazZVBloZ3dkcWh5enBpcHNycmxz.5da9c3b032ae31de59d1b5655cab07a1a4d75859',
    'floor_max': '',
    'floor_min': '',
    'module': '',
    'order': 'price',
    'page': '1',
    'price_max': '',
    'price_min': '',
    'rooms': '',
    'square_max': '',
    'square_min': '',
    'utm_campaign': 'tw_hutton_lunar_leninsky38_yandex_search_brand_rf|74182020',
    'utm_content': 'type__text3search|pl_none|grid_4906919036|adid_12323454679|rt_38694245598|ptype_premium|pos_1|device_mobile',
    'utm_medium': 'cpc',
    'utm_source': 'yandex',
    'utm_term': 'лунар ленинский проспект|kwid_38694245598',
    'yclid': '9509856325491490815',
}





flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://lunar.moscow/api/property/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)

    try:
        items = response.json()["results"]
    except:
        break

    for i in items:

        url = ''

        date = datetime.date.today()
        project = "Лунар"
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
        developer = "Хаттон"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['module_letter']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        if i['decoration_type'] == "White box":
            finish_type = "Предчистовая"
        elif i['decoration_type'] == 'Финишная':
            finish_type = "С отделкой"
        else:
            finish_type = i['decoration_type']
        room_count = i["room"]

        area = i["square"]
        price_per_metr = ''
        try:
            old_price = int(i['old_price'].replace(".00", ''))
            price = i["price"]
        except AttributeError:
            old_price = i["price"]
            price = ''
        discount = ''
        price_per_metr_new = ''

        section = ''
        floor = i["floor_number"]
        flat_number = i['number']


        print(
            f"{url}, {project}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = int(params["page"]) + 1
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)