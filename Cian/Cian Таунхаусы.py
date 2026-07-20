# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам, например

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

multi_ids = []

proxies = {
    'https': '47.95.203.57:8080'
}

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
    'transport-accessibility_onboarding_counter': '3',
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
    'frontend-serp.chatAnimationShownCount': '20',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775',
    '_CIAN_GK': '8421b1d7-727f-42ac-9f77-a0ed1f26ad1b',
    'login_mro_popup': '1',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'frontend-serp.chatAnimationCounter': '23',
    'frontend-serp.chatAnimationPrevPath': '%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D4951%26totime%3D2592000',
    'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1776238374488',
    'tmr_detect': '0%7C1776238405763',
    'uxfb_card_satisfaction': '%5B325820477%2C325739631%5D',
    '_ym_isad': '2',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnovostroyki-kareliya%2F',
    'newbuilding-search-frontend.chatAnimationCounter': '122',
    'newbuilding-search-frontend.chatAnimationShownCount': '122',
    'countCallNowPopupShowed': '2%3A1776238384809',
    'sopr_utm': '%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D',
    'session_region_name': '%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_region_name': '%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_main_town_region_id': '5075',
    'forever_region_id': '5075',
    '_yasc': 'HIeW7GIe0Spkh//zvX/eKAiLCnH3KEIstQ4WG2h4DoxyJ3ZBRJpBKA/3X9wS/Hs5MXrp',
    '_yasc': 'voyH4TGZ29yf68P6Gxmkg+RJ8QyLw2WEkplncw7Zx4kYb1pVvpHWyyfOIDgeG5Pl6R3v',
    'sopr_session': '649df47953b3454e',
    '_ym_visorc': 'b',
    'session_region_id': '4593',
    'session_main_town_region_id': '1',
    '_ga_3369S417EL': 'GS2.1.s1776254404$o51$g1$t1776258771$j42$l0$h0',
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
    # 'cookie': '_ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; transport-accessibility_onboarding_counter=3; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; frontend-serp.offer_chat_onboarding_shown=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; frontend-serp.chatAnimationShownCount=20; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775; _CIAN_GK=8421b1d7-727f-42ac-9f77-a0ed1f26ad1b; login_mro_popup=1; newbuilding_mortgage_payment_filter_onboarding=1; frontend-serp.chatAnimationCounter=23; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26decorations_list%255B0%255D%3Dfine%26decorations_list%255B1%255D%3DfineWithFurniture%26decorations_list%255B2%255D%3DpreFine%26decorations_list%255B3%255D%3Dwithout%26engine_version%3D2%26from_developer%3D1%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D4951%26totime%3D2592000; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1776238374488; tmr_detect=0%7C1776238405763; uxfb_card_satisfaction=%5B325820477%2C325739631%5D; _ym_isad=2; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki-kareliya%2F; newbuilding-search-frontend.chatAnimationCounter=122; newbuilding-search-frontend.chatAnimationShownCount=122; countCallNowPopupShowed=2%3A1776238384809; sopr_utm=%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D; session_region_name=%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_region_name=%D0%AF%D1%80%D0%BE%D1%81%D0%BB%D0%B0%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_main_town_region_id=5075; forever_region_id=5075; _yasc=HIeW7GIe0Spkh//zvX/eKAiLCnH3KEIstQ4WG2h4DoxyJ3ZBRJpBKA/3X9wS/Hs5MXrp; _yasc=voyH4TGZ29yf68P6Gxmkg+RJ8QyLw2WEkplncw7Zx4kYb1pVvpHWyyfOIDgeG5Pl6R3v; sopr_session=649df47953b3454e; _ym_visorc=b; session_region_id=4593; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1776254404$o51$g1$t1776258771$j42$l0$h0',
}

