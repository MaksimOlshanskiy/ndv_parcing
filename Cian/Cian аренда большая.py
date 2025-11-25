import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import haversine

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

coords = city_centers.get("1")

ids = [4629063,
       ]  # id ЖК для парсинга

proxies = {
    'https': '47.95.203.57:8080'
}

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
        '_type': 'flatrent',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'region': {
            'type': 'terms',
            'value': [
                1
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 3,
            },
        },
        'room': {
            'type': 'terms',
            'value': [
                1
            ],
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
        },
        'for_day': {
            'type': 'term',
            'value': '!1',
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
}



response = requests.post(
    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

name_counter = 1

session = requests.Session()

flats = []
counter = 1
total_count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


current_date = datetime.date.today()

while len(flats) < total_count:

    if counter > 1:
        sleep_time = random.uniform(6, 9)
        time.sleep(sleep_time)
    try:
        response = session.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            cookies=cookies,
            headers=headers,
            json=json_data
        )

        print(response.status_code)

        items = response.json()["data"]["offersSerialized"]
    except:
        print("Произошла ошибка, пробуем ещё раз")
        print(response.status_code)
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
        data = i['geo']['address']
        result = {}
        counterr = {}

        for item in data:
            t = item["type"]
            name = item["fullName"]

            # Первый раз — без номера
            if t not in counterr:
                counterr[t] = 1
                key = t
            else:
                counterr[t] += 1
                key = f"{t}{counterr[t]}"

            result[key] = name

        print(result)
        # список нужных переменных
        keys = ["location", "location2", "okrug", "raion", "mikroraion", "metro", "street", "house"]

        # создаём переменные
        for key in keys:
            globals()[key] = result.get(key, "")

        try:
            adress = i['geo']['userInput']
        except:
            adress = ''
        try:
            jk = i['geo']['jk']['displayName']
        except:
            jk = ''
        try:
            if not i['roomsCount'] and i['flatType'] == 'studio':
                rooms_count = 0
            else:
                rooms_count = i['roomsCount']
        except:
            rooms_count = ''
        try:
            area = float(i['totalArea'])
        except:
            area = ''
        try:
            price = int(i['bargainTerms']['priceRur'])
        except:
            price = i['bargainTerms']['priceRur']
        try:
            finish_type = repair_ids_dict.get(repair_id)
        except:
            finish_type = 'Неизвестно'
        try:
            description = i['description']
        except:
            description = ''
        try:
            if i['fromDeveloper'] == True or i['user']['isBuilder'] == True:
                property_from = "От застройщика"
            elif i['user']['isAgent'] is True:
                property_from = "От агента"
            elif i['isByHomeowner'] is True:
                property_from = 'От собственника'
            else:
                property_from = ''
        except:
            property_from = ''
        url = str(i['fullUrl'])

        try:
            added = i['added']
        except:
            added = ''
        try:
            balconiesCount = i['balconiesCount']
        except:
            balconiesCount = ''
        try:
            bedroomsCount = i['bedroomsCount']
        except:
            bedroomsCount = ''
        try:
            buildYear = i['building']['buildYear']
        except:
            buildYear = ''
        try:
            cargoLiftsCount = i['building']['cargoLiftsCount']
        except:
            cargoLiftsCount = ''
        try:
            passengerLiftsCount = i['building']['passengerLiftsCount']
        except:
            passengerLiftsCount = ''
        try:
            floorsCount = i['building']['floorsCount']
        except:
            floorsCount = ''
        try:
            materialType = i['building']['materialType']
        except:
            materialType = ''
        try:
            parking = i['building']['parking']['type']
        except:
            parking = ''
        try:
            creationDate = i['creationDate']
        except:
            creationDate = ''
        try:
            floorNumber = i['floorNumber']
        except:
            floorNumber = ''
        try:
            coordinates_lat = i['geo']['coordinates']['lat']
        except:
            coordinates_lat = ''
        try:
            coordinates_lng = i['geo']['coordinates']['lng']
        except:
            coordinates_lng = ''
        try:
            highways_nearest = i['geo']['highways'][0]['name']
        except:
            highways_nearest = ''
        try:
            highway_distance = i['geo']['highways'][0]['distance']
        except:
            highway_distance = ''
        try:
            railways_nearest = i['geo']['railways'][0]['name']
        except:
            railways_nearest = ''
        try:
            railways_id = i['geo']['railways'][0]['id']
        except:
            railways_id = ''
        try:
            railways_nearest_distance = i['geo']['railways'][0]['distance']
        except:
            railways_nearest_distance = ''
        try:
            railways_nearest_time = i['geo']['railways'][0]['time']
        except:
            railways_nearest_time = ''
        try:
            railways_nearest_travelType = i['geo']['railways'][0]['travelType']
        except:
            railways_nearest_travelType = ''
        try:
            jk = i['geo']['jk']['displayName']
        except:
            jk = ''
        try:
            underground_nearest = i['geo']['railways'][0]['name']
        except:
            underground_nearest = ''
        try:
            underground_nearest_time = i['geo']['railways'][0]['time']
        except:
            underground_nearest_time = ''
        try:
            hasFurniture = i['hasFurniture']
        except:
            hasFurniture = ''
        try:
            kitchenArea = i['kitchenArea']
        except:
            kitchenArea = ''
        try:
            livingArea = i['livingArea']
        except:
            livingArea = ''
        try:
            loggiasCount = i['loggiasCount']
        except:
            loggiasCount = ''

        print(
            f"Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
        result = [location, location2, okrug, raion, mikroraion, metro, street, house, adress, rooms_count, area, price,
                  finish_type, description, property_from, url,
                  added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount, floorsCount,
                  materialType,
                  parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest,
                  highway_distance,
                  railways_nearest, railways_nearest_distance, railways_nearest_time, railways_nearest_travelType, jk,
                  underground_nearest, underground_nearest_time, hasFurniture,
                  kitchenArea, livingArea, loggiasCount
                  ]
        flats.append(result)

    json_data["jsonQuery"]["page"]["value"] += 1
    print("-----------------------------------------------------------------------------")
    total_count = response.json()["data"]["offerCount"]
    downloaded = len(flats)
    print(f'Номер страницы: {json_data["jsonQuery"]["page"]["value"]}')
    print(f'Загружено {downloaded} предложений из {total_count}')
    counter += 1
    if not items:
        break
    sleep_time = random.uniform(7, 9)
    time.sleep(sleep_time)

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{location}_{current_date}_{name_counter}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Локация',
                                  'Локация2',
                                  'Округ',
                                  'Район',
                                  'Микрорайон',
                                  'Метро',
                                  'Улица',
                                  'Дом',
                                  'Адрес',
                                  'Кол-во комнат',
                                  'Площадь',
                                  'Цена',
                                  'Отделка',
                                  'Описание',
                                  'Объявление от',
                                  'Ссылка',
                                  'Обновлено',
                                  'Балконы',
                                  'Число спален',
                                  'Год постройки',
                                  'Грузовые лифты',
                                  'Пассажирские лифты',
                                  'Всего этажей',
                                  'Тип материалов',
                                  'Паркинг',
                                  'Дата создания',
                                  'Этаж',
                                  'Координаты широта',
                                  'Координаты долгота',
                                  'Ближайшее шоссе',
                                  'Расстояние от МКАД',
                                  'Ближайшая жд станция',
                                  'Расстояние до жд станции',
                                  'Время до жд',
                                  'Тип траспорта',
                                  'ЖК',
                                  'Ближайшее метро',
                                  'Время до метро',
                                  'С мебелью',
                                  'Площадь кухни',
                                  'Жилая площадь',
                                  'Число лоджий'
                                  ])

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Аренда_{location}_{json_data['jsonQuery']['room']['value']}_{json_data['jsonQuery']['floor']['value']['lte']}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
