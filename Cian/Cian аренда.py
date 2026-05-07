import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import haversine

proxies = {
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260"
}

'''

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

'''

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

coords = city_centers.get("1")

ids = [4629063,
       ]  # id ЖК для парсинга



cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    '_ym_uid': '174161324651361127',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrdel': '1744094487237',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
    'ma_id': '6225667261741613246584',
    '__ai_fp_uuid': '245d903c22bdc927%3A15',
    '_gcl_au': '1.1.9818463.1769411842',
    '_ym_d': '1773209373',
    '_ga': 'GA1.1.1538482319.1774343544',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'transport-accessibility_onboarding_counter': '3',
    'uxs_uid': '92604860-28f8-11f1-a98a-bba19a4d4807',
    'uxfb_usertype': 'searcher',
    'cookie_agreement_accepted': '1',
    'newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown': '1',
    'map_preview_onboarding_counter': '3',
    'login_button_tooltip_key': '1',
    'frontend-serp.header_builder_chat_onboarding_shown': '1',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:205657295806|ad:1889238602131455357|grp:5657295806|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=|205657295806&utm_campaign=b2c_nov_mskmo_perf_mix_search_dsa_feed_general_drr_arwm_703812141&etext=2202.h07M9Tlhg3N9CwbhNMoyrVsLWbdrg5CRpbuLNhiEcIVoTY8yPfNz7DVvSxFMf63mtQfzGVZPsUeL_PUMqGvCe3BsenN6dGFxZmZlYWRmaWY.c0ab089525eaca3735ee4aa1b318395f0703704e&yclid=3873403374751711231',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'frontend-serp.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatAnimationShownCount': '107',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'frontend-serp.chatAnimationShownCount': '7',
    'newbuilding-search-frontend.chatAnimationCounter': '111',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnovostroyki%2F',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    'frontend-serp.chatAnimationCounter': '10',
    'frontend-serp.chatAnimationPrevPath': '%2Fkupit-kvartiru-novostroyki%2F',
    'countCallNowPopupShowed': '1%3A1775476258941',
    'login_mro_popup': '1',
    '_ym_isad': '2',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'sopr_session': 'fae946ecf38d45c1',
    '_ym_visorc': 'b',
    '_yasc': 'Tu+m1q51YcAao8zTF2cf67U43ADqBoQ2GvzS377VQlrkNNWUkSDfT5ZafajKHuXa9xnEHv8=',
    '_yasc': 'cmWqSE81taufl30qdvZxf3jt2BVKotcz9wCSqQfsvbkWhkJOHrkyhpe0LM1DdhTbX+b00Vk=',
    'session_region_id': '1',
    'session_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'forever_region_id': '1',
    'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'session_main_town_region_id': '1',
    '_ga_3369S417EL': 'GS2.1.s1775570514$o35$g1$t1775570874$j12$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; _ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; transport-accessibility_onboarding_counter=3; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:205657295806|ad:1889238602131455357|grp:5657295806|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=|205657295806&utm_campaign=b2c_nov_mskmo_perf_mix_search_dsa_feed_general_drr_arwm_703812141&etext=2202.h07M9Tlhg3N9CwbhNMoyrVsLWbdrg5CRpbuLNhiEcIVoTY8yPfNz7DVvSxFMf63mtQfzGVZPsUeL_PUMqGvCe3BsenN6dGFxZmZlYWRmaWY.c0ab089525eaca3735ee4aa1b318395f0703704e&yclid=3873403374751711231; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=107; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatAnimationShownCount=7; newbuilding-search-frontend.chatAnimationCounter=111; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; frontend-serp.chatAnimationCounter=10; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki%2F; countCallNowPopupShowed=1%3A1775476258941; login_mro_popup=1; _ym_isad=2; newbuilding_mortgage_payment_filter_onboarding=1; sopr_session=fae946ecf38d45c1; _ym_visorc=b; _yasc=Tu+m1q51YcAao8zTF2cf67U43ADqBoQ2GvzS377VQlrkNNWUkSDfT5ZafajKHuXa9xnEHv8=; _yasc=cmWqSE81taufl30qdvZxf3jt2BVKotcz9wCSqQfsvbkWhkJOHrkyhpe0LM1DdhTbX+b00Vk=; session_region_id=1; session_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; forever_region_id=1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1775570514$o35$g1$t1775570874$j12$l0$h0',
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
    '_liquiditySource': 'web_serp',
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
                        json=json_data,
                        proxies=proxies,
                    )