json_data = {
    'jsonQuery': {
        '_type': 'suburbansale',
        'from_mcad_km': {
            'type': 'range',
            'value': {
                 'lte': 50,
            },
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'highway',
                    'id': 4,
                },
                {
                    'type': 'highway',
                    'id': 10,
                },
                {
                    'type': 'highway',
                    'id': 29,
                },
                {
                    'type': 'highway',
                    'id': 129,
                },
            ],
        },
        'house_year': {
            'type': 'range',
            'value': {
                'gte': 2010,
                'lte': 2026,
            },
        },
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                4593,
            ],
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
        },
        'electronic_trading': {
            'type': 'term',
            'value': 2,
        },
        'land_status': {
            'type': 'terms',
            'value': [
                1,
                2,
            ],
        },
        'object_type': {
            'type': 'terms',
            'value': [
                1,
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
    },
    '_liquiditySource': 'web_serp',
}


name_counter = 80

response = requests.post(
    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

items_count = response.json()['data']["aggregatedCount"]
print(f'Found {items_count} items')


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


current_date = datetime.date.today()

session = requests.Session()

flats = []
counter = 1
total_count = 1
json_data["jsonQuery"]["page"]["value"] = 1

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
            if i['similar'] and i['similar']['count'] != 0 :
                multi_id = i['similar']['url'].split('=')[-1]
                print(multi_id)
                multi_ids.append(multi_id)
                continue
        except:
            continue

        try:
            region = i['geo']['address'][0]['fullName']
        except:
            region = ''
        try:
            house_area = float(i['totalArea'].replace(',', '.'))
        except:
            house_area = ''
        try:
            uchastok_area = float(i['land']['area'])
        except:
            uchastok_area = i['land']['area']
        try:
            price = int(i['bargainTerms']['priceRur'])
        except:
            price = i['bargainTerms']['priceRur']
        try:
            poselok = i['geo']['address'][2]['fullName']
        except:
            poselok = ''
        try:
            kp = i['kp']['name']
        except:
            kp = ''
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
        url = i['fullUrl']
        flours = i['building']['floorsCount']

        print(
            f"Шоссе {region}, {url}, Участок: {uchastok_area}, дом: {house_area}, цена: {price}, посёлок {poselok}, кп: {kp}, объявление {property_from}")
        result = [region, uchastok_area, house_area, price, poselok, kp, property_from, flours, url]
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

for mult_id in multi_ids:

    json_data = {
        'jsonQuery': {
            '_type': 'suburbansale',
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'multi_id': {
                'type': 'term',
                'value': mult_id,
            },
            'page': {
                'type': 'term',
                'value': 1,
            },
            'region': {
                'type': 'terms',
                'value': [
                    1,
                ],
            },
        },
        '_liquiditySource': 'web_serp',
    }

    json_data["jsonQuery"]["page"]["value"] = 1
    print(f'id = {mult_id}')
    print(json_data)
    while True:

        if counter > 1:
            sleep_time = random.uniform(6, 9)
            time.sleep(sleep_time)

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
                region = i['geo']['address'][0]['fullName']
            except:
                region = ''
            try:
                house_area = float(i['totalArea'].replace(',', '.'))
            except:
                house_area = ''
            try:
                uchastok_area = float(i['land']['area'])
            except:
                uchastok_area = i['land']['area']
            try:
                price = int(i['bargainTerms']['priceRur'])
            except:
                price = i['bargainTerms']['priceRur']
            try:
                poselok = i['geo']['address'][2]['fullName']
            except:
                poselok = ''
            try:
                kp = i['kp']['name']
            except:
                kp = ''
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
            url = i['fullUrl']
            flours = i['building']['floorsCount']

            print(
                f"{region}, {url}, Участок: {uchastok_area}, дом: {house_area}, цена: {price}, посёлок {poselok}, кп: {kp}, объявление {property_from}")
            result = [region, uchastok_area, house_area, price, poselok, kp, property_from, flours, url]
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

counter += 1

print(multi_ids)
# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"МО-{name_counter}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Регион',
                                  'Размер участка',
                                  'Размер дома',
                                  'Цена',
                                  'Посёлок',
                                  'Коттеджный посёлок',
                                  'Объявление от',
                                  'Этажность',
                                  'Ссылка'
                                  ])

current_date = datetime.date.today()

# Сохранение файла в папку
df.to_excel(file_path, index=False)
