import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import haversine

'''

'''
type_of_lot = 'Вторичка, аренда'



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
                4631
            ],
        },
        'repair': {
            'type': 'terms',
            'value': [
                1, 2, 3, 4
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 99,
            },
        },
        'room': {
            'type': 'terms',
            'value': [
                1, 2, 3, 4, 5, 6, 7, 9
            ],
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



flats = []
counter = 1
total_count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

repair_ids = [2, 3, 4]
repair_ids_dict = {1: 'Без отделки', 2: 'Косметический', 3: 'Евроремонт', 4: 'Дизайнерский'}
rooms_ids = [1,2,3,4,5,6,7,9]

session = requests.Session()

response = session.post(    # Первичный запрос для определения количества лотов
                        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                        cookies=cookies,
                        headers=headers,
                        json=json_data
                    )

items_count = response.json()['data']["aggregatedCount"]
print(f'В городе {items_count} лотов')


if items_count <=  1500:

    rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    total_floor_list = [[1, 100]]

elif 2500 <= items_count <= 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    total_floor_list = [[1, 6], [7, 12], [13, 200]]

elif items_count > 4500:

    rooms_ids = [[1], [9]]
    total_floor_list = [[1, 2], [3, 5], [6, 8], [9, 12], [13, 200]]


current_date = datetime.date.today()
json_data["jsonQuery"]["repair"]["value"] = [0]

for rooms in rooms_ids:

    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["room"]["value"] = rooms


    for repair_id in repair_ids:

        json_data["jsonQuery"]["page"]["value"] = 1
        json_data["jsonQuery"]["repair"]["value"][0] = repair_id


        for f in total_floor_list:


            json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
            json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
            json_data["jsonQuery"]["page"]["value"] = 1
            print(f'Снимаем комнатность: {rooms}')
            print(f'Снимаем отделку: {repair_ids_dict.get(repair_id)}')
            print(f'Снимаем следующие этажи: {f}')

            name_counter = f'{rooms} комнат_этажи - {f[0]}-{f[1]}_{repair_ids_dict.get(repair_id)}'
            flats = []

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
                    result = [type_of_lot, location, location2, okrug, raion, mikroraion, metro, street, house, adress, rooms_count,
                              area, price,
                              finish_type, description, property_from, url,
                              added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount,
                              floorsCount,
                              materialType,
                              parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest,
                              highway_distance,
                              railways_nearest, railways_nearest_distance, railways_nearest_time,
                              railways_nearest_travelType, jk,
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

            df = pd.DataFrame(flats, columns=['Тип объявления',
                                              'Локация',
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

            filename = f"Аренда_{location}_{json_data['jsonQuery']['room']['value']}_{json_data['jsonQuery']['floor']['value']['lte']}_{json_data['jsonQuery']['repair']['value']}_{current_date}.xlsx"

            # Полный путь к файлу
            file_path = os.path.join(folder_path, filename)

            # Сохранение файла в папку
            df.to_excel(file_path, index=False)
