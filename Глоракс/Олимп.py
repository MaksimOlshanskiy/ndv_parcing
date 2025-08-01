import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests


import requests

from functions import save_flats_to_excel

headers = {
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'https://dom-olymp.ru/apartments/selection-of-apartments.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

response = requests.get('https://dom-olymp.ru/apartments/api.json', headers=headers)
items = response.json()

for korp in items:

    all_flats = korp['apartments']



    for i in all_flats:



        url = ''
        developer = "Glorax"
        project = 'Олимп (Хотьково)'
        korpus = i['house_number']
        type = 'Квартиры'
        finish_type = 'Без отделки'
        room_count = i['room_count']
        try:
            area = float(i['square'])
        except:
            area = ''
        try:
            old_price = i['price']
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        section = ''
        try:
            floor = int(i['floor'])
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

