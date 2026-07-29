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
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270"
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
    'countCallNowPopupShowed': '2%3A1774604089870',
    'newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown': '1',
    'map_preview_onboarding_counter': '3',
    'login_button_tooltip_key': '1',
    'frontend-serp.header_builder_chat_onboarding_shown': '1',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:205657295806|ad:1889238602131455357|grp:5657295806|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=|205657295806&utm_campaign=b2c_nov_mskmo_perf_mix_search_dsa_feed_general_drr_arwm_703812141&etext=2202.h07M9Tlhg3N9CwbhNMoyrVsLWbdrg5CRpbuLNhiEcIVoTY8yPfNz7DVvSxFMf63mtQfzGVZPsUeL_PUMqGvCe3BsenN6dGFxZmZlYWRmaWY.c0ab089525eaca3735ee4aa1b318395f0703704e&yclid=3873403374751711231',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'newbuilding-search-frontend.chatAnimationShownCount': '0',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'newbuilding-search-frontend.chatAnimationCounter': '105',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnovostroyki-ot-zastroyschikov%2F',
    '_ym_isad': '2',
    '_yasc': 'UIbNcWUdyuf0EKgvw8Nq7kQLpqY96efYdlowvRcjBUUSYjpsemyKQRq9kkvAZ2trPg==',
    'session_region_id': '5048',
    'forever_region_id': '5048',
    'session_region_name': '%D0%A7%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_region_name': '%D0%A7%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'session_main_town_region_id': '5048',
    'forever_main_town_region_id': '5048',
    'login_mro_popup': '1',
    '_yasc': 'qT+ZIRInbFfq0ln+TcuewZG60b7DDAe6Po+YZr9KOM2loXMhX7p/LqFGNgNPgdWbtg==',
    'sopr_session': 'a1796f7b14a04d82',
    '_ym_visorc': 'b',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'frontend-serp.chatTooltipAnimationShown': '1',
    'frontend-serp.chatAnimationShownCount': '1',
    'frontend-serp.chatAnimationCounter': '3',
    'frontend-serp.chatAnimationPrevPath': '%2Fcat.php%3Fdeal_type%3Dsale%26engine_version%3D2%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26p%3D2%26region%3D5048',
    '_ga_3369S417EL': 'GS2.1.s1775203684$o23$g1$t1775203826$j49$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://chelyabinsk.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://chelyabinsk.cian.ru/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; _ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; transport-accessibility_onboarding_counter=3; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; countCallNowPopupShowed=2%3A1774604089870; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:205657295806|ad:1889238602131455357|grp:5657295806|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=|205657295806&utm_campaign=b2c_nov_mskmo_perf_mix_search_dsa_feed_general_drr_arwm_703812141&etext=2202.h07M9Tlhg3N9CwbhNMoyrVsLWbdrg5CRpbuLNhiEcIVoTY8yPfNz7DVvSxFMf63mtQfzGVZPsUeL_PUMqGvCe3BsenN6dGFxZmZlYWRmaWY.c0ab089525eaca3735ee4aa1b318395f0703704e&yclid=3873403374751711231; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; newbuilding-search-frontend.chatAnimationShownCount=0; newbuilding-search-frontend.builder_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationCounter=105; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki-ot-zastroyschikov%2F; _ym_isad=2; _yasc=UIbNcWUdyuf0EKgvw8Nq7kQLpqY96efYdlowvRcjBUUSYjpsemyKQRq9kkvAZ2trPg==; session_region_id=5048; forever_region_id=5048; session_region_name=%D0%A7%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_region_name=%D0%A7%D0%B5%D0%BB%D1%8F%D0%B1%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_main_town_region_id=5048; forever_main_town_region_id=5048; login_mro_popup=1; _yasc=qT+ZIRInbFfq0ln+TcuewZG60b7DDAe6Po+YZr9KOM2loXMhX7p/LqFGNgNPgdWbtg==; sopr_session=a1796f7b14a04d82; _ym_visorc=b; newbuilding_mortgage_payment_filter_onboarding=1; frontend-serp.chatTooltipAnimationShown=1; frontend-serp.chatAnimationShownCount=1; frontend-serp.chatAnimationCounter=3; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26engine_version%3D2%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26p%3D2%26region%3D5048; _ga_3369S417EL=GS2.1.s1775203684$o23$g1$t1775203826$j49$l0$h0',
}
rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
flats_total = []
flats = []
newbuilding_classes = [
                'economy',
                'comfort',
                'business',
                'premium',
            ]


json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                1,
                4593,
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
        'page': {
            'type': 'term',
            'value': 1,
        },
        'description_include': {
            'type': 'terms',
            'value': [
                'с террасой',
                'терраса',
            ],
        },
        'building_status': {
            'type': 'term',
            'value': 2,
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'decorations_list': {
            'type': 'terms',
            'value': [
                'preFine',
            ],
        },
    },
    '_liquiditySource': 'web_serp',
}

current_date = datetime.date.today()
session = requests.Session()
counter = 1
total_count = 1

for decoration in decoration_list:

    json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
    json_data["jsonQuery"]["page"]["value"] = 1
    print(decoration)



    while True:

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
            class_of_jk = ''

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
        print(f'Всего лотов: {total_count}')
        downloaded = len(flats)
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
    filename = f"Разовая_выгрузка__{current_date}.xlsx"

    # Полный путь к файлу0
    file_path = os.path.join(folder_path, filename)

    # Сохранение файла в папку
    df.to_excel(file_path, index=False)

# merge_and_clean(folder_path, f'Первичка_{city_in_work}_{current_date}.xlsx')
