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
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270"
}


print(f'Первоначальный IP: {requests.get("https://ipinfo.io/json", proxies=proxies).json()}')

decoration_dict = {'preFine' : 'Предчистовая', 'fine' : 'С отделкой', 'without' : 'Без отделки', 'fineWithFurniture' : 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']

Пустые проекты: [5494, 2344978, 3683691, 92320, 2511297, 4457540, 3966751, 90586, 4482950, 176051, 7956, 4558643, 1358767, 4056931, 2202, 3922634, 4109874, 3872784, 5692858, 8607]


obshiy = [36935, 1444810, 6381, 5494, 50743, 2352, 48686, 2184313, 7778, 5138735,
          3419909, 3911074, 46840, 50027, 4051375, 4186702, 2234022, 1900321, 368, 81377, 45865,
       5227, 4771631, 4117447, 4708643, 3782658, 4157734, 45774, 2498484, 8825,
       4025502, 92320, 2511297, 4850351, 3932079, 4780951, 4296442, 4676364, 912499, 4033066,
       3206071, 3966751, 4720970, 4682511, 3913242, 4779110, 8787, 3930584, 90586,
       4260360, 5340468, 4648486, 46529, 48693, 4482950, 176051, 7789, 2567913, 4585408, 7030,
       300653, 5138871, 3730443, 7956, 4558643, 4729772, 1358767, 17877, 1628126, 8689, 5208,
        3394804, 600475, 5499, 4056931, 2522095, 2202, 4677457, 3922634, 4109874, 6644, 319,
          4126730, 3402470, 3872784, 5500590, 5698426, 5624837, 3975866, 4394151, 4090740,
          5593155, 5077128, 5747793, 5734461, 4202659, 7020, 5736965, 5708539, 4670407, 5688213, 36571, 7480, 52703,
          5692858, 5739813, 5741740, 5274, 8607, 5747459, 5713989, 3867553, 5556228, 12967, 5734549, 5703570]


parsim = obshiy

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
    'forever_region_id': '4959',
    'forever_region_name': '%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_main_town_region_id': '4959',
    'session_region_id': '4593',
    'session_main_town_region_id': '1',
    'login_mro_popup': '1',
    '_ym_isad': '2',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'sopr_session': '984fe57857c04e92',
    '_ym_visorc': 'b',
    '_yasc': 'TRKPtQwX100Llb+e03dywP4BMM51qmiqnpIri2vjwENZelIZncfgiKhy9oA6lHkCD45B0dE=',
    '_yasc': '0SMjQFnVkpPLd+wWAfEiWFOgNTsWxvn3eJZjAgkulSdK+kvhtbHsGVU0Gbe2z9s/OyK/5r8=',
    '_ga_3369S417EL': 'GS2.1.s1775561722$o34$g1$t1775562653$j60$l0$h0',
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
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; _ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; transport-accessibility_onboarding_counter=3; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:205657295806|ad:1889238602131455357|grp:5657295806|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=|205657295806&utm_campaign=b2c_nov_mskmo_perf_mix_search_dsa_feed_general_drr_arwm_703812141&etext=2202.h07M9Tlhg3N9CwbhNMoyrVsLWbdrg5CRpbuLNhiEcIVoTY8yPfNz7DVvSxFMf63mtQfzGVZPsUeL_PUMqGvCe3BsenN6dGFxZmZlYWRmaWY.c0ab089525eaca3735ee4aa1b318395f0703704e&yclid=3873403374751711231; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatAnimationShownCount=107; frontend-serp.offer_chat_onboarding_shown=1; frontend-serp.chatAnimationShownCount=7; newbuilding-search-frontend.chatAnimationCounter=111; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki%2F; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; frontend-serp.chatAnimationCounter=10; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki%2F; countCallNowPopupShowed=1%3A1775476258941; forever_region_id=4959; forever_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_main_town_region_id=4959; session_region_id=4593; session_main_town_region_id=1; login_mro_popup=1; _ym_isad=2; newbuilding_mortgage_payment_filter_onboarding=1; sopr_session=984fe57857c04e92; _ym_visorc=b; _yasc=TRKPtQwX100Llb+e03dywP4BMM51qmiqnpIri2vjwENZelIZncfgiKhy9oA6lHkCD45B0dE=; _yasc=0SMjQFnVkpPLd+wWAfEiWFOgNTsWxvn3eJZjAgkulSdK+kvhtbHsGVU0Gbe2z9s/OyK/5r8=; _ga_3369S417EL=GS2.1.s1775561722$o34$g1$t1775562653$j60$l0$h0',
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


