# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам, например

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

ids = [4457540
       ]  # id ЖК для парсинга

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
    '_ga_3369S417EL': 'GS2.1.s1787295947$o71$g1$t1787296297$j49$l0$h0',
    'entry_src': 'bare_domain',
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
    # 'cookie': '_CIAN_GK=ebd70d3a-b0b3-483e-b09f-0f982f2a4eea; _gcl_au=1.1.96319925.1782933291; tmr_lvid=3a549fa46199720d5a0041676fe444a9; tmr_lvidTS=1782933291907; _ga=GA1.1.2045904184.1782933294; _ym_uid=1782933294531685029; _ym_d=1782933294; uxfb_usertype=searcher; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; uxs_uid=246eace0-7581-11f1-b1a1-3b03d0af4385; cookie_agreement_accepted=1; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; transport-accessibility_onboarding_counter=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; login_button_tooltip_key=1; frontend-offer-card.consultant_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationCounter=2; nbrdng_fv=1786546847550; rrpvid=938073304451891; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki-krasnodarskiy-kray-sochi-gorodskoy-okrug%2F; frontend-serp.chatAnimationCounter=75; frontend-serp.chatAnimationShownCount=75; countCallNowPopupShowed=1%3A1786997542942; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; _yasc=Wiajr9ZLYqzNfsnMxWbY4f3nH/4tPD5PdvqYV6A2x+Stw9i1YJJaC49KofvwUIxs35ndBPnjIg==; _yasc=vGLYQRwRTIBQpoL2XWmYuwTJsFTh8ufz9e6KiBxmM6YcQOIAAInObgoxtTA2O9b2Euy46x1y5Q==; login_mro_popup=1; sopr_session=b80f654a16d740c2; _ym_isad=2; _ym_visorc=b; mdd=1; forever_region_id=-1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1787295947$o71$g1$t1787296297$j49$l0$h0; entry_src=bare_domain',
}

proxies = {
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270"
}

json_data = {
    'jsonQuery': {
        '_type': 'suburbanrent',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                4607,
            ],
        },
        'currency': {
            'type': 'term',
            'value': 2,
        },
        'for_day': {
            'type': 'term',
            'value': '!1',
        },
        'object_type': {
            'type': 'terms',
            'value': [
                1,
                4,
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
    '_liquiditySource': 'web_serp',
}


name_counter = "РязО"


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
        sleep_time = random.uniform(2, 4)
        time.sleep(sleep_time)
    try:
        response = session.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            cookies=cookies,
            headers=headers,
            json=json_data,
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
            highway = i['geo']['highways'][0]['name']
        except:
            highway = ''
        try:
            house_area = float(i['totalArea'].replace(',', '.'))
        except:
            house_area = ''
        try:
            uchastok_area = float(i['land']['area'])
        except:
            uchastok_area = ''
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



        print(
            f"Шоссе {highway}, {url}, Участок: {uchastok_area}, дом: {house_area}, цена: {price}, посёлок {poselok}, кп: {kp}, объявление {property_from}")
        result = ['Рязанская область', highway, uchastok_area, house_area, price, poselok, kp, property_from, url]
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

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"МО-{name_counter}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Регион',
                                  'Шоссе',
                                  'Размер участка',
                                  'Размер дома',
                                  'Цена',
                                  'Посёлок',
                                  'Коттеджный посёлок',
                                  'Объявление от',
                                  'Ссылка'
                                  ])

current_date = datetime.date.today()


# Сохранение файла в папку
df.to_excel(file_path, index=False)
