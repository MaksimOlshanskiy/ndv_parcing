'''

cian отдаёт не более 1500 объявлений
нужно проходиться по каждому списку: ids_moscow и т.д., подставляя его в 40 строке

'''


import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, save_cian_to_excel, save_flats_to_excel

proxies = {
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10260"
}


print(f'Первоначальный IP: {requests.get("https://ipinfo.io/json", proxies=proxies).json()}')

decoration_dict = {'preFine' : 'Предчистовая', 'fine' : 'С отделкой', 'without' : 'Без отделки', 'fineWithFurniture' : 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']



obshiy = [36935, 1444810, 5494, 50743, 2352, 48686, 2184313, 7778, 5138735,
          3419909, 3911074, 46840, 50027, 4051375, 4186702, 2234022, 1900321, 368, 81377, 45865,
       5227, 4771631, 4117447, 4708643, 3782658, 4157734, 45774, 2498484, 8825,
       4025502, 92320, 2511297, 4780951, 4296442, 4676364, 912499, 4033066,
       3206071, 3966751, 4720970, 4682511, 3913242, 4779110, 8787, 3930584, 90586,
       4260360, 5340468, 4648486, 46529, 48693, 4482950, 176051, 7789, 2567913, 4585408, 7030,
       300653, 5138871, 3730443, 7956, 4558643, 4729772, 1358767, 17877, 1628126, 8689, 5208,
        3394804, 600475, 5499, 4056931, 2522095, 2202, 4677457, 3922634, 4109874, 6644, 319,
          4126730, 3402470, 3872784, 5500590, 5698426, 5624837, 3975866, 4394151, 4090740,
          5593155, 5077128, 5747793, 5734461, 4202659, 7020, 5736965, 5708539, 5688213, 36571, 7480, 52703,
          5692858, 5739813, 5274, 8607, 5747459, 5713989, 3867553, 5556228, 12967, 5734549, 5553299]


parsim = [5706133]

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
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'cian_ruid': '8098251',
    'forever_region_id': '1',
    'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'countCallNowPopupShowed': '0%3A1787651078355',
    '_yasc': 'rOkWqiD61tIId0y+u2x4PZAMD++NZaKhmfnJuZBXkdrjYTGw59XnPJwiY0eh68E3YCKgdR50vw==',
    '_yasc': 'phw8pWZS1Y5dVsfqXzPFXm0AUh/JMQK9enkMKD3Zqcmfc0F7EjECfEvUW+1S45rfnvx5fs+xdg==',
    'login_mro_popup': '1',
    'sopr_session': 'e7dfb9b931c64166',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'mdd': '1',
    'session_region_id': '1',
    'session_main_town_region_id': '1',
    '_ga_3369S417EL': 'GS2.1.s1787676465$o78$g1$t1787676474$j51$l0$h0',
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
    # 'cookie': '_CIAN_GK=ebd70d3a-b0b3-483e-b09f-0f982f2a4eea; _gcl_au=1.1.96319925.1782933291; tmr_lvid=3a549fa46199720d5a0041676fe444a9; tmr_lvidTS=1782933291907; _ga=GA1.1.2045904184.1782933294; _ym_uid=1782933294531685029; _ym_d=1782933294; uxfb_usertype=searcher; WBRMVisitLast_utm=; WBRMVisitLast_referrer=https%3A%2F%2Fwww.google.com%2F; WBRMVisitFirst_utm=; WBRMVisitFirst_referrer=https%3A%2F%2Fwww.google.com%2F; uxs_uid=246eace0-7581-11f1-b1a1-3b03d0af4385; cookie_agreement_accepted=1; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; transport-accessibility_onboarding_counter=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; login_button_tooltip_key=1; frontend-offer-card.consultant_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationCounter=2; nbrdng_fv=1786546847550; rrpvid=938073304451891; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki-krasnodarskiy-kray-sochi-gorodskoy-okrug%2F; frontend-serp.chatAnimationCounter=75; frontend-serp.chatAnimationShownCount=75; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; cian_ruid=8098251; forever_region_id=1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; countCallNowPopupShowed=0%3A1787651078355; _yasc=rOkWqiD61tIId0y+u2x4PZAMD++NZaKhmfnJuZBXkdrjYTGw59XnPJwiY0eh68E3YCKgdR50vw==; _yasc=phw8pWZS1Y5dVsfqXzPFXm0AUh/JMQK9enkMKD3Zqcmfc0F7EjECfEvUW+1S45rfnvx5fs+xdg==; login_mro_popup=1; sopr_session=e7dfb9b931c64166; _ym_isad=2; _ym_visorc=b; mdd=1; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1787676465$o78$g1$t1787676474$j51$l0$h0; entry_src=bare_domain',
}

