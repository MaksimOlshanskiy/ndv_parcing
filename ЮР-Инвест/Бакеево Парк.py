import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'nH2r4gOfNQwvOe5uIvLcCCBfBAcTtHTz',
    'tmr_lvid': 'fbbe8ad5dc76620bce5544c5d38612ac',
    'tmr_lvidTS': '1744100086502',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ct_ids': 'sxn6d06l%3A34704%3A845687760',
    '_ct_session_id': '845687760',
    '_ct_site_id': '34704',
    'call_s': '___sxn6d06l.1744101886.845687760.129217:400274|2___',
    '_ct': '1300000000522635150',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_fbp': 'fb.1.1744100087031.77877498222069338',
    '_ga': 'GA1.2.1912214567.1744100087',
    '_gid': 'GA1.2.815229790.1744100087',
    '_ym_uid': '1744100087651523117',
    '_ym_d': '1744100087',
    'domain_sid': 'nhcm68uEc8QTMYAH6fiFR%3A1744100087364',
    '_ga_QP2TMWBZGY': 'GS1.2.1744100087.1.0.1744100087.60.0.0',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    'cted': 'modId%3Dsxn6d06l%3Bclient_id%3D1912214567.1744100087%3Bya_client_id%3D1744100087651523117%3Bfbp%3Dfb.1.1744100087031.77877498222069338',
    'tmr_detect': '0%7C1744100088821',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://bakeevopark.ru',
    'priority': 'u=1, i',
    'referer': 'https://bakeevopark.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=nH2r4gOfNQwvOe5uIvLcCCBfBAcTtHTz; tmr_lvid=fbbe8ad5dc76620bce5544c5d38612ac; tmr_lvidTS=1744100086502; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ct_ids=sxn6d06l%3A34704%3A845687760; _ct_session_id=845687760; _ct_site_id=34704; call_s=___sxn6d06l.1744101886.845687760.129217:400274|2___; _ct=1300000000522635150; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _fbp=fb.1.1744100087031.77877498222069338; _ga=GA1.2.1912214567.1744100087; _gid=GA1.2.815229790.1744100087; _ym_uid=1744100087651523117; _ym_d=1744100087; domain_sid=nhcm68uEc8QTMYAH6fiFR%3A1744100087364; _ga_QP2TMWBZGY=GS1.2.1744100087.1.0.1744100087.60.0.0; _ym_visorc=w; _ym_isad=2; cted=modId%3Dsxn6d06l%3Bclient_id%3D1912214567.1744100087%3Bya_client_id%3D1744100087651523117%3Bfbp%3Dfb.1.1744100087031.77877498222069338; tmr_detect=0%7C1744100088821',
}

data = {
    'params[square-from]': '33.7',
    'params[square-to]': '114.81',
    'params[price-from]': '6 622 834',
    'params[price-to]': '15 701 921',
    'params[param1]': 'false',
    'params[param2]': 'false',
    'params[param3]': 'false',
    'params[param4]': 'false',
    'params[param5]': 'false',
    'params[param6]': 'false',
    'params[param8]': 'false',
    'params[param9]': 'false',
    'params[param10]': 'false',
    'params[param11]': 'false',
    'params[param12]': 'false',
    'params[param13]': 'false',
    'params[param14]': 'false',
    'params[balcony]': 'false',
    'params[sort]': '2',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

response = requests.post('https://bakeevopark.ru/ajax/handler.php', cookies=cookies, headers=headers, data=data)

print(response.status_code)

items = response.json()


for i in items:

    url = ''

    date = datetime.date.today()
    project = "Бакеево Парк"
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
    developer = "ЮР-Инвест"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = int(i['PROPS']['HOUSE']['VALUE'])
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    if i['PROPS']['OTDELKA']['VALUE'] == 'Чистовая':
        finish_type = 'С отделкой'
    elif i['PROPS']['OTDELKA']['VALUE'] == 'Черновая':
        finish_type = 'Предчистовая'
    else:
        finish_type = 'Без отделки'
    room_count = int(i['PROPS']['ROOMS_COUNT']['VALUE'])
    area = float(i['PROPS']['SQUARE']["VALUE"].replace(' ', ''))
    price_per_metr = ''
    old_price = int(i['FIELDS']['PRICE'].replace(' ', ''))
    discount = ''
    price_per_metr_new = ''
    price = int(i['FIELDS']['PRICE_DISCOUNT'].replace(' ', ''))
    section = ''
    floor = int(i['PROPS']['FLOOR']['VALUE'])
    flat_number = ''
    print(
        f"{url}, {project}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

save_flats_to_excel(flats, project, developer)