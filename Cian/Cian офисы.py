import requests
import datetime
import time
import pandas as pd
import os
import random
from functions import merge_and_clean, haversine
import json

type_of_lot = 'Коммерция, продажа'

# noinspection PyDictDuplicateKeys
import requests

cookies = {
    '_ym_uid': '1740731467185025844',
    '_gcl_au': '1.1.221627179.1775114569',
    'cookie_agreement_accepted': '1',
    'tmr_lvid': '5d429d59ad05d69a68419a6b714c0955',
    'tmr_lvidTS': '1775114589434',
    '_ga': 'GA1.1.1494365673.1775114597',
    'uxfb_usertype': 'searcher',
    '_CIAN_GK': '9dad5c1d-1f84-4ff8-afb9-1be8d68b7c80',
    '_ym_d': '1776705880',
    'cian_ruid': '8098251',
    'uxs_uid': 'd6ea8010-470f-11f1-a167-7960045d3975',
    'nbrdng_fv': '1777837191618',
    'newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown': '1',
    'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatAnimationShownCount': '3',
    'newbuilding-card-desktop-frontend.consultant_cian_chat_onboarding_shown': '1',
    'newbuilding-card-desktop-fichering-frontend.consultant_cian_chat_onboarding_shown': '1',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'WBRMVisitLast_utm': '',
    'WBRMVisitLast_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    'WBRMVisitFirst_utm': '',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'frontend-serp.chatTooltipAnimationShown': '1',
    'frontend-serp.chatAnimationShownCount': '3',
    'frontend-serp.chatAnimationCounter': '5',
    'frontend-serp.chatAnimationPrevPath': '%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D4927%26totime%3D2592000',
    'map_preview_onboarding_counter': '3',
    'transport-accessibility_onboarding_counter': '3',
    'newbuilding-search-frontend.chatAnimationCounter': '6',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnewobjects%2Flist%2F%3Fbuilders%255B0%255D%3D17132%26deal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D-1%26show_old_newobjects%3D1',
    'frontend-serp.header_builder_chat_onboarding_shown': '1',
    'WBRMVisitFirst_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    'DMIR_AUTH': 'NljgjqJFspi9B9hsVLvOL%2BN485l2a9rEXksqKNZqXrAYN9mp0xFbnrmllZXUXxTJ0ECVZaPNbRxkfUgWCr8zfaHnKwYJd89t5UVlGfOHwISanLF%2BxErUpPcKTPI3eN9rzbOZLukbDk0n58Qs9wtu%2BWbFT%2FlGQ6lN%2BRPE4cU6TNg%3D',
    'countCallNowPopupShowed': '2%3A1780486387527',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'forever_region_id': '4606',
    'session_region_id': '4606',
    'session_region_name': '%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_region_name': '%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'session_main_town_region_id': '4959',
    'forever_main_town_region_id': '4959',
    '_ym_isad': '1',
    'rrpvid': '77082295317102',
    'uxfb_card_satisfaction': '%5B329625786%2C299784235%2C326369393%5D',
    '_yasc': 'nIVOEOTwgCpJV9Buz2Cm+2rS1mZ4JhGGWhhwvWl6/DswfYaS5K6sd8cDVC1zboScBemVqUNc/g==.MTc4MDI1OTE2MjE1MQ==',
    '_yasc': 'kGQW0dHjNKWLF/hu7OKyR2l5Y/XD/96egM4rIwbCxkr6pFOmgI9p+B7TKVtawX2zyoSaD7cDrg==.MTc4MDI1OTE2MjE1MQ==',
    'sopr_session': '81be96dc537c4570',
    'cookieUserID': '8098251',
    '_ga_3369S417EL': 'GS2.1.s1781549168$o46$g1$t1781549765$j32$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://rostov.cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://rostov.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1740731467185025844; _gcl_au=1.1.221627179.1775114569; cookie_agreement_accepted=1; tmr_lvid=5d429d59ad05d69a68419a6b714c0955; tmr_lvidTS=1775114589434; _ga=GA1.1.1494365673.1775114597; uxfb_usertype=searcher; _CIAN_GK=9dad5c1d-1f84-4ff8-afb9-1be8d68b7c80; _ym_d=1776705880; cian_ruid=8098251; uxs_uid=d6ea8010-470f-11f1-a167-7960045d3975; nbrdng_fv=1777837191618; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=3; newbuilding-card-desktop-frontend.consultant_cian_chat_onboarding_shown=1; newbuilding-card-desktop-fichering-frontend.consultant_cian_chat_onboarding_shown=1; frontend-serp.offer_chat_onboarding_shown=1; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; frontend-serp.chatAnimationShownCount=3; frontend-serp.chatAnimationCounter=5; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D4927%26totime%3D2592000; map_preview_onboarding_counter=3; transport-accessibility_onboarding_counter=3; newbuilding-search-frontend.chatAnimationCounter=6; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnewobjects%2Flist%2F%3Fbuilders%255B0%255D%3D17132%26deal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D-1%26show_old_newobjects%3D1; frontend-serp.header_builder_chat_onboarding_shown=1; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; DMIR_AUTH=NljgjqJFspi9B9hsVLvOL%2BN485l2a9rEXksqKNZqXrAYN9mp0xFbnrmllZXUXxTJ0ECVZaPNbRxkfUgWCr8zfaHnKwYJd89t5UVlGfOHwISanLF%2BxErUpPcKTPI3eN9rzbOZLukbDk0n58Qs9wtu%2BWbFT%2FlGQ6lN%2BRPE4cU6TNg%3D; countCallNowPopupShowed=2%3A1780486387527; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; forever_region_id=4606; session_region_id=4606; session_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_main_town_region_id=4959; forever_main_town_region_id=4959; _ym_isad=1; rrpvid=77082295317102; uxfb_card_satisfaction=%5B329625786%2C299784235%2C326369393%5D; _yasc=nIVOEOTwgCpJV9Buz2Cm+2rS1mZ4JhGGWhhwvWl6/DswfYaS5K6sd8cDVC1zboScBemVqUNc/g==.MTc4MDI1OTE2MjE1MQ==; _yasc=kGQW0dHjNKWLF/hu7OKyR2l5Y/XD/96egM4rIwbCxkr6pFOmgI9p+B7TKVtawX2zyoSaD7cDrg==.MTc4MDI1OTE2MjE1MQ==; sopr_session=81be96dc537c4570; cookieUserID=8098251; _ga_3369S417EL=GS2.1.s1781549168$o46$g1$t1781549765$j32$l0$h0',
}

