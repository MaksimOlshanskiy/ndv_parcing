import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import haversine, merge_and_clean

'''
region_list = [
    1, 2, 4593, 4588, 4584, 4606, 4608, 4618, 4560, 4609, 4619, 181462,
    4564, 4581, 4620, 4607, 4557, 4623, 4612, 4573, 4598, 4585, 4555,
    4567, 4621, 4587, 4605, 4568, 4625, 184723, 4604, 4576, 4574, 4603,
    4602, 4562, 4561, 4565, 4601, 4636, 4599, 4629, 4580, 4630, 4572,
    4615, 4614, 4591, 4553, 4635, 4624, 4570, 4583, 4566, 4600, 4554,
    4556, 4558, 4563, 4569, 5053, 4571, 4575, 4577, 4578, 4579, 4582,
    4586, 4589, 4590, 4592, 4594, 4595, 4597, 4610, 4611, 4613, 4617,
    4622, 4627, 4628, 4631, 4633, 4634
]
'''
type_of_lot = 'Вторичка, аренда'

cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrdel': '1744094487237',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
    'newbuilding-search-frontend.consultant_cian_chat_onboarding_shown': '1',
    'cookie_agreement_accepted': '1',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    '_ga': 'GA1.1.460280003.1749468781',
    'uxfb_usertype': 'searcher',
    'uxs_uid': '1ed08180-4604-11f0-94f5-19dbce91137e',
    'seen_cpd_landing': '1',
    'cian_ruid': '8098251',
    'map_preview_onboarding_counter': '3',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    'rrpvid': '771260525504896',
    'rcuid': '67e27578d41e2c9a8a114add',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    'transport-accessibility_onboarding_counter': '3',
    'ma_id': '6225667261741613246584',
    '__upin': 'jzXjhLRLkqO1JTeopJQqkQ',
    '_ym_d': '1757401308',
    '__ai_fp_uuid': '245d903c22bdc927%3A15',
    'cfidsw-cian': 'SgybcGIxNohISLx1pm7TZqH4g2s0yZuun/43PQdS2lgKaW1Kt2AcGCTAyJaFGaa6yif3R/HldhAgXm3NC0K1u2QP7/sFfrGAdA4ZVPMfOJa4b0/tEUtDjqgwm9GSX+69a5J2oQxu0kb6xLq5qabHFKDbtz7bLcmntk7vk6q2',
    'fgsscw-cian': 'dkUfb3f6bf8a85c6dfe120486165772c64b880e0',
    'gsscw-cian': 'GdzeiSCNUpAGrW7VRqkf5HSFFt9sNQakyL+AtSmc+VocwkwctD0owGAy6Ep70WOKkOAy04eijt+ES0daHnOK3gwUOuidmlC2G9TB0+wNvtP8V7sHMYFtMTpkKfyD6YRffqoxkmNFnaFzVK89TYWEvJqUdrnwGhnmR1lz4ESuajkKMlmHorWlZYK6F5eL8vkb18AUsoA0gb3TqJZcjGTNUM0NDgVC77X1RVs+OTJ0BoIZS5emlG03oHMUOE5DmailvO+/rtfQBtyE',
    'ma_id_api': 'GxRtmeoGuaB8279kyKiOOWoPH3AsJBUy4myCSKYvMpjBeANYebQlWRDzcAcb90W0aJ3L82J0ln2wRtm+ZcV/EtxWXxRMU3PbIiQ+wf0Q2kPuA5vJ5WrM0laQZQoxa7r8hTzTdJ1xpw4hKDANo4wrMeQ5E+pmcaaQlBTcWkjgFjcCgrcb5/1hOsy4Nv8P/yxdpkf2ErnEUxaWyUGayjdao676tqTl//KiB2aQXIbJV6N/+hg6BweZ4ef6fwjquBXebADBMM3MAawoME8u0fnP/3qkkD3/m4jccb4sC735sgX3+kYmdxq/nQjGk3O11dbRxbZaLgMPt6C6d8xY+FzAhg==',
    '_gcl_au': '1.1.1810869406.1761569722',
    'frontend-offer-card.consultant_chat_onboarding_shown': '1',
    'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnovostroyki-ot-zastroyschikov%2F',
    'countCallNowPopupShowed': '2%3A1763716639971',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:52037811265|ad:16202025265|grp:5454187042|drf:no|dev:desktop|p:premium|n:1|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&ybaip=1&yclid=10829203034459865087',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    '_ym_isad': '2',
    'newbuilding-search-frontend.chatAnimationCounter': '3',
    'newbuilding_mortgage_payment_filter_onboarding': '1',
    'session_region_name': '%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4',
    'forever_region_id': '4704',
    'forever_region_name': '%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4',
    'uxfb_card_satisfaction': '%5B309384022%2C324043854%2C323869097%2C323963675%5D',
    'frontend-serp.chatAnimationPrevPath': '%2Fcat.php%3Fdeal_type%3Dsale%26engine_version%3D2%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D184723%26with_newobject%3D1',
    'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1764075804222',
    'tmr_detect': '0%7C1764075908711',
    '_yasc': '2pJhiBC9TKWK+iEBt0k7uqLzYAamY8koI2dwBC1R57nRBWm98Pc4WfFXcGpEyCYGbQ==',
    '_yasc': 'ehxxEZLh8A5uNNZIvEAgT48WIgAamRbce24lu+osB4O/l8bs7EXwxOmp6kY4whrppw==',
    'session_region_id': '184723',
    'session_main_town_region_id': '184723',
    'login_mro_popup': '1',
    'sopr_session': '7fde76427fd54c5e',
    '_ym_visorc': 'b',
    'cookieUserID': '8098251',
    '_ga_3369S417EL': 'GS2.1.s1764083298$o390$g1$t1764083308$j50$l0$h0',
    'frontend-serp.chatAnimationCounter': '4',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://sevastopol.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://sevastopol.cian.ru/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; _ga=GA1.1.460280003.1749468781; uxfb_usertype=searcher; uxs_uid=1ed08180-4604-11f0-94f5-19dbce91137e; seen_cpd_landing=1; cian_ruid=8098251; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; rrpvid=771260525504896; rcuid=67e27578d41e2c9a8a114add; frontend-offer-card.builder_chat_onboarding_shown=1; transport-accessibility_onboarding_counter=3; ma_id=6225667261741613246584; __upin=jzXjhLRLkqO1JTeopJQqkQ; _ym_d=1757401308; __ai_fp_uuid=245d903c22bdc927%3A15; cfidsw-cian=SgybcGIxNohISLx1pm7TZqH4g2s0yZuun/43PQdS2lgKaW1Kt2AcGCTAyJaFGaa6yif3R/HldhAgXm3NC0K1u2QP7/sFfrGAdA4ZVPMfOJa4b0/tEUtDjqgwm9GSX+69a5J2oQxu0kb6xLq5qabHFKDbtz7bLcmntk7vk6q2; fgsscw-cian=dkUfb3f6bf8a85c6dfe120486165772c64b880e0; gsscw-cian=GdzeiSCNUpAGrW7VRqkf5HSFFt9sNQakyL+AtSmc+VocwkwctD0owGAy6Ep70WOKkOAy04eijt+ES0daHnOK3gwUOuidmlC2G9TB0+wNvtP8V7sHMYFtMTpkKfyD6YRffqoxkmNFnaFzVK89TYWEvJqUdrnwGhnmR1lz4ESuajkKMlmHorWlZYK6F5eL8vkb18AUsoA0gb3TqJZcjGTNUM0NDgVC77X1RVs+OTJ0BoIZS5emlG03oHMUOE5DmailvO+/rtfQBtyE; ma_id_api=GxRtmeoGuaB8279kyKiOOWoPH3AsJBUy4myCSKYvMpjBeANYebQlWRDzcAcb90W0aJ3L82J0ln2wRtm+ZcV/EtxWXxRMU3PbIiQ+wf0Q2kPuA5vJ5WrM0laQZQoxa7r8hTzTdJ1xpw4hKDANo4wrMeQ5E+pmcaaQlBTcWkjgFjcCgrcb5/1hOsy4Nv8P/yxdpkf2ErnEUxaWyUGayjdao676tqTl//KiB2aQXIbJV6N/+hg6BweZ4ef6fwjquBXebADBMM3MAawoME8u0fnP/3qkkD3/m4jccb4sC735sgX3+kYmdxq/nQjGk3O11dbRxbZaLgMPt6C6d8xY+FzAhg==; _gcl_au=1.1.1810869406.1761569722; frontend-offer-card.consultant_chat_onboarding_shown=1; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnovostroyki-ot-zastroyschikov%2F; countCallNowPopupShowed=2%3A1763716639971; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:52037811265|ad:16202025265|grp:5454187042|drf:no|dev:desktop|p:premium|n:1|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&ybaip=1&yclid=10829203034459865087; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; _ym_isad=2; newbuilding-search-frontend.chatAnimationCounter=3; newbuilding_mortgage_payment_filter_onboarding=1; session_region_name=%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4; forever_region_id=4704; forever_region_name=%D0%92%D0%BE%D0%BB%D0%B3%D0%BE%D0%B3%D1%80%D0%B0%D0%B4; uxfb_card_satisfaction=%5B309384022%2C324043854%2C323869097%2C323963675%5D; frontend-serp.chatAnimationPrevPath=%2Fcat.php%3Fdeal_type%3Dsale%26engine_version%3D2%26object_type%255B0%255D%3D2%26offer_type%3Dflat%26region%3D184723%26with_newobject%3D1; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1764075804222; tmr_detect=0%7C1764075908711; _yasc=2pJhiBC9TKWK+iEBt0k7uqLzYAamY8koI2dwBC1R57nRBWm98Pc4WfFXcGpEyCYGbQ==; _yasc=ehxxEZLh8A5uNNZIvEAgT48WIgAamRbce24lu+osB4O/l8bs7EXwxOmp6kY4whrppw==; session_region_id=184723; session_main_town_region_id=184723; login_mro_popup=1; sopr_session=7fde76427fd54c5e; _ym_visorc=b; cookieUserID=8098251; _ga_3369S417EL=GS2.1.s1764083298$o390$g1$t1764083308$j50$l0$h0; frontend-serp.chatAnimationCounter=4',
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
                2, 3, 4
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
                1, 2, 3, 4, 5, 6, 7, 9
            ],
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
                        json=json_data
                    )

