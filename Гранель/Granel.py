# текущий код выгружает все квартиры из всех ЖК одним запросом

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime

from functions import save_flats_to_excel

cookies = {
    'csrftoken': 'cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1',
    '_ym_uid': '1741701518760793495',
    '_ym_d': '1741701518',
    '_ym_isad': '2',
    '_ga': 'GA1.2.2019530414.1741701518',
    '_gid': 'GA1.2.119258665.1741701518',
    '_ym_visorc': 'w',
    '_dc_gtm_UA-68221887-1': '1',
    'OAuth': '1295255121',
    'wr_visit_id': '1295255121',
    'mars': '571cea60c1064eddb514b03f938bcb9a',
    'sessionid': 'wk6174yimlq6hn0dhjlkqahnsdwa596u',
    'dbl': '4e6bc89260dc4d5fbf8bdec6e0fe8670',
    'cted': 'modId%3Dfc97be79%3Bclient_id%3D2019530414.1741701518%3Bya_client_id%3D1741701518760793495',
    '_ct_ids': 'fc97be79%3A17380%3A4794763832',
    '_ct_session_id': '4794763832',
    '_ct_site_id': '17380',
    'call_s': '___fc97be79.1741703320.4794763832.49394:1248368|2___',
    '_ct': '3100000002820627262',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_gali': 'header',
    '_ga_FR9TMQETHP': 'GS1.1.1741701517.1.1.1741701532.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'priority': 'u=1, i',
    'referer': 'https://granelle.ru/flats?is_released=0&view=grid',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-csrftoken': 'cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1',
    # 'cookie': 'csrftoken=cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1; _ym_uid=1741701518760793495; _ym_d=1741701518; _ym_isad=2; _ga=GA1.2.2019530414.1741701518; _gid=GA1.2.119258665.1741701518; _ym_visorc=w; _dc_gtm_UA-68221887-1=1; OAuth=1295255121; wr_visit_id=1295255121; mars=571cea60c1064eddb514b03f938bcb9a; sessionid=wk6174yimlq6hn0dhjlkqahnsdwa596u; dbl=4e6bc89260dc4d5fbf8bdec6e0fe8670; cted=modId%3Dfc97be79%3Bclient_id%3D2019530414.1741701518%3Bya_client_id%3D1741701518760793495; _ct_ids=fc97be79%3A17380%3A4794763832; _ct_session_id=4794763832; _ct_site_id=17380; call_s=___fc97be79.1741703320.4794763832.49394:1248368|2___; _ct=3100000002820627262; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _gali=header; _ga_FR9TMQETHP=GS1.1.1741701517.1.1.1741701532.0.0.0',
}

params = {
    'area_max': '',
    'area_min': '',
    'city': '1',
    'floor_number_max': '',
    'floor_number_min': '',
    'is_apartments': '',
    'is_black_friday': '',
    'is_business': '',
    'is_coming': '',
    'is_cyber_monday': '',
    'is_profit': '',
    'is_property_of_the_day': '',
    'is_released': '0',
    'is_with_keys': '',
    'limit': '4000',
    'offset': '0',
    'order': '',
    'price_max': '',
    'price_min': '',
    'search': '',
    'withLayouts': 'false',
}

response = requests.get('https://granelle.ru/api/flats/', params=params, cookies=cookies, headers=headers)

flats = []
counter = 1
offset = 0
date = datetime.now().date()

def extract_digits_or_original(s):
    if s == "Тихий дом":
        return s
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


url = 'https://granelle.ru/api/flats/'
response = requests.get(url, params=params, cookies=cookies, headers=headers)

items = response.json()["results"]

for i in items:

    url = f"https://granelle.ru/flats/{i["id"]}"
    developer = "Гранель"
    project = i["project"]
    korpus = i["building"]
    if i['type'] == "flat":
        type = 'Квартиры'
    else:
        type = i['type']
    if i["finish_type"] == "whitebox":
        finish_type = "Предчистовая"
    elif i["finish_type"] == "finish":
        finish_type = "С отделкой"
    elif i["finish_type"] == "without_finish":
        finish_type = "Без отделки"
    else:
        finish_type = i["finish_type"]
    room_count = i["rooms"]
    try:
        area = float(i["area"])
    except:
        area = ''
    try:
        old_price = round(float(i["price"]))
    except:
        old_price = ''
    try:
        price = round(float(i["price_discounted"]))
    except:
        price = ''
    section = ''
    try:
        floor = int(i["floor"])
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
    srok_sdachi = f"{i["completion_quarter"]} кв {i["completion_year"]} года"
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    price_per_metr = ''
    discount = ''
    price_per_metr_new = ''

    print(
        f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

save_flats_to_excel(flats, project, developer)

