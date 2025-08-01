import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from datetime import datetime
import requests

from functions import save_flats_to_excel

finishing_ids = ['e78af76f-8f3c-49c0-ba9c-0421df104fa4', 'f7c51519-b5eb-4055-9dfb-cc40b9f1a426', '9120e779-f2a7-440c-91b1-aeb2ab2aec66']
finishing_ids_dict = {'e78af76f-8f3c-49c0-ba9c-0421df104fa4' : 'С отделкой', 'f7c51519-b5eb-4055-9dfb-cc40b9f1a426' : 'Предчистовая', '9120e779-f2a7-440c-91b1-aeb2ab2aec66' : 'Без отделки' }
rooms_count_list = ['studio', '1_room', '2_room', '3_room', '4_and_more_room']
rooms_count_dict = {'studio': 0, '1_room': 1, '2_room': 2, '3_room': 3, '4_and_more_room': 4}

cookies = {
    '_ym_uid': '1742813750390448864',
    '_ym_d': '1742813750',
    'anonymousAccountID': '3ebba459-fc69-4b6b-bab6-06e29c691b5d',
    'businessLocationAlias': 'moscow',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-public_key=ccb902671fc9e0392dd67d04b2a41234,sentry-trace_id=3184d56251cb4837a997a98664ac0f91,sentry-sample_rate=1,sentry-transaction=GET%20%2Fzhilye-kompleksy%2Fakczenty-e0f1ab,sentry-sampled=true',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://dombook.plus/zhilye-kompleksy/akczenty-e0f1ab',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '3184d56251cb4837a997a98664ac0f91-b9202a06e70e7294-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1742813750390448864; _ym_d=1742813750; anonymousAccountID=3ebba459-fc69-4b6b-bab6-06e29c691b5d; businessLocationAlias=moscow; _ym_isad=2; _ym_visorc=w',
}

params = {
    'pagination[per_page]': '10',
    'pagination[page]': '1',
    'filters[finishing_type][0]': '9120e779-f2a7-440c-91b1-aeb2ab2aec66',
    'project_id': '8716b383-7dfb-417e-a7e4-ccb8489e173c',
    'lot_type_alias': 'kvartira',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



for rooms in rooms_count_list:
    params['filters[rooms][0]'] = rooms

    for f_id in finishing_ids:
        params['filters[finishing_type][0]'] = f_id
        params["pagination[page]"] = '1'

        while True:

            print(params)

            response = requests.get('https://dombook.plus/api/v1/project/get.lots', params=params, cookies=cookies, headers=headers)

            print(response.status_code)
            items = response.json()['content']['lots']

            for i in items:

                url = ''
                date = datetime.now()
                project = i['project']['name']
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
                developer = "PLUS Development"
                okrug = ''
                district = ''
                adress = ''
                eskrou = ''
                korpus = i['building_name'].replace('Корпус ', '')
                konstruktiv = ''
                klass = ''
                srok_sdachi = ''
                srok_sdachi_old = ''
                stadia = ''
                dogovor = ''
                type = 'Квартиры'
                finish_type = finishing_ids_dict.get(params['filters[finishing_type][0]'])
                room_count = rooms_count_dict.get(rooms)

                area = float(i['square'])

                price_per_metr = ''
                if i['discount_price'] is not None:
                    old_price = i['price']
                else:
                    old_price = ''
                discount = ''
                price_per_metr_new = ''
                if i["discount_price"] is not None:
                    price = i["discount_price"]
                else:
                    price = i["price"]
                section = ''
                floor = i['floor']
                flat_number = ''



                print(
                    f"{project}, {url}, отделка: {finish_type}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
                result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                          distance_to_mck, time_to_mck, distance_to_bkl,
                          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                          klass, srok_sdachi, srok_sdachi_old,
                          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                          price_per_metr_new, price, section, floor, flat_number]
                flats.append(result)
            if not items:
                break
            params["pagination[page]"] = str(int(params["pagination[page]"]) + 1)
            sleep_time = random.uniform(1, 4)
            time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)