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

proxies = {
    'https': '47.95.203.57:8080'
}

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
        '_type': 'suburbansale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                4623,
            ],
        },
        'price': {
            'type': 'range',
            'value': {
                'gte': 0,
                'lte': 4000000,
            },
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
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
}



response = requests.post(
    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
    cookies=cookies,
    headers=headers,
    json=json_data,
)


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
        sleep_time = random.uniform(7, 11)
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
            if float(i['land']['area']) > 200 or i['land']['areaUnitType'] == 'hectare':
                continue#   можно менять данный фильтр, какой максимальный размер участка добавляем
        except:
            continue
        try:
            highway = i['geo']['highways'][0]['name']
        except:
            highway = ''
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
            f"Шоссе {highway}, {url}, Участок: {uchastok_area}, цена: {price}, посёлок {poselok}, объявление {property_from}")
        result = [highway, uchastok_area, price, poselok, property_from, url]
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

filename = f"ИЖС-1_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Шоссе',
                                  'Размер участка',
                                  'Цена',
                                  'Посёлок',
                                  'Объявление от',
                                  'Ссылка'
                                  ])

current_date = datetime.date.today()


# Сохранение файла в папку
df.to_excel(file_path, index=False)
