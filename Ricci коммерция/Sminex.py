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
    'origin': 'https://www.sminex.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.sminex.com/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'RoompickerStartSession',
    'variables': {
        'searchParams': 'type=commercial&profiles=retail',
        'currency': 'RUB',
    },
    'query': 'query RoompickerStartSession($searchParams: String, $currency: String) {\n  roompickerStartSession(searchParams: $searchParams, currency: $currency) {\n    sessionId\n    searchParams\n    orderBy\n    orderIsDesc\n    totalQuantity\n    hasMore\n    filters {\n      id\n      attrEntity\n      attrName\n      title\n      filterType\n      groupTitle\n      groups {\n        title\n        values {\n          id\n          value\n          isActive\n          isDisabled\n          preview\n          hint {\n            title\n            description\n            imageUrl\n            moreUrl\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      histogram {\n        rangeFrom\n        rangeTo\n        min\n        max\n        globalMin\n        globalMax\n        data\n        __typename\n      }\n      __typename\n    }\n    lots {\n      id\n      projectName\n      buildingName\n      floorNumber\n      flatName\n      flatPrice\n      flatPriceMeter\n      flatType\n      flatSizes\n      flatArea\n      flatRooms\n      flatBlocked\n      flatCeilingHeight\n      flatCode\n      projectId\n      courtyardName\n      advantages\n      mainFloor\n      totalFloors\n      flatWindowViews\n      layouts {\n        balconyFromBedroom\n        balconyFromKitchenLiving\n        bathroomWindow\n        closetWindow\n        homeOffice\n        kidsPlayroom\n        link\n        linkMinified\n        nannyRoom\n        planOrder\n        planType\n        pool\n        sportsRoom\n        twoStory\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
}




flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



response = requests.post('https://apikey.sminex.com/', headers=headers, json=json_data)
print(response.status_code)
print(response)

items = response.json()['data']['roompickerStartSession']['lots']

for i in items:


    url = ""
    date = datetime.date.today()
    project = i['projectName']
    english = ''
    promzona = ''
    mestopolozhenie = ''
    subway = ''
    distance_to_subway = ''
    time_to_subway = ''
    finish_type = 'Без отделки'
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
    korpus = i['buildingName']
    if 'Sky' in korpus:
        project = 'RiverSky'
    if project == 'Достижение':
        korpus = '1'
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = i['flatType']
    room_count = ''
    area = float(i['flatArea'])
    price_per_metr = ''
    old_price = float(i['flatPrice'])
    discount = ''
    price_per_metr_new = ''
    price = float(i['flatPrice'])
    section = ''
    floor = i['floorNumber']
    flat_number = ''


    print(
        f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)


save_flats_to_excel(flats, project, developer)