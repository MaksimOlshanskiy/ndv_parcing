import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1781591879104977302',
    '_ym_d': '1781591879',
    '_ym_isad': '1',
    '_ct_site_id': '82671',
    '_ct': '3600000000004128969',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'cted': 'modId%3Diy4916ok%3Bya_client_id%3D1781591879104977302',
    '_ym_visorc': 'w',
    '_ct_ids': 'iy4916ok%3A82671%3A5169456',
    '_ct_session_id': '5169456',
    'call_s': '___iy4916ok.1781597398.5169456.550224:1564730|2___',
}

headers = {
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://novoe-pavlovo.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://novoe-pavlovo.ru/townhouses',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'accept': 'application/graphql-response+json, application/json',
    'content-type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1781591879104977302; _ym_d=1781591879; _ym_isad=1; _ct_site_id=82671; _ct=3600000000004128969; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; cted=modId%3Diy4916ok%3Bya_client_id%3D1781591879104977302; _ym_visorc=w; _ct_ids=iy4916ok%3A82671%3A5169456; _ct_session_id=5169456; call_s=___iy4916ok.1781597398.5169456.550224:1564730|2___',
}

json_data = {
    'query': '\n  query GetFlats(\n    $where: Flat_where\n    $limit: Int\n    $page: Int\n    $sort: String\n  ) {\n    Flats(\n      where: $where\n      limit: $limit\n      page: $page\n      sort: $sort\n    ) {\n      docs {\n        id\n        code\n        crmId\n        name\n        deadline\n        section\n        url\n        plan0\n        plan1\n        plan2\n        plan3\n        price\n        pricem\n        area\n        building\n        mbedroom\n        landArea\n        type\n        terrace\n        security\n        garage\n        electricity\n        water\n        gas\n        sewerage\n        updatedAt\n        createdAt\n        _status\n      }\n      totalDocs\n      limit\n      totalPages\n      page\n      pagingCounter\n      hasPrevPage\n      hasNextPage\n      prevPage\n      nextPage\n    }\n  }\n',
    'variables': {
        'where': {
            'AND': [
                {
                    'price': {
                        'greater_than_equal': 299786,
                        'less_than_equal': 3693790799,
                    },
                },
                {
                    'pricem': {
                        'greater_than_equal': 1873,
                        'less_than_equal': 232799999,
                    },
                },
                {
                    'area': {
                        'greater_than_equal': 1,
                        'less_than_equal': 999.05,
                    },
                },
                {
                    'landArea': {
                        'greater_than_equal': 0.11,
                        'less_than_equal': 99.19,
                    },
                },
                {
                    '_status': {
                        'equals': 'published',
                    },
                },
            ],
        },
        'limit': 100,
        'page': 1,
        'sort': 'price',
    },
    'operationName': 'GetFlats',
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
counter = 1

response = requests.post('https://novoe-pavlovo.ru/api/gql', cookies=cookies, headers=headers, json=json_data)

items = response.json()["data"]["Flats"]['docs']

for i in items:

    url = ''
    date = datetime.date.today()
    project = 'Новое Павлово'
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
    developer = "СЗ Сосновый парк"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = str(i["building"])
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = i['deadline'].replace('I', '1').replace('.', '')
    stadia = ''
    dogovor = ''
    type = 'Таунхаусы'
    finish_type = 'Без отделки'
    room_count = ''
    area = float(i["area"])
    price_per_metr = ''
    old_price = i["price"]
    discount = ''
    price_per_metr_new = ''
    price = i['price']
    section = ''
    floor = ''
    flat_number = ''

    print(
        f"{counter}, {project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)
    counter += 1



save_flats_to_excel(flats, project, developer)

