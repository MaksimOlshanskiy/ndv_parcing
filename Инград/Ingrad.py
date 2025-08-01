import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://www.ingrad.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.ingrad.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

params = {
    'numberElementsPage': '200',
    'currentPage': '1',
    'sortBy': 'price',
    'sortOrder': 'asc',
    'ignoreFilterAdvantagesFlatsAliases': '0',
    'ignoreFilterRooms': '0',
    'ignoreFilterHouses': '0',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://new-api.ingrad.ru/api/flats/search', params=params, headers=headers)

    items = response.json()["data"]["flats"]

    for i in items:

        url = f"https://www.ingrad.ru/{i["link"]}"

        date = datetime.date.today()
        project = i["estateData"]["name"]
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
        developer = "Sminex"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = str(i["houseData"]["number"])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['type'] == "flat":
            type = 'Квартира'
        else:
            type = ''
        if i["finish"] == 'White Box':
            finish_type = 'Предчистовая'
        else:
            finish_type = i["finish"]

        try:
            room_count = int(i["rooms"])
        except:
            room_count = i["rooms"]
        area = float(i["square"])
        price_per_metr = ''
        old_price = i["priceNoDiscount"]
        discount = ''
        price_per_metr_new = ''
        price = i['price'][0]
        section = ''
        try:
            floor = int(i["floorData"]["number"])
        except:
            floor = i["floorData"]["number"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["currentPage"] = str(int(params["currentPage"]) + 1)
    sleep_time = random.uniform(10, 15)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break


save_flats_to_excel(flats, project, "Sminex-Инград")