json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'newobject',
                    'id': 4825183,
                },
            ],
        },
        'decorations_list': {
            'type': 'terms',
            'value': [
                'preFine',
            ],
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
'_liquiditySource': 'web_serp',
}



def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

current_date = datetime.date.today()

no_flats = []

for y in parsim:

    session = requests.Session()

    flats = []

    json_data["jsonQuery"]["page"]["value"] = 1

    print("Новый ЖК", y)

    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y

    for decoration in decoration_list:

        counter = 1
        total_count = 1
        json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
        json_data["jsonQuery"]["page"]["value"] = 1
        print(decoration)
        print(json_data)




        while True:

            if counter > 1:
                sleep_time = random.uniform(2, 4)
                time.sleep(sleep_time)

            try:
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                    proxies = proxies,
                )

                print(response.status_code)
            except:
                print("Произошла ошибка, пробуем ещё раз")
                time.sleep(61)
                session = requests.Session()
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data,
                )
                print(response.status_code)
            items = response.json()["data"]["offersSerialized"]


            for i in items:
                try:
                    if i['building']['deadline']['isComplete'] == True:
                        srok_sdachi_old = "Дом сдан"
                    elif i['building']['deadline']['quarterEnd'] is None:
                        srok_sdachi_old = ''
                    else:
                        srok_sdachi_old = f"{i['building']['deadline']['quarterEnd']}"
                except:
                    srok_sdachi_old = ''
                try:
                    url = i['fullUrl']
                except:
                    url = ''

                try:
                    if i['isApartments'] == True:
                        type = "Апартаменты"
                    else:
                        type = "Квартира"
                except:
                    type = ''
                try:
                    if i['discount'] is not None:
                        price = extract_digits_or_original(i['discount']['newPrice'])
                        old_price = extract_digits_or_original(i['discount']['oldPrice'])
                    else:
                        old_price = i['bargainTerms']['priceRur']
                        price = ''
                except:
                    old_price = i['bargainTerms']['priceRur']
                    price = ''
                try:
                    project = i['geo']['jk']['displayName']
                except:
                    project = ''
                try:
                    finish_type = decoration_dict.get(decoration)
                except:
                    finish_type = ''
                try:
                    adress = i['geo']['userInput']
                except:
                    adress = ""

                try:
                    korpus = str(i["geo"]["jk"]["house"]["name"]).replace('Корпус ', '')
                except:
                    korpus = ''

                try:
                    developer = i['geo']['jk']['developer']['name']
                except:
                    developer = ""

                try:
                    if i["roomsCount"] == None:
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
                english = ''
                promzona = ''
                mestopolozhenie = ''
                subway = ''
                distance_to_subway = ''
                time_to_subway = ''
                mck = ''
                distance_to_mck = ''
                time_to_mck = ''
                bkl = ''
                distance_to_bkl = ''
                time_to_bkl = ''
                status = ''
                start = ''
                comment = ''

                okrug = ''
                district = ''

                eskrou = ''
                konstruktiv = ''
                klass = ''
                srok_sdachi = ''
                stadia = ''
                dogovor = ''

                discount = ''
                price_per_metr = ''
                price_per_metr_new = ''

                section = ''
                flat_number = ''


                print(
                    f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi_old}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                          mck, distance_to_mck, time_to_mck, distance_to_bkl,
                          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                          konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                          price_per_metr_new, price, section, floor, flat_number]
                flats.append(result)

            total_count = response.json()["data"]["offerCount"]
            downloaded = len(flats)
            print(f'ID ЖК: {y}. Отделка: {decoration}. Загружено {downloaded} предложений из {total_count}')
            print("-----------------------------------------------------------------------------")
            if not items:
                break
            json_data["jsonQuery"]["page"]["value"] += 1



            counter += 1

    if len(flats) > 0:
        save_flats_to_excel(flats, project, developer, kvartirografia=True)
    else:
        no_flats.append(y)

print(f'Пустые проекты: {no_flats}')


