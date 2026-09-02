import requests
import datetime
import time
import pandas as pd
import os
import random

from jedi.api import file_name

from functions import merge_and_clean, haversine
import json

# noinspection PyDictDuplicateKeys
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
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnovostroyki%2F',
    'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatAnimationShownCount': '1',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    'transport-accessibility_onboarding_counter': '1',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'login_button_tooltip_key': '1',
    'frontend-offer-card.consultant_chat_onboarding_shown': '1',
    'newbuilding-search-frontend.chatAnimationCounter': '2',
    'nbrdng_fv': '1786546847550',
    'rrpvid': '938073304451891',
    'frontend-serp.chatAnimationPrevPath': '%2Fkupit-kvartiru-novostroyki-krasnodarskiy-kray-sochi-gorodskoy-okrug%2F',
    'frontend-serp.chatAnimationCounter': '75',
    'frontend-serp.chatAnimationShownCount': '75',
    'countCallNowPopupShowed': '1%3A1786997542942',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    '_yasc': 'Wiajr9ZLYqzNfsnMxWbY4f3nH/4tPD5PdvqYV6A2x+Stw9i1YJJaC49KofvwUIxs35ndBPnjIg==',
    '_yasc': 'vGLYQRwRTIBQpoL2XWmYuwTJsFTh8ufz9e6KiBxmM6YcQOIAAInObgoxtTA2O9b2Euy46x1y5Q==',
    'login_mro_popup': '1',
    'sopr_session': 'b80f654a16d740c2',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'mdd': '1',
    'forever_region_id': '-1',
    'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'session_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'session_region_id': '1',
    'session_main_town_region_id': '1',
    '_ga_3369S417EL': 'GS2.1.s1787295947$o71$g1$t1787297182$j53$l0$h0',
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
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=ebd70d3a-b0b3-483e-b09f-0f982f2a4eea; _gcl_au=1.1.96319925.1782933291; tmr_lvid=3a549fa46199720d5a0041676fe444a9; tmr_lvidTS=1782933291907; _ga=GA1.1.2045904184.1782933294; _ym_uid=1782933294531685029; _ym_d=1782933294; uxfb_usertype=searcher; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; uxs_uid=246eace0-7581-11f1-b1a1-3b03d0af4385; cookie_agreement_accepted=1; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; transport-accessibility_onboarding_counter=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; login_button_tooltip_key=1; frontend-offer-card.consultant_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationCounter=2; nbrdng_fv=1786546847550; rrpvid=938073304451891; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki-krasnodarskiy-kray-sochi-gorodskoy-okrug%2F; frontend-serp.chatAnimationCounter=75; frontend-serp.chatAnimationShownCount=75; countCallNowPopupShowed=1%3A1786997542942; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; _yasc=Wiajr9ZLYqzNfsnMxWbY4f3nH/4tPD5PdvqYV6A2x+Stw9i1YJJaC49KofvwUIxs35ndBPnjIg==; _yasc=vGLYQRwRTIBQpoL2XWmYuwTJsFTh8ufz9e6KiBxmM6YcQOIAAInObgoxtTA2O9b2Euy46x1y5Q==; login_mro_popup=1; sopr_session=b80f654a16d740c2; _ym_isad=2; _ym_visorc=b; mdd=1; forever_region_id=-1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1787295947$o71$g1$t1787297182$j53$l0$h0',
}

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
                    'type': 'polygon',
                    'name': 'Выделенная область',
                    'coordinates': [
                        [
                            '37.5321932',
                            '55.7511543',
                        ],
                        [
                            '37.5321503',
                            '55.7514448',
                        ],
                        [
                            '37.5321503',
                            '55.7517594',
                        ],
                        [
                            '37.5323863',
                            '55.7520257',
                        ],
                        [
                            '37.5328369',
                            '55.752183',
                        ],
                        [
                            '37.5333304',
                            '55.7522677',
                        ],
                        [
                            '37.5338669',
                            '55.7522798',
                        ],
                        [
                            '37.5344248',
                            '55.7522798',
                        ],
                        [
                            '37.5349612',
                            '55.7522677',
                        ],
                        [
                            '37.5354762',
                            '55.7522556',
                        ],
                        [
                            '37.5359912',
                            '55.7522435',
                        ],
                        [
                            '37.5365062',
                            '55.752183',
                        ],
                        [
                            '37.5370855',
                            '55.7521104',
                        ],
                        [
                            '37.5375576',
                            '55.7519773',
                        ],
                        [
                            '37.5380297',
                            '55.7518563',
                        ],
                        [
                            '37.5385876',
                            '55.75182',
                        ],
                        [
                            '37.5391026',
                            '55.7518442',
                        ],
                        [
                            '37.5396175',
                            '55.7518321',
                        ],
                        [
                            '37.540154',
                            '55.7517352',
                        ],
                        [
                            '37.5406904',
                            '55.7516505',
                        ],
                        [
                            '37.5412483',
                            '55.7515779',
                        ],
                        [
                            '37.5417633',
                            '55.7515174',
                        ],
                        [
                            '37.5422997',
                            '55.7515295',
                        ],
                        [
                            '37.5427718',
                            '55.7516505',
                        ],
                        [
                            '37.5431366',
                            '55.7518563',
                        ],
                        [
                            '37.5430078',
                            '55.7521467',
                        ],
                        [
                            '37.5429864',
                            '55.7524372',
                        ],
                        [
                            '37.5432653',
                            '55.7526913',
                        ],
                        [
                            '37.5437159',
                            '55.7528608',
                        ],
                        [
                            '37.5442309',
                            '55.7529818',
                        ],
                        [
                            '37.5447245',
                            '55.7530786',
                        ],
                        [
                            '37.5452824',
                            '55.7531512',
                        ],
                        [
                            '37.5457759',
                            '55.7532602',
                        ],
                        [
                            '37.5463123',
                            '55.7533812',
                        ],
                        [
                            '37.5468059',
                            '55.753478',
                        ],
                        [
                            '37.5473208',
                            '55.7535385',
                        ],
                        [
                            '37.5479002',
                            '55.7535385',
                        ],
                        [
                            '37.5484366',
                            '55.7533812',
                        ],
                        [
                            '37.5488443',
                            '55.7531754',
                        ],
                        [
                            '37.5492091',
                            '55.7529697',
                        ],
                        [
                            '37.5495524',
                            '55.7527518',
                        ],
                        [
                            '37.5499172',
                            '55.7524856',
                        ],
                        [
                            '37.550282',
                            '55.7522677',
                        ],
                        [
                            '37.5506253',
                            '55.7520499',
                        ],
                        [
                            '37.5508828',
                            '55.7517957',
                        ],
                        [
                            '37.5510759',
                            '55.7515174',
                        ],
                        [
                            '37.551033',
                            '55.7512269',
                        ],
                        [
                            '37.5507326',
                            '55.7509849',
                        ],
                        [
                            '37.5503678',
                            '55.7507549',
                        ],
                        [
                            '37.5499387',
                            '55.7505613',
                        ],
                        [
                            '37.5495524',
                            '55.7503555',
                        ],
                        [
                            '37.5491447',
                            '55.750174',
                        ],
                        [
                            '37.5487156',
                            '55.7499925',
                        ],
                        [
                            '37.548265',
                            '55.7497746',
                        ],
                        [
                            '37.5477929',
                            '55.7495568',
                        ],
                        [
                            '37.5473638',
                            '55.7493873',
                        ],
                        [
                            '37.5469131',
                            '55.7492058',
                        ],
                        [
                            '37.5464625',
                            '55.7490364',
                        ],
                        [
                            '37.5460334',
                            '55.7488669',
                        ],
                        [
                            '37.5456042',
                            '55.7486975',
                        ],
                        [
                            '37.5451536',
                            '55.7484918',
                        ],
                        [
                            '37.5447459',
                            '55.7483102',
                        ],
                        [
                            '37.5442095',
                            '55.7480319',
                        ],
                        [
                            '37.5437803',
                            '55.7478624',
                        ],
                        [
                            '37.5433297',
                            '55.7476809',
                        ],
                        [
                            '37.5428791',
                            '55.7474993',
                        ],
                        [
                            '37.5424499',
                            '55.7473057',
                        ],
                        [
                            '37.5419779',
                            '55.7471484',
                        ],
                        [
                            '37.5415058',
                            '55.746991',
                        ],
                        [
                            '37.5410552',
                            '55.7468216',
                        ],
                        [
                            '37.5405831',
                            '55.7466764',
                        ],
                        [
                            '37.5400896',
                            '55.7465553',
                        ],
                        [
                            '37.5395532',
                            '55.7464585',
                        ],
                        [
                            '37.5389953',
                            '55.7464101',
                        ],
                        [
                            '37.5384374',
                            '55.7464101',
                        ],
                        [
                            '37.5379224',
                            '55.7464343',
                        ],
                        [
                            '37.5373859',
                            '55.7464585',
                        ],
                        [
                            '37.536828',
                            '55.7465553',
                        ],
                        [
                            '37.5363131',
                            '55.7466885',
                        ],
                        [
                            '37.5358624',
                            '55.7468579',
                        ],
                        [
                            '37.5353689',
                            '55.7469426',
                        ],
                        [
                            '37.5348325',
                            '55.7470394',
                        ],
                        [
                            '37.5344248',
                            '55.7472331',
                        ],
                        [
                            '37.5341458',
                            '55.7474872',
                        ],
                        [
                            '37.5338454',
                            '55.7477293',
                        ],
                        [
                            '37.533545',
                            '55.7479713',
                        ],
                        [
                            '37.5332875',
                            '55.7482618',
                        ],
                        [
                            '37.5329871',
                            '55.7485523',
                        ],
                        [
                            '37.5328798',
                            '55.7488427',
                        ],
                        [
                            '37.5327511',
                            '55.7491453',
                        ],
                        [
                            '37.5326652',
                            '55.7494357',
                        ],
                        [
                            '37.5325794',
                            '55.7497504',
                        ],
                        [
                            '37.5324936',
                            '55.7500409',
                        ],
                        [
                            '37.5324078',
                            '55.7503313',
                        ],
                        [
                            '37.5323434',
                            '55.7506218',
                        ],
                        [
                            '37.5322361',
                            '55.7509244',
                        ],
                        [
                            '37.5321503',
                            '55.7512148',
                        ],
                        [
                            '37.5321932',
                            '55.7511543',
                        ],
                    ],
                },
            ],
        },
        'bbox': {
            'type': 'term',
            'value': [
                [
                    37.5266197109,
                    55.7454979228,
                ],
                [
                    37.5678184414,
                    55.7542115852,
                ],
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 99,
            },
        },
        'repair': {
            'type': 'terms',
            'value': [
                1,
                2,
                3,
                4,
            ],
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
        'building_status': {
            'type': 'term',
            'value': 1,
        },
    },
    '_liquiditySource': 'web_serp',
}

