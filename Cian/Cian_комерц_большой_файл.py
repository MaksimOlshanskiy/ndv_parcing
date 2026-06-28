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
    'sopr_session': '1e8ccd66bfb0402e',
    'cookieUserID': '8098251',
    '_ym_visorc': 'b',
    '_ym_isad': '1',
    'rrpvid': '77082295317102',
    '_yasc': 'VmTQ6KQLLyBluKSY8jMQwh7eIb1ayWwoXZ6QpiZVdOJ+C0/uPCKR2IpoIiu7bdhlIYm9DqRtUA==.MTc4MDI1OTE2MjE1MQ==',
    '_yasc': '2Dq1+uP3UoGz2VNd/WdC+PFehaij+gWbw0VSgh40745K9/+s0gjpFw8CkmqTtHC2XNn0NjQw0Q==.MTc4MDI2MTM5NjY3Mg==',
    'uxfb_card_satisfaction': '%5B329625786%2C299784235%5D',
    '_ga_3369S417EL': 'GS2.1.s1781510154$o43$g1$t1781510602$j60$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1740731467185025844; _gcl_au=1.1.221627179.1775114569; cookie_agreement_accepted=1; tmr_lvid=5d429d59ad05d69a68419a6b714c0955; tmr_lvidTS=1775114589434; _ga=GA1.1.1494365673.1775114597; uxfb_usertype=searcher; _CIAN_GK=9dad5c1d-1f84-4ff8-afb9-1be8d68b7c80; _ym_d=1776705880; cian_ruid=8098251; uxs_uid=d6ea8010-470f-11f1-a167-7960045d3975; nbrdng_fv=1777837191618; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=3; newbuilding-card-desktop-frontend.consultant_cian_chat_onboarding_shown=1; newbuilding-card-desktop-fichering-frontend.consultant_cian_chat_onboarding_shown=1; frontend-serp.offer_chat_onboarding_shown=1; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; frontend-serp.chatAnimationShownCount=3; frontend-serp.chatAnimationCounter=5; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D4927%26totime%3D2592000; map_preview_onboarding_counter=3; transport-accessibility_onboarding_counter=3; newbuilding-search-frontend.chatAnimationCounter=6; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnewobjects%2Flist%2F%3Fbuilders%255B0%255D%3D17132%26deal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D-1%26show_old_newobjects%3D1; frontend-serp.header_builder_chat_onboarding_shown=1; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; DMIR_AUTH=NljgjqJFspi9B9hsVLvOL%2BN485l2a9rEXksqKNZqXrAYN9mp0xFbnrmllZXUXxTJ0ECVZaPNbRxkfUgWCr8zfaHnKwYJd89t5UVlGfOHwISanLF%2BxErUpPcKTPI3eN9rzbOZLukbDk0n58Qs9wtu%2BWbFT%2FlGQ6lN%2BRPE4cU6TNg%3D; countCallNowPopupShowed=2%3A1780486387527; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; forever_region_id=4606; session_region_id=4606; session_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_main_town_region_id=4959; forever_main_town_region_id=4959; sopr_session=1e8ccd66bfb0402e; cookieUserID=8098251; _ym_visorc=b; _ym_isad=1; rrpvid=77082295317102; _yasc=VmTQ6KQLLyBluKSY8jMQwh7eIb1ayWwoXZ6QpiZVdOJ+C0/uPCKR2IpoIiu7bdhlIYm9DqRtUA==.MTc4MDI1OTE2MjE1MQ==; _yasc=2Dq1+uP3UoGz2VNd/WdC+PFehaij+gWbw0VSgh40745K9/+s0gjpFw8CkmqTtHC2XNn0NjQw0Q==.MTc4MDI2MTM5NjY3Mg==; uxfb_card_satisfaction=%5B329625786%2C299784235%5D; _ga_3369S417EL=GS2.1.s1781510154$o43$g1$t1781510602$j60$l0$h0',
}