json_data = {
    'jsonQuery': {
        '_type': 'commercialrent',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                1,
            ],
        },
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'price': {
            'type': 'range',
            'value': {
                'gte': 20000001,
                'lte': 999000000,
            },
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
        },
        'office_type': {
            'type': 'terms',
            'value': [
                1,
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
    '_liquiditySource': 'web_commercial-serp',
}
session = requests.Session()
current_date = datetime.date.today()
flats = []

while True:

    response = session.post(  # Первичный запрос для определения количества лотов
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
        keys = ["location", "location2", "location3", "okrug", "raion", "mikroraion", "metro", "street", "house"]

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
        if i['bargainTerms']['priceType'] == 'squareMeter' and i['bargainTerms']['paymentPeriod'] == 'annual':
            price = (price * area)/12
        try:
            finish_type = ''
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
        try:
            url = i['fullUrl']
        except:
            url = ''

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
        try:
            land_area = i['land']['area']
        except:
            land_area = ''
        try:
            land_area_unit_type = i['land']['areaUnitType']
        except:
            land_area_unit_type = ''
        try:
            possibleToChangeStatus = i['land']['possibleToChangeStatus']
        except:
            possibleToChangeStatus = ''
        try:
            land_statusl = i['land']['status']
        except:
            land_statusl = ''
        try:
            land_type = i['land']['type']
        except:
            land_type = ''
        try:
            buildingType2 = i['businessShoppingCenter']['buildingType']
        except:
            buildingType2 = ''
        try:
            buildingClassType = i['businessShoppingCenter']['buildingClassType']
        except:
            buildingClassType = ''
        try:
            building_name = i['businessShoppingCenter']['name']
        except:
            building_name = ''
        try:
            buildingType = i['businessShoppingCenter']['type']
        except:
            buildingType = ''
        try:
            layout = i['layout']
        except:
            layout = ''
        try:
            offerType = i['offerType']
        except:
            offerType = ''
        try:
            officeType = i['office']
        except:
            officeType = ''
        if i['areaParts']:
            for part in i['areaParts']:
                area = part['area']
                price = part['price']

                print(
                    f"Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
                result = [type_of_lot, location, location2, location3, okrug, raion, mikroraion, metro, street, house,
                          adress, rooms_count, area, price, finish_type, description, property_from, url,
                          added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount,
                          floorsCount, materialType,
                          parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest,
                          highway_distance,
                          railways_nearest, railways_nearest_distance, railways_nearest_time,
                          railways_nearest_travelType, jk,
                          underground_nearest, underground_nearest_time, hasFurniture,
                          kitchenArea, livingArea, loggiasCount, land_area, land_area_unit_type, possibleToChangeStatus,
                          land_statusl, land_type,
                          buildingType2, buildingClassType, building_name, buildingType, layout, offerType, officeType
                          ]
                flats.append(result)


        else:
            print(
                f"Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
            result = [type_of_lot, location, location2, location3, okrug, raion, mikroraion, metro, street, house, adress, rooms_count, area, price, finish_type, description, property_from, url,
                      added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount, floorsCount, materialType,
                      parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest, highway_distance,
                      railways_nearest, railways_nearest_distance, railways_nearest_time, railways_nearest_travelType, jk,
                      underground_nearest, underground_nearest_time, hasFurniture,
                      kitchenArea, livingArea, loggiasCount, land_area, land_area_unit_type, possibleToChangeStatus, land_statusl, land_type,
                      buildingType2, buildingClassType, building_name, buildingType, layout, offerType, officeType
                      ]
            flats.append(result)

    json_data["jsonQuery"]["page"]["value"] += 1
    print("-----------------------------------------------------------------------------")





    if not items:
        break
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)


if len(flats) > 0:
    # Базовый путь для сохранения
    base_path = r""

    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"Офисы_аренда_13-3.xlsx"

    # Полный путь к файлу
    file_path = os.path.join(folder_path, filename)

    df = pd.DataFrame(flats, columns=['Тип объявления',
                                      'Локация',
                                      'Локация2',
                                      'Локация3',
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
                                      'ID объявления',
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
                                      'Число лоджий',
                                      'Площадь земли',
                                      'Единица измерения площади',
                                      'Возможность смены статуса',
                                      'Статус земли',
                                      'Тип земли',
                                      'buildingType2',
                                      'buildingClassType',
                                      'building_name',
                                      'buildingType',
                                      'layout',
                                      'offerType',
                                      'officeType'
                                      ])



    # Сохранение файла в папку
    df.to_excel(file_path, index=False)
    print(f'✅ Файл {filename} успешно сохранён')





