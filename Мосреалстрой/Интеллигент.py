import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://mosrealstroy.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://mosrealstroy.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


response = requests.get('https://hub.feedfox.ru/json/intelligent', headers=headers)

items = response.json()

for i in items:
    if i['statuscode'] == '4' and i['subtypecode'] == '2' and i['typecode'] == '2':
        url = ''

        date = datetime.date.today()
        project = "Интеллигент"

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
        developer = "Мосреалстрой"
        okrug = ''
        district = ''
        adress = i['address']
        eskrou = ''
        korpus = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = 'Без отделки'
        room_count = int(i['rooms'])

        area = float(i['square'])
        price_per_metr = ''
        try:
            old_price = int(i['oldPrice'])
        except:
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        price = int(i["price"])
        section = int(i['sectionNumber'])
        floor = int(i['floor'])
        flat_number = int(i['btiNumber'])

        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)


save_flats_to_excel(flats, project, developer)