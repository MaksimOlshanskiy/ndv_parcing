'''

Подстановка названия ЖК и номеров корпусов идёт через словари. При добавлении нового ЖК нужно обновить и словари тоже.
Снимаем сразу оба ЖК
https://ddoomm.moscow/ добавить как цены появятся

'''

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from Developer_dict import developer_dict, name_dict
from functions import save_flats_to_excel

jks = {1317 : "SOLOS", 1316: "Rakurs", 1318: "DOM"}
houses = {1183: '2', 1184: '3', 1185: '4', 1186 : '1', 1187: '2', 1189: '1'}
flats = []
projects_id = [258, 883]
urls = {258: 'https://solos.moscow/api/apartment', 883: 'https://rakurs.moscow/api/v3/places', }



headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'apptoken': 'e290d41710c3ca1a9c8e86ba02ca2e47',
    'content-type': 'application/json',
    'origin': 'https://ddoomm.moscow',
    'priority': 'u=1, i',
    'referer': 'https://ddoomm.moscow/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
}

params = {
    'id_house[]': '1189',
    'category[]': 'Квартира',
    'saleStatus[]': '1',
    'AgentCostStart': '1',
    'AgentCostEnd': '16769800899',
    'allSquareStart': '8.2',
    'allSquareEnd': '1669.7',
    'floorStart': '1',
    'floorEnd': '22',
    'orderBy': 'AgentCost',
    'noBooking[]': '1',
    'page': '1',
}


date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://api.planetarf.ru/api/v3/places', params=params, headers=headers)
    print(response.status_code)

    items = response.json()["places"]


    for i in items:

        url = ''
        developer = "Дар"
        project = 'DOM'
        korpus = houses.get(i["id_house"])
        type = 'Квартиры'
        if i["repair"] == 'Предчистовая отделка':
            finish_type = 'Предчистовая'
        else:
            finish_type = i["repair"]
        room_count = i["rooms"]
        try:
            area = float(i["allSquare"])
        except:
            area = ''
        try:
            old_price = int(i['AgentCost_old'])
        except:
            old_price = ''
        try:
            price = int(i["AgentCost"])
        except:
            price = ''
        section = ''
        try:
            floor = int(i["floor"])
        except:
            floor = i["floor"]
        flat_number = int(i["id"])

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

    if not items:
        break
    params['page'] = str(int(params['page'])+1)
    print('Следующая страница')
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer, kvartirografia=False)