items_count = response.json()['data']["aggregatedCount"]
print(f'В городе {items_count} лотов')


if items_count <=  1500:

    rooms_ids = [[1, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [[1], [9]]
    total_floor_list = [[1, 100]]

elif 2500 <= items_count <= 4500:

    rooms_ids = [[1], [9]]
    total_floor_list = [[1, 6], [7, 12], [13, 200]]

elif items_count > 4500:

    rooms_ids = [[1]]
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
                    sleep_time = random.uniform(1, 2)
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
                    time.sleep(5)
                    session = requests.Session()
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
                        url = i['fullUrl'].rstrip('/').rpartition('/')[-3]
                    except:
                        url = ''
                    try:
                        price = i['bargainTerms']['priceRur']
                    except:
                        price = ''

                    try:
                        adress = i['geo']['userInput']
                    except:
                        adress = ""

                    try:
                        area = float(i["totalArea"])
                    except:
                        area = ''
                    try:
                        rooms = i['roomsCount']
                        if not rooms:
                            rooms = 0
                    except:
                        rooms = ''

                    try:

                        lat_jk = i['geo']['coordinates']['lat']
                        lon_jk = i['geo']['coordinates']['lng']
                        lat_center = coords["lat_center"]
                        lon_center = coords["lon_center"]
                        distance = round(haversine(lat_jk, lon_jk, lat_center, lon_center), 2)

                    except:
                        distance = ''

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
                        finish_type = repair_ids_dict.get(repair_id)
                    except:
                        finish_type = 'Неизвестно'

                    date = datetime.date.today()

                    print(
                        f"{location}, {location2}, {okrug}, {raion}, площадь: {area}, цена: {price}, {url}")
                    result = [date, location, location2, okrug, raion, mikroraion, metro, street, house, url, adress, distance, area, kitchenArea, livingArea, balconies_and_loggias_count,
                              price, rooms, finish_type]
                    flats.append(result)

                json_data["jsonQuery"]["page"]["value"] += 1
                print("-----------------------------------------------------------------------------")
                total_count = response.json()["data"]["offerCount"]
                downloaded = len(flats)
                print(f'Загружено {downloaded} предложений из {total_count}')
                counter += 1
                if not items:
                    break



            # Базовый путь для сохранения
            base_path = r""

            folder_path = os.path.join(base_path, str(current_date))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            df = pd.DataFrame(flats, columns=['Дата обновления',
                                              'Локация',
                                              'Локация2',
                                                          'Округ',
                                                          'Район',
                                                          'Микрорайон',
                                                          'Метро',
                                                          'Улица',
                                                          'Дом',

                                              'Ссылка',
                                              'Адрес',
                                              'Расстояние до центра, км',

                                              'Площадь, кв.м',
                                              'Площадь кухни, кв.м',
                                              'Жилая площадь, кв.м',
                                              'Балконы/лоджии',
                                              'Цена за месяц',
                                              'Кол-во комнат',
                                              'Отделка'
                                              ])

            current_date = datetime.date.today()

            # Базовый путь для сохранения
            base_path = r""

            folder_path = os.path.join(base_path, str(current_date))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"Аренда_{json_data['jsonQuery']['region']['value']}_{json_data['jsonQuery']['room']['value']}_{json_data['jsonQuery']['floor']['value']['lte']}_{json_data['jsonQuery']['repair']['value']}_{current_date}.xlsx"

            # Полный путь к файлу
            file_path = os.path.join(folder_path, filename)

            # Сохранение файла в папку
            df.to_excel(file_path, index=False)