json_data = {
    'jsonQuery': {
        '_type': 'commercialsale',
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
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'coordinates': [
                        [
                            '37.680365',
                            '55.719769',
                        ],
                        [
                            '37.680365',
                            '55.746046',
                        ],
                        [
                            '37.767887',
                            '55.746046',
                        ],
                        [
                            '37.767887',
                            '55.719769',
                        ],
                        [
                            '37.680365',
                            '55.719769',
                        ],
                    ],
                    'name': 'Нижегородский район',
                    'type': 'polygon',
                    'title': 'Москва, Юго-Восточный административный округ, Нижегородский район',
                },
            ],
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

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"jsonQuery":{"_type":"commercialsale","engine_version":{"type":"term","value":2},"region":{"type":"terms","value":[1]},"geo":{"type":"geo","value":[{"coordinates":[["37.680365","55.719769"],["37.680365","55.746046"],["37.767887","55.746046"],["37.767887","55.719769"],["37.680365","55.719769"]],"name":"Нижегородский район","type":"polygon","title":"Москва, Юго-Восточный административный округ, Нижегородский район"}]},"office_type":{"type":"terms","value":[1]},"page":{"type":"term","value":2}},"_liquiditySource":"web_commercial-serp"}'.encode()
#response = requests.post(
#    'https://api.cian.ru/commercial-search-offers/desktop/v1/offers/get-offers/',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



current_date = datetime.date.today()

region_list = [
    4593, 4588, 4584, 4596, 4606, 4608, 4618, 4560, 4609, 4619, 181462,
    4564, 4581, 4620, 4607, 4557, 4623, 4612, 4573, 4598, 4585, 4555,
    4567, 4621, 4587, 4605, 4568, 4625, 184723, 4604, 4576, 4574, 4603,
    4602, 4562, 4561, 4565, 4601, 4636, 4599, 4629, 4580, 4630, 4572,
    4615, 4614, 4591, 4553, 4635, 4624, 4570, 4583, 4566, 4600, 4554,
    4556, 4558, 4563, 4569, 5053, 4571, 4575, 4577, 4578, 4579, 4582,
    4586, 4589, 4590, 4592, 4594, 4595, 4597, 4610, 4611, 4613, 4617,
    4622, 4627, 4628, 4631, 4633, 4634
]

session = requests.Session()

for region in region_list:



    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["region"]["value"][0] = region
    json_data["jsonQuery"]["office_type"]["value"] = [1, 2, 3, 4, 5, 7]
    json_data["jsonQuery"]["offer_seller_type"]["value"] = [2, 3, 1]





    session = requests.Session()

    response = session.post(  # Первичный запрос для определения количества лотов
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        cookies=cookies,
        headers=headers,
        json=json_data
    )

    print(f"Первичный json: {json_data}")

    items_count = response.json()['data']["aggregatedCount"]
    print(f'В регионе {items_count} лотов')

    if items_count <= 1500:

        land_status_ids = [[1,2,3,5,7,11]]
        offer_seller_types = [[1, 2, 3]]

    elif 1500 < items_count < 2500:

        land_status_ids = [[1], [2], [3], [5], [7], [11]]
        offer_seller_types = [[1, 2, 3]]

    elif 2500 <= items_count <= 4500:

        land_status_ids = [[1], [2], [3], [5], [7], [11]]
        offer_seller_types = [[1], [2], [3]]

    elif items_count > 4500:

        land_status_ids = [[1], [2], [3], [5], [7], [11]]
        offer_seller_types = [[1], [2], [3]]

    flats = []
    counter = 1
    total_count = 1


    for land_status in land_status_ids:

        json_data["jsonQuery"]["page"]["value"] = 1
        json_data["jsonQuery"]["office_type"]["value"] = land_status


        for offer_seller_type in offer_seller_types:
            json_data["jsonQuery"]["page"]["value"] = 1
            json_data["jsonQuery"]["offer_seller_type"]["value"] = offer_seller_type
            json_data["jsonQuery"]["page"]["value"] = 1
            print(f'Снимаем регион: {region}')
            print(f"Снимаем land_status: {land_status}")
            print(f"Снимаем offer_seller_type: {offer_seller_type}")

            flats = []

            while True:
                start_time = time.time()
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

                    print(json_data)

                    print(response.status_code)

                    items = response.json()["data"]["offersSerialized"]
                except:
                    print("Произошла ошибка, пробуем ещё раз")
                    print(response.status_code)
                    time.sleep(30)
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
                        url = i['fullUrl'].rstrip('/').rpartition('/')[-1]
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
                total_count = response.json()["data"]["offerCount"]
                downloaded = len(flats)
                print(f'Номер страницы: {json_data["jsonQuery"]["page"]["value"]}')
                print(f'Загружено {downloaded} предложений из {total_count}')
                counter += 1
                if not items:
                    break
                sleep_time = random.uniform(1, 3)
                time.sleep(sleep_time)
                end_time = time.time()
                print(f"Время выполнения: {end_time - start_time:.4f} сек")

            if len(flats) > 0:
                # Базовый путь для сохранения
                base_path = r""

                folder_path = os.path.join(base_path, str(current_date))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                filename = f"Коммерция_продажа_{region}_{land_status}_{offer_seller_type}.xlsx"

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





