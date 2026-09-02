import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'csrftoken': '6eda8f38a6b74b9bcb7233646d384d7bc0a248efb1c1377bc59a71cd5b0dbb81',
    '_ym_uid': '1781591866686747360',
    '_ym_d': '1781591866',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dq1jibwck%3Bya_client_id%3D1781591866686747360',
    'tmr_lvid': 'e09be8abda581e00193675b65972ff7d',
    'tmr_lvidTS': '1781591866653',
    '_ct_ids': 'q1jibwck%3A67117%3A409727945',
    '_ct_session_id': '409727945',
    '_ct_site_id': '67117',
    'call_s': '___q1jibwck.1781593666.409727945.396266:1141142|2___',
    '_ct': '2800000000277776287',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    '_ym_ucs': 'nginx',
    'domain_sid': 'CyYbkJPEg60Nz3UWao9xA%3A1781591872239',
    'tmr_detect': '0%7C1781591876002',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://sezar-group.ru/flats?mode=cards&project=sezar-budushee',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'csrftoken=6eda8f38a6b74b9bcb7233646d384d7bc0a248efb1c1377bc59a71cd5b0dbb81; _ym_uid=1781591866686747360; _ym_d=1781591866; _ym_isad=2; _ym_visorc=w; cted=modId%3Dq1jibwck%3Bya_client_id%3D1781591866686747360; tmr_lvid=e09be8abda581e00193675b65972ff7d; tmr_lvidTS=1781591866653; _ct_ids=q1jibwck%3A67117%3A409727945; _ct_session_id=409727945; _ct_site_id=67117; call_s=___q1jibwck.1781593666.409727945.396266:1141142|2___; _ct=2800000000277776287; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; _ym_ucs=nginx; domain_sid=CyYbkJPEg60Nz3UWao9xA%3A1781591872239; tmr_detect=0%7C1781591876002',
}

params = {
    'limit': '2000',
    'offset': '0',
    'type': 'flat',
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
counter = 1


response = requests.get('https://sezar-group.ru/api/flats/', params=params, cookies=cookies, headers=headers)

items = response.json()["results"]

for i in items:

    url = ''

    date = datetime.date.today()
    project = i["project_name"]
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
    developer = "Sezar Group"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = i['building_number']
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = f"{i['completion_quarter']} кв {i['completion_year']}"
    stadia = ''
    dogovor = ''
    if i['type'] == "flat":
        type = 'Квартира'
    else:
        type = ''
    finish_type = 'Без отделки'
    try:
        room_count = int(i["rooms"])
    except:
        room_count = i["rooms"]
    area = float(i["area"])
    price_per_metr = ''
    if i['has_discount']:
        old_price = i["original_price"]
        price = i['price']
    else:
        price = i['price']
        old_price = i['price']
    discount = ''
    price_per_metr_new = ''

    section = ''
    try:
        floor = int(i["floor_number"])
    except:
        floor = i["floor_number"]
    flat_number = ''

    print(
        f"{counter}, {project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)
    counter += 1

save_flats_to_excel(flats, project, developer)

