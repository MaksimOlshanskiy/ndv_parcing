# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам, например

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, merge_and_clean
import os
import glob


cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    '_gcl_au': '1.1.1976040648.1741613242',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'login_button_tooltip_key': '1',
    'cookie_agreement_accepted': '1',
    '_ga': 'GA1.1.1252090197.1741613246',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'uxfb_usertype': 'searcher',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'uxs_uid': '6864bb20-fdb3-11ef-a35a-c57d685f6f57',
    'afUserId': '01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p',
    'session_main_town_region_id': '1',
    'login_mro_popup': '1',
    'AF_SYNC': '1742810465392',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'map_preview_onboarding_counter': '3',
    'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1742892001597',
    'transport-accessibility_onboarding_counter': '3',
    'nbrdng_sn': '1',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743070248833%2C%22sl%22%3A%7B%22224%22%3A1742983848833%2C%221228%22%3A1742983848833%7D%7D',
    'DMIR_AUTH': '6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D',
    'F6_CIAN_SID': 'e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956',
    'cian_ruid': '8098251',
    'uxfb_card_satisfaction': '%5B310880450%2C310557584%2C314175573%2C304239998%2C313883579%5D',
    'countCallNowPopupShowed': '2%3A1742994427162',
    'frontend-offer-card.builder_chat_onboarding_shown': '1',
    '_yasc': 'e7bGoAyg8WaEp3nDwlIDFLVhQVf/SoWOCY8+9hj1BS+JTIqsy44ziZG6nN3QrHwlnoI=',
    '_yasc': 'VGksZPmps+Clu92DTfglhosHxZU9j4DEqe21+mgtpzN/QGlcthLtmiPri8U21vWCOsg=',
    'sopr_session': '38951139d7bd4bdb',
    'cookieUserID': '8098251',
    '_ym_isad': '2',
    'adrdel': '1743060223780',
    '_ym_visorc': 'b',
    'session_region_id': '1',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd3spRG0fZEhVEQsSF0ReXFVpdRUaS0olbngqZSUtMVYkfEspRFxRfCUfEX5vKFEJFFcvDT47Xi1vDycLElgJIQpJaQtec11SfiogfmBaFBlYVHkPaRpLZXQZGjYXIxl3dCtRDAxXLwkqPWx0MGFRUUtiDxwXMlxOe3NdZxBEQE1HQnR3LDtrHWZLXiFGVUlraWJRNF0tQUdHFHZ/OTBxf1dqNA==tOFAqQ==',
    'F6_CIAN_UID': '8098251',
    '_ga_3369S417EL': 'GS1.1.1743060223.18.1.1743060768.31.0.0',
    'cfidsw-cian': 'frKSft27ZPWJRnUJNMSNbx43eFqg3aWZdU5iIHk4H+kFYVEkvJiorpT0x5XNtYnzIwyJrGS1bpRS1YOshpc00KAMPF43dVYZhpsHRLiDiLx1p1HLekKViIxNKNXRhA7kuSFH9cDIXeLP9ykgh9DwwTLh01fNFp5U/B3f6F8=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; _gcl_au=1.1.1976040648.1741613242; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; login_button_tooltip_key=1; cookie_agreement_accepted=1; _ga=GA1.1.1252090197.1741613246; _ym_uid=174161324651361127; _ym_d=1741613246; uxfb_usertype=searcher; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; uxs_uid=6864bb20-fdb3-11ef-a35a-c57d685f6f57; afUserId=01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p; session_main_town_region_id=1; login_mro_popup=1; AF_SYNC=1742810465392; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; map_preview_onboarding_counter=3; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1742892001597; transport-accessibility_onboarding_counter=3; nbrdng_sn=1; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1743070248833%2C%22sl%22%3A%7B%22224%22%3A1742983848833%2C%221228%22%3A1742983848833%7D%7D; DMIR_AUTH=6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D; F6_CIAN_SID=e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956; cian_ruid=8098251; uxfb_card_satisfaction=%5B310880450%2C310557584%2C314175573%2C304239998%2C313883579%5D; countCallNowPopupShowed=2%3A1742994427162; frontend-offer-card.builder_chat_onboarding_shown=1; _yasc=e7bGoAyg8WaEp3nDwlIDFLVhQVf/SoWOCY8+9hj1BS+JTIqsy44ziZG6nN3QrHwlnoI=; _yasc=VGksZPmps+Clu92DTfglhosHxZU9j4DEqe21+mgtpzN/QGlcthLtmiPri8U21vWCOsg=; sopr_session=38951139d7bd4bdb; cookieUserID=8098251; _ym_isad=2; adrdel=1743060223780; _ym_visorc=b; session_region_id=1; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd3spRG0fZEhVEQsSF0ReXFVpdRUaS0olbngqZSUtMVYkfEspRFxRfCUfEX5vKFEJFFcvDT47Xi1vDycLElgJIQpJaQtec11SfiogfmBaFBlYVHkPaRpLZXQZGjYXIxl3dCtRDAxXLwkqPWx0MGFRUUtiDxwXMlxOe3NdZxBEQE1HQnR3LDtrHWZLXiFGVUlraWJRNF0tQUdHFHZ/OTBxf1dqNA==tOFAqQ==; F6_CIAN_UID=8098251; _ga_3369S417EL=GS1.1.1743060223.18.1.1743060768.31.0.0; cfidsw-cian=frKSft27ZPWJRnUJNMSNbx43eFqg3aWZdU5iIHk4H+kFYVEkvJiorpT0x5XNtYnzIwyJrGS1bpRS1YOshpc00KAMPF43dVYZhpsHRLiDiLx1p1HLekKViIxNKNXRhA7kuSFH9cDIXeLP9ykgh9DwwTLh01fNFp5U/B3f6F8=',
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
                    'type': 'polygon',
                    'name': 'Область поиска',
                    'coordinates': [
                        [
                            '37.1755519',
                            '55.8605102',
                        ],
                        [
                            '37.1702304',
                            '55.8604136',
                        ],
                        [
                            '37.1654239',
                            '55.8603171',
                        ],
                        [
                            '37.1609607',
                            '55.859641',
                        ],
                        [
                            '37.1568408',
                            '55.8589649',
                        ],
                        [
                            '37.153236',
                            '55.8574195',
                        ],
                        [
                            '37.1501461',
                            '55.8555844',
                        ],
                        [
                            '37.1465412',
                            '55.8541356',
                        ],
                        [
                            '37.142593',
                            '55.8530732',
                        ],
                        [
                            '37.1381298',
                            '55.851721',
                        ],
                        [
                            '37.1331516',
                            '55.8506586',
                        ],
                        [
                            '37.1292034',
                            '55.8497893',
                        ],
                        [
                            '37.1250835',
                            '55.8487269',
                        ],
                        [
                            '37.1209636',
                            '55.8474713',
                        ],
                        [
                            '37.118732',
                            '55.845443',
                        ],
                        [
                            '37.1170154',
                            '55.8420625',
                        ],
                        [
                            '37.1170154',
                            '55.8382957',
                        ],
                        [
                            '37.1173587',
                            '55.835205',
                        ],
                        [
                            '37.1177021',
                            '55.8327904',
                        ],
                        [
                            '37.118732',
                            '55.8302792',
                        ],
                        [
                            '37.120792',
                            '55.8279611',
                        ],
                        [
                            '37.1231952',
                            '55.8253533',
                        ],
                        [
                            '37.1262851',
                            '55.8229387',
                        ],
                        [
                            '37.1300617',
                            '55.8212002',
                        ],
                        [
                            '37.1348682',
                            '55.8200412',
                        ],
                        [
                            '37.1388164',
                            '55.8192685',
                        ],
                        [
                            '37.1431079',
                            '55.8189787',
                        ],
                        [
                            '37.1473995',
                            '55.8192685',
                        ],
                        [
                            '37.1520343',
                            '55.8195582',
                        ],
                        [
                            '37.1564975',
                            '55.8195582',
                        ],
                        [
                            '37.1606174',
                            '55.8205241',
                        ],
                        [
                            '37.1650806',
                            '55.8215865',
                        ],
                        [
                            '37.1704021',
                            '55.8226489',
                        ],
                        [
                            '37.1757236',
                            '55.8240977',
                        ],
                        [
                            '37.1803585',
                            '55.8255465',
                        ],
                        [
                            '37.1829334',
                            '55.8273816',
                        ],
                        [
                            '37.1867099',
                            '55.8293133',
                        ],
                        [
                            '37.1908298',
                            '55.8307621',
                        ],
                        [
                            '37.1946063',
                            '55.8321143',
                        ],
                        [
                            '37.1995845',
                            '55.833563',
                        ],
                        [
                            '37.2033611',
                            '55.8347221',
                        ],
                        [
                            '37.207481',
                            '55.836364',
                        ],
                        [
                            '37.2105709',
                            '55.8381025',
                        ],
                        [
                            '37.2134891',
                            '55.8404206',
                        ],
                        [
                            '37.2153774',
                            '55.8448635',
                        ],
                        [
                            '37.2177806',
                            '55.847761',
                        ],
                        [
                            '37.2182956',
                            '55.8502722',
                        ],
                        [
                            '37.2179523',
                            '55.8526869',
                        ],
                        [
                            '37.2162357',
                            '55.8548117',
                        ],
                        [
                            '37.2122875',
                            '55.8561639',
                        ],
                        [
                            '37.2057643',
                            '55.8575161',
                        ],
                        [
                            '37.1994129',
                            '55.8582888',
                        ],
                        [
                            '37.1946063',
                            '55.8590615',
                        ],
                        [
                            '37.1894565',
                            '55.8602205',
                        ],
                        [
                            '37.1853366',
                            '55.8609932',
                        ],
                        [
                            '37.1808734',
                            '55.8609932',
                        ],
                        [
                            '37.1762386',
                            '55.8610897',
                        ],
                        [
                            '37.1755519',
                            '55.8605102',
                        ],
                    ],
                },
            ],
        },
        'bbox': {
            'type': 'term',
            'value': [
                [
                    37.0303263984,
                    55.813274257,
                ],
                [
                    37.3049846016,
                    55.8667871026,
                ],
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 100,
            },
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
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
        'page': {
            'type': 'term',
            'value': 2,
        },
    },
}


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


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

