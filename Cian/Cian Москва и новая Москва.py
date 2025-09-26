'''

cian отдаёт не более 1500 объявлений
нужно проходиться по каждому списку: ids_moscow и т.д., подставляя его в 40 строке

'''


import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, save_cian_to_excel

decoration_dict = {'preFine' : 'Предчистовая', 'fine' : 'С отделкой', 'without' : 'Без отделки', 'fineWithFurniture' : 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']


obshiy = [36935, 1444810, 6381, 5494, 50743, 2352, 48686, 2184313, 2344978, 7778, 5138735, 3683691,
       3419909, 3911074, 46840, 50027, 4051375, 4186702, 2234022, 1900321, 368, 81377, 45865,
       5227, 4771631, 4117447, 4708643, 3782658, 4157734, 45774, 843911, 2498484, 8825,
       4025502, 92320, 2511297, 4850351, 3932079, 4780951, 4296442, 4676364, 912499, 4033066,
       3206071, 4457540, 3966751, 4720970, 4682511, 3913242, 4779110, 8787, 3930584, 90586,
       5100524, 4260360, 5340468, 4648486, 46529, 48693, 4482950, 176051, 7789, 2567913, 4585408, 7030,
       1641578, 300653, 5138871, 3730443, 7956, 4558643, 4729772, 1358767, 17877, 4833927, 1628126, 8689, 5208,
        4482905, 5194393, 3394804, 600475, 5499, 4056931, 2522095, 2202, 4677457, 3922634, 4109874, 6644, 319,
          4126730, 3402470, 3872784, 5500590, 5698426, 4747901, 5624837, 3975866, 5696721, 5694445, 41567]

ids_moscow = [1444810, 6381, 5494, 50743, 2352, 48686, 2184313, 2344978, 7778, 5138735, 3683691,
       3419909, 3911074, 46840, 50027, 4051375, 4186702, 2234022, 1900321, 368, 81377, 45865,
       5227, 4771631, 4117447, 4708643, 3782658, 4157734, 45774, 843911, 2498484, 8825,
       4025502, 92320, 2511297, 4850351, 3932079, 4780951, 4296442, 4676364, 912499, 4033066,
       3206071, 4457540, 3966751, 4720970, 4682511, 3913242, 4779110, 8787, 3930584, 90586,
       5100524, 4260360, 5340468, 4648486, 46529, 48693, 4482950, 176051, 7789, 2567913, 4585408, 7030,
       1641578, 300653, 5138871
       ]  # id ЖК для парсинга, переименовываем на просто ids

ids_mo_dalnee = [3730443, 7956, 4558643, 4729772, 1358767, 17877
       ]

ids_mo_srednee = [4833927, 1628126, 8689, 5208, 4482905, 5194393, 3394804, 600475, 5499, 4056931, 2522095, 2202

       ]

ids_mo_bliz = [118473, 4677457, 3922634, 4109874, 6644, 319, 4126730
       ]

parsim = [41567]

cookies = {
    '_CIAN_GK': '787699e3-fc12-4a31-a77a-6cfd610b499c',
    '_gcl_au': '1.1.1422723987.1740731465',
    'tmr_lvid': 'b47c6c39b48ce8d68592cfa9ff9beaf0',
    'tmr_lvidTS': '1740731465513',
    '_ga': 'GA1.1.582149124.1740731467',
    '_ym_uid': '1740731467185025844',
    '_ym_d': '1740731467',
    'uxfb_usertype': 'searcher',
    'uxs_uid': '5b193cf0-f5ae-11ef-8867-1b8844357aae',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'afUserId': 'be3c106f-b0b6-4cef-af07-257ce88c47d3-p',
    'login_button_tooltip_key': '1',
    'cookie_agreement_accepted': '1',
    '__zzatw-cian': 'MDA0dBA=Fz2+aQ==',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'login_mro_popup': '1',
    'AF_SYNC': '1741934640332',
    'uxfb_card_satisfaction': '%5B314449567%2C314109440%2C304829381%2C308541124%2C313898469%5D',
    'session_region_id': '4584',
    'session_main_town_region_id': '4820',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742068546693%2C%22sl%22%3A%7B%22224%22%3A1741982146693%2C%221228%22%3A1741982146693%7D%7D',
    'cf_clearance': '9bFfKFzrTyhJoXh6aUwmAUOw7.BpxIzlXSVpaOItWN8-1742045497-1.2.1.1-KPUokSd_FdfMVYehorc1zC2Quny6JE2i8yrzcZ01XILzjkP7zxqgscaMzMKBg4CuFeRhC97Bv87CgJRcVM2tYAILfmFG0rKUqsSm6QiquIjpes0g7s64Gw9AcWqKjNrofZ61T6Q300fL.dSxfRredQ55XAjzhsSsfVI4do_RJ6krlopy9BFfj1yfRBzXHYEBkbZi3uYeJjTKAc45DoW19.npfYLQeKT1xwCH6Ggy6Gz_p2V1Mnr_X9pb0L8vTvi3K2sWC3ioMZMl6yn_qKZ5hP.2MuXPEqPt_MYIBj2ovOvQzeabrtARIcHxaESCyv.AEg9nB9Wyv6FeDAuAVXNCpXl0qEIDDK_ornkhkkxLyFo',
    'countCallNowPopupShowed': '1%3A1742045479686',
    'sopr_session': '84b470aec35341e6',
    'adrdel': '1742045514747',
    '_ym_visorc': 'b',
    '_ym_isad': '1',
    '__cf_bm': 'ePtk5p8wMH3.xlQDOOiuz5wZaPNU7A1zwvjnCkoNHV0-1742045698-1.0.1.1-dxq.c.moLRQKtPve.MgKmqOenHlr9ek_ABNjKvJvQx3pd5l3tn4.N52Z8LHlvVNlw6v3qvBGoEt8_6Vw_y.Is_dZVXmPBR7mvjqXUzrN34g',
    '_ga_3369S417EL': 'GS1.1.1742045476.23.1.1742045996.15.0.0',
    'cfidsw-cian': 'AxdMvlRRvR6My2+fKjo4YJdkzCoF/jlq91PsPICw1gb/lQoINg65e35zgs3rWzmh2HHtC2h8oQGhyYkaGNzM90nGR60NqOhPs2Bve5PCL6Z7YKfyZwxq/LC162B50yseaP2lR8ETH+7tgalQtQ+SVZ/4D6qFYMITcwYMzoQ=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://krasnodar.cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://krasnodar.cian.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=787699e3-fc12-4a31-a77a-6cfd610b499c; _gcl_au=1.1.1422723987.1740731465; tmr_lvid=b47c6c39b48ce8d68592cfa9ff9beaf0; tmr_lvidTS=1740731465513; _ga=GA1.1.582149124.1740731467; _ym_uid=1740731467185025844; _ym_d=1740731467; uxfb_usertype=searcher; uxs_uid=5b193cf0-f5ae-11ef-8867-1b8844357aae; adrcid=A0r9KB4fc8duMUv2jPsp-tg; afUserId=be3c106f-b0b6-4cef-af07-257ce88c47d3-p; login_button_tooltip_key=1; cookie_agreement_accepted=1; __zzatw-cian=MDA0dBA=Fz2+aQ==; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; login_mro_popup=1; AF_SYNC=1741934640332; uxfb_card_satisfaction=%5B314449567%2C314109440%2C304829381%2C308541124%2C313898469%5D; session_region_id=4584; session_main_town_region_id=4820; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742068546693%2C%22sl%22%3A%7B%22224%22%3A1741982146693%2C%221228%22%3A1741982146693%7D%7D; cf_clearance=9bFfKFzrTyhJoXh6aUwmAUOw7.BpxIzlXSVpaOItWN8-1742045497-1.2.1.1-KPUokSd_FdfMVYehorc1zC2Quny6JE2i8yrzcZ01XILzjkP7zxqgscaMzMKBg4CuFeRhC97Bv87CgJRcVM2tYAILfmFG0rKUqsSm6QiquIjpes0g7s64Gw9AcWqKjNrofZ61T6Q300fL.dSxfRredQ55XAjzhsSsfVI4do_RJ6krlopy9BFfj1yfRBzXHYEBkbZi3uYeJjTKAc45DoW19.npfYLQeKT1xwCH6Ggy6Gz_p2V1Mnr_X9pb0L8vTvi3K2sWC3ioMZMl6yn_qKZ5hP.2MuXPEqPt_MYIBj2ovOvQzeabrtARIcHxaESCyv.AEg9nB9Wyv6FeDAuAVXNCpXl0qEIDDK_ornkhkkxLyFo; countCallNowPopupShowed=1%3A1742045479686; sopr_session=84b470aec35341e6; adrdel=1742045514747; _ym_visorc=b; _ym_isad=1; __cf_bm=ePtk5p8wMH3.xlQDOOiuz5wZaPNU7A1zwvjnCkoNHV0-1742045698-1.0.1.1-dxq.c.moLRQKtPve.MgKmqOenHlr9ek_ABNjKvJvQx3pd5l3tn4.N52Z8LHlvVNlw6v3qvBGoEt8_6Vw_y.Is_dZVXmPBR7mvjqXUzrN34g; _ga_3369S417EL=GS1.1.1742045476.23.1.1742045996.15.0.0; cfidsw-cian=AxdMvlRRvR6My2+fKjo4YJdkzCoF/jlq91PsPICw1gb/lQoINg65e35zgs3rWzmh2HHtC2h8oQGhyYkaGNzM90nGR60NqOhPs2Bve5PCL6Z7YKfyZwxq/LC162B50yseaP2lR8ETH+7tgalQtQ+SVZ/4D6qFYMITcwYMzoQ=',
}

json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'newobject',
                    'id': 4825183,
                },
            ],
        },
        'decorations_list': {
            'type': 'terms',
            'value': [
                'preFine',
            ],
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
}



