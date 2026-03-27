import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from datetime import datetime

from functions import save_flats_to_excel

headers = {
    'accept': 'application/graphql-response+json, application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://grandfili.ru',
    'priority': 'u=1, i',
    'referer': 'https://grandfili.ru/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

json_data = {
    'query': '\n  query GetFlats(\n    $where: Flat_where\n    $limit: Int\n    $page: Int\n    $sort: String\n  ) {\n    Flats(\n      where: $where\n      limit: $limit\n      page: $page\n      sort: $sort\n    ) {\n      docs {\n        id\n        code\n        crmId\n        name\n        deadline\n        section\n        url\n        planPath\n        floorPlan\n        viewsPlan\n        floor\n        rooms\n        area\n        price\n        number\n        view1\n        view2\n        view3\n        view4\n        fireplace\n        mbedroom\n        kpantry\n        wbath\n        loggia\n        wardrobe\n        pnumber\n         plans {\n          id\n          url\n        }\n        updatedAt\n        createdAt\n        _status\n      }\n      totalDocs\n      limit\n      totalPages\n      page\n      pagingCounter\n      hasPrevPage\n      hasNextPage\n      prevPage\n      nextPage\n    }\n  }\n',
    'variables': {
        'where': {
            'AND': [
                {
                    'price': {
                        'greater_than_equal': 28988223,
                        'less_than_equal': 77940933,
                    },
                },
                {
                    'area': {
                        'greater_than_equal': 38.73,
                        'less_than_equal': 100.14,
                    },
                },
                {
                    'floor': {
                        'greater_than_equal': 2,
                        'less_than_equal': 10,
                    },
                },
                {
                    '_status': {
                        'equals': 'published',
                    },
                },
            ],
        },
        'limit': 20,
        'page': 1,
        'sort': 'area',
    },
    'operationName': 'GetFlats',
}





flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


session = requests.Session()

while True:

    response = requests.post('https://grandfili.ru/api/gql', headers=headers, json=json_data)

    print(response.status_code)
    items = response.json()['data']['Flats']['docs']

    for i in items:

        url = ''


        date = datetime.now()
        project = 'Гранд Фили'
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
        developer = "Гранард"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = 'Без отделки'
        room_count = i['rooms']
        area = float(i['area'])
        price_per_metr = ''
        old_price = int(i['price'])
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = int(i['floor'])
        flat_number = i['number']



        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break
    json_data['variables']['page'] = json_data['variables']['page'] + 1
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")