print(f'Первоначальный IP: {requests.get("https://ipinfo.io/json").json()}')

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
    'Волгоград': 4704
}


print("Список доступных регионов:")
for city, city_id in cities_dict.items():
    print(f"{city}: {city_id}")

user_input = input("\nВведите ID нужного региона или введите свой: ")

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

coords = city_centers.get(user_input)

try:
    user_id = int(user_input)
    if user_id in cities_dict.values():
        selected_city = [city for city, cid in cities_dict.items() if cid == user_id][0]
        print(f"\nВы выбрали город: {selected_city}")
    else:
        print("\nГород не в списке")
except ValueError:
    print("\nОшибка: введите числовой ID.")

json_data['jsonQuery']['region']['value'] = [user_input]

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

start_time = time.time()
current_date = datetime.date.today()

repair_ids = [1, 2, 3, 4]
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
city_in_work = response.json()['data']['breadcrumbs'][0]['title']
print(city_in_work)

json_data["jsonQuery"]["repair"]["value"] = [1]

if items_count <= 2000:

    rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 100]]

elif 2500 <= items_count <= 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 6], [7, 12], [13, 200]]

elif items_count > 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 3], [4, 7], [8, 15], [16, 200]]


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
            counter = 1
            total_count = 1



            while len(flats) < total_count:

                if counter > 1:
                    sleep_time = random.uniform(3, 5)
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
                    time.sleep(15)
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

                    new_result = {
                        ('mikroraion' if isinstance(v, str) and 'мкр' in v else k): v
                        for k, v in result.items()
                    }
                    result = new_result
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
                        finish_type = repair_ids_dict.get(repair_id)
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

                    year_of_build = i['building']['buildYear']

                    print(
                        f"{url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                    result = [project, developer, location, location2, okrug, raion, mikroraion, metro, street, house,
                              korpus, distance, srok_sdachi, type,
                              finish_type, room_count, area, kitchenArea, livingArea, price, floor,
                              balconies_and_loggias_count, parking, year_of_build, url]
                    flats.append(result)

                if not items:
                    break
                json_data["jsonQuery"]["page"]["value"] += 1
                print(len(flats))
                print("-----------------------------------------------------------------------------")
                total_count = response.json()["data"]["offerCount"]
                downloaded = len(flats)
                print()
                counter += 1

            if len(flats) > 1:

                df = pd.DataFrame(flats, columns=['Название проекта',
                                                        'Девелопер',
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
                                                        'Год постройки',
                                                        'Ссылка'
                                                        ])

                current_date = datetime.date.today()

                # Базовый путь для сохранения
                base_path = r""

                folder_path = os.path.join(base_path, str(current_date))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)


                def sanitize_filename(name):
                    for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                        name = name.replace(char, '_')
                    return name


                project = sanitize_filename(project)
                filename = f"{city_in_work}__{current_date}_{name_counter}.xlsx"

                # Полный путь к файлу0
                file_path = os.path.join(folder_path, filename)

                # Сохранение файла в папку
                try:
                    df.to_excel(file_path, index=False)
                    print(f'Сохранён файл {file_path}')
                except:
                    filename = f"{project}_{current_date}_2.xlsx"
                    file_path = os.path.join(folder_path, filename)
                    df.to_excel(file_path, index=False)

merge_and_clean(folder_path, f'Вторичка_{city_in_work}_{current_date}.xlsx')
