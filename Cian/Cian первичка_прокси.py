import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import merge_and_clean, haversine
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

decoration_dict = {'preFine': 'Предчистовая', 'fine': 'С отделкой', 'without': 'Без отделки',
                   'fineWithFurniture': 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

proxies = {
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260"
}

# from itertools import cycle
#
# proxies_list = [
#
#     "http://STm87nUFS6:6StepJYs2y@185.42.27.210:10270",
#
# ]
#
# proxy_pool = cycle(proxies_list)








print(f'Первоначальный IP: {requests.get("https://ipinfo.io/json").json()}')

cookies = {
    '_CIAN_GK': 'ebd70d3a-b0b3-483e-b09f-0f982f2a4eea',
    '_gcl_au': '1.1.96319925.1782933291',
    'tmr_lvid': '3a549fa46199720d5a0041676fe444a9',
    'tmr_lvidTS': '1782933291907',
    '_ga': 'GA1.1.2045904184.1782933294',
    '_ym_uid': '1782933294531685029',
    '_ym_d': '1782933294',
    'uxfb_usertype': 'searcher',
    'WBRMVisitLast_utm': '',
    'WBRMVisitLast_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    'WBRMVisitFirst_utm': '',
    'WBRMVisitFirst_referrer': 'https%3A%2F%2Fwww.google.com%2F',
    'uxs_uid': '246eace0-7581-11f1-b1a1-3b03d0af4385',
    'cookie_agreement_accepted': '1',
    'map_preview_onboarding_counter': '3',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'frontend-serp.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatAnimationShownCount': '1',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    'transport-accessibility_onboarding_counter': '1',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'login_button_tooltip_key': '1',
    'frontend-offer-card.consultant_chat_onboarding_shown': '1',
    'nbrdng_fv': '1786546847550',
    'rrpvid': '938073304451891',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'cian_ruid': '8098251',
    'newbuilding-card-desktop-fichering-frontend.compare_onboarding_shown': '1',
    'frontend-serp.compare_onboarding_shown': '1',
    'newbuilding-card-desktop-frontend.compare_onboarding_shown': '1',
    'newbuilding_compare_onboarding_shown': '1',
    'forever_region_id': '2',
    'forever_region_name': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
    'frontend-serp.chatAnimationShownCount': '81',
    'newbuilding-search-frontend.compare_onboarding_shown': '1',
    'newbuilding-search-frontend.chatAnimationCounter': '4',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnewobjects%2Flist%3Fdeal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D-2%26p%3D2',
    'countCallNowPopupShowed': '2%3A1788111560835',
    'uxfb_card_satisfaction': '%5B327835654%5D',
    'login_mro_popup': '1',
    'session_region_id': '2',
    'session_region_name': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3',
    'session_main_town_region_id': '2',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    '_yasc': 'eKM9hDKO37mm6ym8IHXmpyERL3q5FikiesnLDkIg8GLX3JZAzTyPisB+ZnIc5apo72AEU1rGdQ==',
    'anti_bot': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiYW50aV9ib3QiLCJ2YWx1ZSI6ImV5SnlaVzF2ZEdWZmFYQWlPaUkxTGpJeU9DNHhNVFF1T0RRaWZRPT0iLCJpYXQiOjE3ODgyMDM0ODh9.BsKm4X-2TgnW2OmG9rdqpDH_J8NYKA_EB5HrDAxBAUI',
    '_yasc': '5CtRd5Jzr29eM76aNgWB8X+RXvIuZBPxYd7yn1PxXEmTO4hXf3lZn1y9XRGLkc7BOF9EOV0Xsg==',
    'frontend-serp.chatAnimationPrevPath': '%2Fcat.php%3Fdeal_type%3Dsale%26engine_version%3D2%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26p%3D3%26region%3D2',
    '_ga_3369S417EL': 'GS2.1.s1788203493$o107$g0$t1788203493$j60$l0$h0',
    'frontend-serp.chatAnimationCounter': '87',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://spb.cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://spb.cian.ru/',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=ebd70d3a-b0b3-483e-b09f-0f982f2a4eea; _gcl_au=1.1.96319925.1782933291; tmr_lvid=3a549fa46199720d5a0041676fe444a9; tmr_lvidTS=1782933291907; _ga=GA1.1.2045904184.1782933294; _ym_uid=1782933294531685029; _ym_d=1782933294; uxfb_usertype=searcher; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; uxs_uid=246eace0-7581-11f1-b1a1-3b03d0af4385; cookie_agreement_accepted=1; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; transport-accessibility_onboarding_counter=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; login_button_tooltip_key=1; frontend-offer-card.consultant_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationCounter=2; nbrdng_fv=1786546847550; rrpvid=938073304451891; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; cian_ruid=8098251; newbuilding-card-desktop-fichering-frontend.compare_onboarding_shown=1; frontend-serp.compare_onboarding_shown=1; newbuilding-card-desktop-frontend.compare_onboarding_shown=1; newbuilding_compare_onboarding_shown=1; uxfb_card_satisfaction=%5B326074406%5D; login_mro_popup=1; _ym_isad=2; mdd=1; newbuilding_mortgage_payment_filter_onboarding=1; forever_region_id=2; session_region_id=2; forever_region_name=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3; session_region_name=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3; countCallNowPopupShowed=1%3A1788111560835; session_main_town_region_id=2; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D2%26totime%3D2592000; frontend-serp.chatAnimationShownCount=81; frontend-serp.chatAnimationCounter=82; _yasc=/JlYpxSilpzMPJl7LbxtPejTSANfxPTeGuGuSa8ePINjLDRd9vlBQnPYybHDA9Gc8ORqw8VOMA==; _ga_3369S417EL=GS2.1.s1788123277$o98$g0$t1788123277$j60$l0$h0; _yasc=dCe3lxF5nQZTaUO2dd1izLRqIMQ718gtlGUsDZpnPeDKwbhsA+UOpVKVxaZep6ugPGyDGgzsLA==',
}



newbuilding_classes = [
                'economy',
                'comfort',
                'business',
                'premium',
            ]





cities_dict = {
    'Москва': 1,
    'Санкт-Петербург': 2,
    'Новосибирск': 4897,
    'Екатеринбург': 4743,
    'Казань': 4777,
    'Красноярск': 4827,
    'Нижний Новгород': 4885,
    'Челябинск': 5048,
    'Уфа': 176245,
    'Краснодар': 4820,
    'Самара': 4966,
    'Ростов-на-Дону': 4959,
    'Омск': 4914,
    'Воронеж': 4713,
    'Пермь': 4927,
    'Волгоград': 4704,
    'Тюмень': 5024,
    'Владивосток': 4701
}

cities_list = [4704]

for city_id in cities_list:

    json_data_first = {
        'jsonQuery': {
            'region': {
                'type': 'terms',
                'value': [
                    1,
                ],
            },
            'newbuilding_class': {
                'type': 'terms',
                'value': [
                    'comfort',
                ],
            },
            'from_developer': {
                'type': 'term',
                'value': True,
            },
        },
        'uri': '/newobjects/list?deal_type=sale&engine_version=2&offer_type=newobject&region=5048&p=2',
        'subdomain': 'www',
        'offset': 0,
        'count': 25,
        'userCanUseHiddenBase': False,
    }

    coords = city_centers.get(city_id)

    # noinspection PyTypeChecker
    json_data_first['jsonQuery']['region']['value'] = [city_id]

    ids_dict = {}

    json_data_first['offset'] = 0


    for newbuilding_class in newbuilding_classes:

        json_data_first['jsonQuery']['newbuilding_class']['value'] = [newbuilding_class]
        json_data_first['offset'] = 0

        while True:

            requests.get("https://www.cian.ru/")

            response = requests.post(
                'https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/',
                cookies=cookies,
                headers=headers,
                json=json_data_first,
            )

            print(response.status_code)

            items = response.json()['newbuildings']

            for i in items:
                if i['fromDeveloperPropsCount'] < 1:
                    continue
                id = i['id']
                class_of_building = json_data_first['jsonQuery']['newbuilding_class']['value']
                ids_dict[id] = class_of_building[0]
            if not items:
                break
            json_data_first['offset'] += 25


    ids = list(ids_dict.keys())

    print(ids_dict)
    city_in_work = response.json()['breadcrumbs'][0]['title']
    print(city_in_work)
    print(response.json()['breadcrumbs'][1]['title'])
    print(ids)
    print(f'Количество ЖК: {len(ids)}'      )

    json_data = {
        'jsonQuery': {
            '_type': 'flatsale',
            'sort': {
                'type': 'term',
                'value': 'price_object_order',
            },
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'geo': {
                'type': 'geo',
                'value': [
                    {
                        'type': 'newobject',
                        'id': 4013017,
                    },
                ],
            },
            'decorations_list': {
                'type': 'terms',
                'value': [
                    'preFine',
                ],
            },
            'publish_period': {
                'type': 'term',
                'value': 2592000,
            },
            'floor': {
                'type': 'range',
                'value': {
                    'gte': 1,
                    'lte': 99,
                },
            },
            'from_developer': {
                'type': 'term',
                'value': True,
            },
            'room': {
                'type': 'terms',
                'value': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    9,
                ],
            },
            'page': {
                'type': 'term',
                'value': 1,
            },
        },
        '_liquiditySource': 'web_serp',
    }

    current_date = datetime.date.today()
    # ids = [2812291, 6534, 3690038]
    for y in ids:

        flats = []
        session = requests.Session()
        flats_total = []

        if y in []:
            continue

        print(f"Новый ЖК, {y}, {ids.index(y) + 1} из {len(ids)}")

        json_data['jsonQuery']['room'] = {
            'type': 'terms',
            'value': [1, 2, 3, 4, 5, 6, 7, 9]
        }

        json_data["jsonQuery"]["floor"]["value"]["gte"] = 1
        json_data["jsonQuery"]["floor"]["value"]["lte"] = 99
        json_data["jsonQuery"]["geo"]["value"][0]["id"] = y
        json_data["jsonQuery"]["page"]["value"] = 1
        json_data["jsonQuery"]["decorations_list"]["value"][0] = []

        response = session.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )
        flats_count = response.json()['data']['aggregatedCount']
        print(f'Количество квартир в проекте: {flats_count}')
        time.sleep(1)

        if flats_count > 2500:

            json_data['jsonQuery']['room'] = {
                'type': 'terms',
                'value': [1],
            }
            rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
            total_floor_list = [[1, 3], [4, 7], [8, 12], [13, 17], [18, 23], [24, 30], [31, 40], [41, 200]]

        elif 1500 <= flats_count <= 2500:

            json_data['jsonQuery']['room'] = {
                'type': 'terms',
                'value': [1],
            }
            rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
            total_floor_list = [[1, 200]]

        else:
            del json_data['jsonQuery']['room']
            rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
            total_floor_list = [[1, 200]]

        print(json_data)

        for decoration in decoration_list:

            json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
            json_data["jsonQuery"]["page"]["value"] = 1

            for room_id in rooms_ids:

                json_data["jsonQuery"]["page"]["value"] = 1

                try:
                    json_data["jsonQuery"]["room"]["value"][0] = room_id
                except:
                    ''
                counter = 1
                total_count = 1

                for f in total_floor_list:


                    json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
                    json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
                    json_data["jsonQuery"]["page"]["value"] = 1
                    print(f'Этажи квартир: {f}')

                    name_counter = f'{room_id}-{f[0]}-{f[1]}-{decoration}'

                    while True:

                        print(f"Число комнат: {room_id}")
                        if counter > 1:
                            sleep_time = random.uniform(2, 4)
                            # time.sleep(sleep_time)
                        try:
                            response = session.post(
                                'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                                cookies=cookies,
                                headers=headers,
                                json=json_data,
                                proxies=proxies
                            )

                            print(response.status_code)
                            # print(f'IP через прокси: {requests.get("https://ipinfo.io/json", proxies=proxies).json()}')



                            items = response.json()["data"]["offersSerialized"]

                        except:

                            print("Произошла ошибка, пробуем ещё раз")
                            time.sleep(7)
                            session = requests.Session()

                            retry = Retry(
                                total=5,
                                backoff_factor=1,
                                status_forcelist=[429, 500, 502, 503, 504],
                            )

                            adapter = HTTPAdapter(max_retries=retry)

                            session.mount("http://", adapter)
                            session.mount("https://", adapter)

                            response = session.post(
                                'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                                cookies=cookies,
                                headers=headers,
                                json=json_data,
                                proxies=proxies,
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
                                if i['building']['deadline']['isComplete']:
                                    srok_sdachi = "Дом сдан"
                                elif i['building']['deadline']['quarterEnd'] is None and i['building']['deadline'][
                                    'year'] is None:
                                    srok_sdachi = ''
                                else:
                                    srok_sdachi = f"Cдача ГК: {i['newbuilding']['house']['finishDate']['quarter']} квартал, {i['newbuilding']['house']['finishDate']['year']} года".replace(
                                        'None', '')
                            except:
                                srok_sdachi = ''
                            try:
                                url = i['fullUrl'].rstrip('/').rpartition('/')[-3]
                            except:
                                url = ''

                            try:
                                if i['isApartments']:
                                    type = "Апартаменты"
                                else:
                                    type = "Квартира"
                            except:
                                type = ''

                            try:
                                price = i['bargainTerms']['priceRur']
                            except:
                                price = ''
                            try:
                                project = i['geo']['jk']['displayName'].replace('ЖК ', '').replace('«', '').replace('»', '')
                            except:
                                project = ''
                            # try:
                            #   if i['decoration'] == "fine":
                            #      finish_type = "С отделкой"
                            #    elif i['decoration'] == "without" or i['decoration'] == "rough":
                            #       finish_type = "Без отделки"
                            #   else:
                            #      finish_type = i['decoration']
                            # except:
                            #   finish_type = ''
                            # if not finish_type:
                            #    finish_type = classify_renovation(i['description'])
                            try:
                                finish_type = decoration_dict.get(decoration)
                            except:
                                finish_type = 'Не определён'

                            try:
                                adress = i['geo']['userInput']
                            except:
                                adress = ""

                            try:
                                korpus = i["geo"]["jk"]["house"]["name"]
                            except:
                                korpus = ''

                            try:
                                developer = i['geo']['jk']['developer']['name']
                            except:
                                developer = ""

                            try:
                                if i["roomsCount"] is None:
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
                            try:
                                added = i['added']
                            except:
                                added = ''
                            try:
                                kitchenArea = float(i['kitchenArea'])
                            except:
                                kitchenArea = 0
                            try:
                                livingArea = float(i['livingArea'])
                            except:
                                livingArea = 0
                            try:
                                parking = i['building']['parking']['type']
                            except:
                                parking = ''
                            try:
                                balconiesCount = int(i['balconiesCount'])
                            except:
                                balconiesCount = 0
                            try:
                                loggiasCount = int(i['loggiasCount'])
                            except:
                                loggiasCount = 0
                            balconies_and_loggias_count = balconiesCount + loggiasCount
                            try:

                                lat_jk = i['geo']['coordinates']['lat']
                                lon_jk = i['geo']['coordinates']['lng']
                                lat_center = coords["lat_center"]
                                lon_center = coords["lon_center"]
                                distance = round(haversine(lat_jk, lon_jk, lat_center, lon_center), 2)

                            except:
                                distance = ''
                            class_of_jk = ids_dict.get(y, '').replace('economy', 'Комфорт').replace('comfort', 'Комфорт').replace('business', 'Бизнес').replace('premium', 'Премиум')

                            print(
                                f"{project}, {url}, класс: {class_of_jk}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                            result = [project, developer, class_of_jk, location, location2, okrug, raion, mikroraion, metro, street, house, korpus, distance, srok_sdachi, type,
                                      finish_type, room_count, area, kitchenArea, livingArea, price, floor,
                                      balconies_and_loggias_count, parking, url]
                            flats.append(result)
                            flats_total.append(result)

                        if not items:
                            break
                        json_data["jsonQuery"]["page"]["value"] += 1
                        print(len(flats))
                        print("-----------------------------------------------------------------------------")
                        total_count = response.json()["data"]["offerCount"]
                        downloaded = len(flats)
                        print(
                            f'ID ЖК: {y}, {ids.index(y) + 1} из {len(ids)}. Загружено {downloaded} предложений из {total_count}')
                        counter += 1

        if len(flats_total) > 1:

            df = pd.DataFrame(flats_total, columns=['Название проекта',
                                                    'Девелопер',
                                                    'Класс',
                                                    'Локация',
                                                    'Локация2',
                                                              'Округ',
                                                              'Район',
                                                              'Микрорайон',
                                                              'Метро',
                                                              'Улица',
                                                              'Дом',
                                                    'Корпус',
                                                    'Расстояние до центра, км',
                                                    'Срок сдачи',
                                                    'Тип помещения',
                                                    'Отделка',
                                                    'Кол-во комнат',
                                                    'Площадь, кв.м',
                                                    'Площадь кухни, кв.м',
                                                    'Жилая площадь, кв.м',
                                                    'Цена лота, руб.',
                                                    'Этаж',
                                                    'Балконы/лоджии',
                                                    'Паркинг',
                                                    'Ссылка'
                                                    ])

            current_date = datetime.date.today()

            # Базовый путь для сохранения
            base_path = r""

            folder_path = os.path.join(base_path, 'Первичка', str(current_date))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)


            def sanitize_filename(name):
                for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                    name = name.replace(char, '_')
                return name


            project = sanitize_filename(project)
            filename = f"{city_id}_{project}__{current_date}_{name_counter}.xlsx"

            # Полный путь к файлу0
            file_path = os.path.join(folder_path, filename)

            # Сохранение файла в папку
            try:
                df.to_excel(file_path, index=False)
            except:
                filename = f"{city_id}_{project}_{current_date}_2.xlsx"
                file_path = os.path.join(folder_path, filename)
                df.to_excel(file_path, index=False)

# merge_and_clean(folder_path, f'Первичка_{city_in_work}_{current_date}.xlsx')
