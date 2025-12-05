import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import datetime
import random

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1744356214802326974',
    '_ym_d': '1744356214',
    '_ym_isad': '2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://domoplaner.ru/catalog/471/haTFbn/?start=1&domain=aHR0cHM6Ly9zaWdtYS1zaWxpbm8uY29t&back=1&state=facades&house_id=3843',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1744356214802326974; _ym_d=1744356214; _ym_isad=2',
}

response = requests.get('https://domoplaner.ru/widget-api/widget/471-haTFbn/', cookies=cookies, headers=headers)
print(response.status_code)
items = response.json()['flats']
flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for i in items:

    url = ''
    developer = "Айгрин"
    project = 'Сигма Силино'
    korpus = '1'
    type = 'Апартаменты'
    if i['decoration_id'] == 273:
        finish_type = 'С отделкой'
    if i['is_studio'] == 1:
        room_count = 0
    else:
        room_count = int(i['rooms'])
    try:
        area = float(i['area'])
    except:
        area = ''
    try:
        old_price = int(i['price'])
    except:
        old_price = ''
    try:
        price = int(i['price_with_discount'])
    except:
        price = ''
    section = i['house_title']
    try:
        floor = int(i['floor_number'])
    except:
        floor = ''
    flat_number = int(i['number'])


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

save_flats_to_excel(flats, project, developer)