# добавляем отделку в json_data
json_data['jsonQuery']['repair'] = {
    'type': 'terms',
    'value': [4],
}

if items_count <=  1500:

    rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
    total_floor_list = [[1, 100]]

elif items_count >= 2500:

    rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
    total_floor_list = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 11], [12, 14], [15, 20],
                        [21, 200]]

print(json_data)


for rooms in rooms_ids:

    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["room"]["value"] = rooms
    print(f'Комнатность: {rooms}')

    for repair_id in repair_ids:

        json_data["jsonQuery"]["page"]["value"] = 1
        json_data["jsonQuery"]["repair"]["value"][0] = repair_id

        for f in total_floor_list:

            flats = []
            json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
            json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
            json_data["jsonQuery"]["page"]["value"] = 1
            print(f'Этажи квартир: {f}')

            name_counter = f'{rooms}-{f[0]}-{f[1]}_{repair_id}'

            counter = 1
            total_count = 1

            while len(flats) < total_count:

                if counter > 1:
                    sleep_time = random.uniform(7, 11)
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
                    try:
                        geo1 = i['geo']['address'][0]['fullName']
                    except:
                        geo1 = ''
                    try:
                        geo2 = i['geo']['address'][1]['fullName']
                    except:
                        geo2 = ''
                    try:
                        geo3 = i['geo']['address'][2]['fullName']
                    except:
                        geo3 = ''
                    try:
                        geo4 = i['geo']['address'][3]['fullName']
                    except:
                        geo4 = ''

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
                    url = str(i['fullUrl'])

                    print(
                        f"Город {geo1}, {geo2}, {geo3}, {geo4}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}, объявление {property_from}")
                    result = [geo1, geo2, geo3, geo4, adress, jk, rooms_count, area, price, finish_type, description, property_from, url]
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
                sleep_time = random.uniform(7, 11)
                time.sleep(sleep_time)

                counter += 1

                # Базовый путь для сохранения
                base_path = r""

                folder_path = os.path.join(base_path, str(current_date))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                filename = f"{geo1}_{current_date}_{name_counter}.xlsx"

                # Полный путь к файлу
                file_path = os.path.join(folder_path, filename)

                df = pd.DataFrame(flats, columns=['Гео1',
                                                  'Гео2',
                                                  'Гео3',
                                                  'Гео4',
                                                  'Адрес',
                                                  'Название проекта',
                                                  'Кол-во комнат',
                                                  'Площадь',
                                                  'Цена',
                                                  'Отделка',
                                                  'Описание',
                                                  'Объявление от',
                                                  'Ссылка'
                                                  ])

                current_date = datetime.date.today()

                # Сохранение файла в папку
                df.to_excel(file_path, index=False)

    merge_and_clean(folder_path, f'Вторичка_{geo1}_{current_date}.xlsx')


