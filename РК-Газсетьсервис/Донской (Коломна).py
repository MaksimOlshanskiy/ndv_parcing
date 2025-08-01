import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': '6oigrd1mvnpas7270no670d9qi',
    '_ym_uid': '1744366056493324114',
    '_ym_d': '1744366056',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://rk-gazsetservis.ru/catalog/choose/complex_2/filter/?turnId[]=34',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=6oigrd1mvnpas7270no670d9qi; _ym_uid=1744366056493324114; _ym_d=1744366056; _ym_isad=2; _ym_visorc=w',
}

response = requests.get(
    'https://rk-gazsetservis.ru/catalog/api/catalog_free/?complexId[]=2&turnId[]=34&tab[]=filter',
    cookies=cookies,
    headers=headers,
)

items = response.json()['flat']
flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for i in items:

    url = ''
    developer = "РК-Газсетьсервис"
    project = 'Донской (Коломна)'
    korpus = ''
    type = 'Квартиры'
    finish_type = 'Без отделки'
    room_count = int(i['room'])
    try:
        area = float(i['area'])
    except:
        area = ''
    try:
        old_price = int(i['price'])
    except:
        old_price = ''
    try:
        price = ''
    except:
        price = ''
    section = ''
    try:
        floor = int()
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