items_count = response.json()['data']["aggregatedCount"]
print(f'В городе {items_count} лотов')


if items_count <=  1500:

    rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    total_floor_list = [[1, 100]]

elif 2500 <= items_count <= 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    total_floor_list = [[1, 6], [7, 12], [13, 200]]

elif items_count > 4500:

    rooms_ids = [[1], [9]]
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
                    print(response.status_code)
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
                    keys = ["location", "location2", "location3", "okrug", "raion", "mikroraion", "metro", "street",
                            "house"]

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
                        finish_type = repair_ids_dict.get(repair_id)
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

                    print(
                        f"Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
                    result = [type_of_lot, location, location2, location3, okrug, raion, mikroraion, metro, street,
                              house, adress, rooms_count, area, price, finish_type, description, property_from, url,
                              added, balconiesCount, bedroomsCount, buildYear, cargoLiftsCount, passengerLiftsCount,
                              floorsCount, materialType,
                              parking, creationDate, floorNumber, coordinates_lat, coordinates_lng, highways_nearest,
                              highway_distance,
                              railways_nearest, railways_nearest_distance, railways_nearest_time,
                              railways_nearest_travelType, jk,
                              underground_nearest, underground_nearest_time, hasFurniture,
                              kitchenArea, livingArea, loggiasCount
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
                sleep_time = random.uniform(2, 4)
                time.sleep(sleep_time)



            # Базовый путь для сохранения
            base_path = r""

            folder_path = os.path.join(base_path, str(current_date))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

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
                                              'Число лоджий'
                                              ])

            current_date = datetime.date.today()

            # Базовый путь для сохранения
            base_path = r""

            folder_path = os.path.join(base_path, str(current_date))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            filename = f"Аренда_{location}_{json_data['jsonQuery']['room']['value']}_{json_data['jsonQuery']['floor']['value']['lte']}_{json_data['jsonQuery']['repair']['value']}_{current_date}.xlsx"

            # Полный путь к файлу
            file_path = os.path.join(folder_path, filename)

            # Сохранение файла в папку
            df.to_excel(file_path, index=False)

merge_and_clean(folder_path, f'Аренда_{location}_{current_date}.xlsx')