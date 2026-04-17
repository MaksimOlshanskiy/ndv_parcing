import requests
import datetime
import time
import pandas as pd
import os
import random
from functions import merge_and_clean, haversine
import json



# noinspection PyDictDuplicateKeys
cookies = {
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
    'uxs_uid': '92604860-28f8-11f1-a98a-bba19a4d4807',
    'uxfb_usertype': 'searcher',
    'cookie_agreement_accepted': '1',
    'newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown': '1',
    'map_preview_onboarding_counter': '3',
    'login_button_tooltip_key': '1',
    'frontend-serp.header_builder_chat_onboarding_shown': '1',
    'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
    'frontend-serp.chatTooltipAnimationShown': '1',
    'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775',
    '_CIAN_GK': '8421b1d7-727f-42ac-9f77-a0ed1f26ad1b',
    'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1776238374488',
    'newbuilding-search-frontend.chatAnimationShownCount': '122',
    'countCallNowPopupShowed': '2%3A1776238384809',
    'sopr_utm': '%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'login_mro_popup': '1',
    'newbuilding-search-frontend.chatAnimationCounter': '124',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnewobjects%2Flist%2F%3Fdeal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D4973',
    'uxfb_card_satisfaction': '%5B297124173%2C313319705%5D',
    'frontend-serp.chatAnimationPrevPath': '%2Fkupit-kvartiru-novostroyki-kaliningradskaya-oblast-zelenogradskiy-01413799%2F',
    'frontend-serp.chatAnimationShownCount': '56',
    'frontend-serp.chatAnimationCounter': '57',
    '_ga_L109H0KCP9': 'GS2.1.s1776411488$o2$g0$t1776411488$j60$l0$h0',
    '_ym_isad': '2',
    '_yasc': 'Ej438V2ZT6fDKajUZ5DtXexROTXSGYJWid6eUA4zvGqJPzAGFCzgrieJw30mOc/gXAVe',
    '_yasc': 'tfnkrfDxxpXjze3rx6QnjnTjJI2v/Jo8463QW53yhQNO+LC5ec0nPBcNwybiLcB0gY7F',
    'sopr_session': '35c4869cbaf649f0',
    '_ym_visorc': 'b',
    'session_region_id': '1',
    'session_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'forever_region_id': '1',
    'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    '_ga_3369S417EL': 'GS2.1.s1776425421$o58$g1$t1776425976$j60$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; frontend-serp.offer_chat_onboarding_shown=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775; _CIAN_GK=8421b1d7-727f-42ac-9f77-a0ed1f26ad1b; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1776238374488; newbuilding-search-frontend.chatAnimationShownCount=122; countCallNowPopupShowed=2%3A1776238384809; sopr_utm=%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D; newbuilding_mortgage_payment_filter_onboarding=1; login_mro_popup=1; newbuilding-search-frontend.chatAnimationCounter=124; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnewobjects%2Flist%2F%3Fdeal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D4973; uxfb_card_satisfaction=%5B297124173%2C313319705%5D; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki-kaliningradskaya-oblast-zelenogradskiy-01413799%2F; frontend-serp.chatAnimationShownCount=56; frontend-serp.chatAnimationCounter=57; _ga_L109H0KCP9=GS2.1.s1776411488$o2$g0$t1776411488$j60$l0$h0; _ym_isad=2; _yasc=Ej438V2ZT6fDKajUZ5DtXexROTXSGYJWid6eUA4zvGqJPzAGFCzgrieJw30mOc/gXAVe; _yasc=tfnkrfDxxpXjze3rx6QnjnTjJI2v/Jo8463QW53yhQNO+LC5ec0nPBcNwybiLcB0gY7F; sopr_session=35c4869cbaf649f0; _ym_visorc=b; session_region_id=1; session_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; forever_region_id=1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; _ga_3369S417EL=GS2.1.s1776425421$o58$g1$t1776425976$j60$l0$h0',
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
        'foot_min': {
            'type': 'range',
            'value': {
                'lte': 1,
            },
        },
        'only_foot': {
            'type': 'term',
            'value': '2',
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
        'building_type2': {
            'type': 'terms',
            'value': [
                1,
                42,
                43,
                44,
                45,
                20,
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
    '_liquiditySource': 'web_commercial-serp',
}

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



current_date = datetime.date.today()

types_dict = {1: 'Офис, продажа', 2: 'Торговая площадь, продажа', 3: 'Склад, продажа', 5: 'Помещение свободного назначения, продажа',
              7: 'Производство, продажа', 11: 'Здание, продажа'}

not_done = [1, 2]
region_list = [1]

session = requests.Session()

for region in region_list:



    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["region"]["value"][0] = region


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




    flats = []
    counter = 1
    total_count = 1






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
                url = i['fullUrl'].rstrip('/').rpartition('/')[-3]
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
            try:
                phones = i['phones'][0]['number']
            except:
                phones = ''

            print(
                f" Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
            result = [location, location2, location3, okrug, raion, mikroraion, metro, street, house, adress, rooms_count, area, price, finish_type, description, property_from, url,
                      added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount, floorsCount, materialType,
                      parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest, highway_distance,
                      railways_nearest, railways_nearest_distance, railways_nearest_time, railways_nearest_travelType, jk,
                      underground_nearest, underground_nearest_time, hasFurniture,
                      kitchenArea, livingArea, loggiasCount, land_area, land_area_unit_type, possibleToChangeStatus, land_statusl, land_type,
                      buildingType2, buildingClassType, building_name, buildingType, layout, offerType, officeType, phones
                      ]
            flats.append(result)

        json_data["jsonQuery"]["page"]["value"] += 1
        print("-----------------------------------------------------------------------------")
        total_count = response.json()["data"]["offerCount"]
        downloaded = len(flats)
        print(f'Номер страницы: {json_data["jsonQuery"]["page"]["value"]}')
        print(f'Загружено {downloaded} предложений из {total_count}')
        counter += 1
        if downloaded > 500:
            break
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

        filename = f"Коммерция_продажа_{region}.xlsx"

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        df = pd.DataFrame(flats, columns=['Локация',
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
                                          'officeType',
                                          'Телефон'
                                          ])



        # Сохранение файла в папку
        df.to_excel(file_path, index=False)
        print(f'✅ Файл {filename} успешно сохранён')