def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

current_date = datetime.date.today()

no_flats = []

for y in parsim:

    session = requests.Session()

    flats = []

    json_data["jsonQuery"]["page"]["value"] = 1

    print("Новый ЖК", y)

    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y

    for decoration in decoration_list:

        counter = 1
        total_count = 1
        json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
        json_data["jsonQuery"]["page"]["value"] = 1
        print(decoration)




        while True:

            if counter > 1:
                sleep_time = random.uniform(7, 11)
                time.sleep(sleep_time)

            try:
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data
                )

                print(response.status_code)
            except:
                print("Произошла ошибка, пробуем ещё раз")
                time.sleep(61)
                session = requests.Session()
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data
                )
                print(response.status_code)
            items = response.json()["data"]["offersSerialized"]


            for i in items:
                try:
                    if i['building']['deadline']['isComplete'] == True:
                        srok_sdachi = "Дом сдан"
                    elif i['building']['deadline']['quarterEnd'] is None:
                        srok_sdachi = ''
                    else:
                        srok_sdachi = f"Cдача ГК: {i['building']['deadline']['quarterEnd']}"
                except:
                    srok_sdachi = ''
                try:
                    url = i['fullUrl']
                except:
                    url = ''

                try:
                    if i['isApartments'] == True:
                        type = "Апартаменты"
                    else:
                        type = "Квартира"
                except:
                    type = ''
                try:
                    if i['discount'] is not None:
                        price = extract_digits_or_original(i['discount']['newPrice'])
                        old_price = extract_digits_or_original(i['discount']['oldPrice'])
                    else:
                        old_price = i['bargainTerms']['priceRur']
                        price = ''
                except:
                    print('Херня какая-то тут')
                    old_price = i['bargainTerms']['priceRur']
                    price = ''
                try:
                    project = i['geo']['jk']['displayName']
                except:
                    project = ''
                try:
                    finish_type = decoration_dict.get(decoration)
                except:
                    finish_type = ''
                try:
                    adress = i['geo']['userInput']
                except:
                    adress = ""

                try:
                    korpus = str(i["geo"]["jk"]["house"]["name"]).replace('Корпус ', '')
                except:
                    korpus = ''

                try:
                    developer = i['geo']['jk']['developer']['name']
                except:
                    developer = ""

                try:
                    if i["roomsCount"] == None:
                        room_count = 0
                    else:
                        room_count = int(i["roomsCount"])
                except:
                    room_count = ''
                try:
                    area = float(i["totalArea"])
                except:
                    area = ''


                date = datetime.date.today()

                try:
                    floor = i["floorNumber"]
                except:
                    floor = ''
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

                eskrou = ''
                konstruktiv = ''
                klass = ''
                srok_sdachi_old = ''
                stadia = ''
                dogovor = ''

                discount = ''
                price_per_metr = ''
                price_per_metr_new = ''

                section = ''
                flat_number = ''


                print(
                    f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                          mck, distance_to_mck, time_to_mck, distance_to_bkl,
                          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                          konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                          price_per_metr_new, price, section, floor, flat_number]
                flats.append(result)

            total_count = response.json()["data"]["offerCount"]
            downloaded = len(flats)
            print(f'ID ЖК: {y}. Отделка: {decoration}. Загружено {downloaded} предложений из {total_count}')
            print("-----------------------------------------------------------------------------")
            if not items:
                break
            json_data["jsonQuery"]["page"]["value"] += 1



            counter += 1

    if len(flats) > 0:
        save_cian_to_excel(flats, project, developer)
    else:
        no_flats.append(y)

print(f'Пустые проекты: {no_flats}')


