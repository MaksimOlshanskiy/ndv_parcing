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
    'DMIR_AUTH': 'mgy0rTyxBQExFI3hRrY9WIt9MvSCNFqa%2Bzm4IVGqXQ9E8uImyZAXcovTzLMZHu7sJH4NX6mSM79OHryqc6JMCg6IZN%2BCR6kVHv2iHQDRCix7gDY4nA5zopU3Z1k%2Bk7QMya2T%2FiJkoY45KVHVZ69nC6%2FBBBzXENqOvTIyvNZ%2BCo8%3D',
    'forever_region_id': '4606',
    'forever_region_name': '%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    'forever_main_town_region_id': '4959',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:53632938357|ad:16644615549|grp:5511051039|drf:no|dev:desktop|p:premium|n:2|reg:10758|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&ybaip=1&yclid=6818025664178814975',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'countCallNowPopupShowed': '2%3A1763362751209',
    '_ym_isad': '2',
    '_yasc': 'dgiUeSTPP193oguKbYFBFb1Idz2vYwWtXrx0xl3VIrYLH03hVlarYLoHlZjan+VQjw==',
    '_yasc': 'zbfOUZCD2VRuDcJ56B/We1y6IbfxvVfDkP0EexZ2QVFbrEe1ZYDaRqx1eUI7xoiNsQ==',
    'sopr_session': '1e3dcee3e8a042cc',
    'cookieUserID': '8098251',
    '_ym_visorc': 'b',
    'uxfb_card_satisfaction': '%5B323633012%2C319363085%2C322859138%2C319931163%5D',
    'session_region_id': '1',
    'session_main_town_region_id': '1',
    '_ga_3369S417EL': 'GS2.1.s1763474406$o363$g1$t1763475916$j58$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; _ga=GA1.1.460280003.1749468781; uxfb_usertype=searcher; uxs_uid=1ed08180-4604-11f0-94f5-19dbce91137e; seen_cpd_landing=1; cian_ruid=8098251; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; rrpvid=771260525504896; rcuid=67e27578d41e2c9a8a114add; frontend-offer-card.builder_chat_onboarding_shown=1; transport-accessibility_onboarding_counter=3; ma_id=6225667261741613246584; __upin=jzXjhLRLkqO1JTeopJQqkQ; _ym_d=1757401308; __ai_fp_uuid=245d903c22bdc927%3A15; cfidsw-cian=SgybcGIxNohISLx1pm7TZqH4g2s0yZuun/43PQdS2lgKaW1Kt2AcGCTAyJaFGaa6yif3R/HldhAgXm3NC0K1u2QP7/sFfrGAdA4ZVPMfOJa4b0/tEUtDjqgwm9GSX+69a5J2oQxu0kb6xLq5qabHFKDbtz7bLcmntk7vk6q2; fgsscw-cian=dkUfb3f6bf8a85c6dfe120486165772c64b880e0; gsscw-cian=GdzeiSCNUpAGrW7VRqkf5HSFFt9sNQakyL+AtSmc+VocwkwctD0owGAy6Ep70WOKkOAy04eijt+ES0daHnOK3gwUOuidmlC2G9TB0+wNvtP8V7sHMYFtMTpkKfyD6YRffqoxkmNFnaFzVK89TYWEvJqUdrnwGhnmR1lz4ESuajkKMlmHorWlZYK6F5eL8vkb18AUsoA0gb3TqJZcjGTNUM0NDgVC77X1RVs+OTJ0BoIZS5emlG03oHMUOE5DmailvO+/rtfQBtyE; ma_id_api=GxRtmeoGuaB8279kyKiOOWoPH3AsJBUy4myCSKYvMpjBeANYebQlWRDzcAcb90W0aJ3L82J0ln2wRtm+ZcV/EtxWXxRMU3PbIiQ+wf0Q2kPuA5vJ5WrM0laQZQoxa7r8hTzTdJ1xpw4hKDANo4wrMeQ5E+pmcaaQlBTcWkjgFjcCgrcb5/1hOsy4Nv8P/yxdpkf2ErnEUxaWyUGayjdao676tqTl//KiB2aQXIbJV6N/+hg6BweZ4ef6fwjquBXebADBMM3MAawoME8u0fnP/3qkkD3/m4jccb4sC735sgX3+kYmdxq/nQjGk3O11dbRxbZaLgMPt6C6d8xY+FzAhg==; _gcl_au=1.1.1810869406.1761569722; frontend-offer-card.consultant_chat_onboarding_shown=1; DMIR_AUTH=mgy0rTyxBQExFI3hRrY9WIt9MvSCNFqa%2Bzm4IVGqXQ9E8uImyZAXcovTzLMZHu7sJH4NX6mSM79OHryqc6JMCg6IZN%2BCR6kVHv2iHQDRCix7gDY4nA5zopU3Z1k%2Bk7QMya2T%2FiJkoY45KVHVZ69nC6%2FBBBzXENqOvTIyvNZ%2BCo8%3D; forever_region_id=4606; forever_region_name=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; forever_main_town_region_id=4959; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:53632938357|ad:16644615549|grp:5511051039|drf:no|dev:desktop|p:premium|n:2|reg:10758|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&ybaip=1&yclid=6818025664178814975; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; countCallNowPopupShowed=2%3A1763362751209; _ym_isad=2; _yasc=dgiUeSTPP193oguKbYFBFb1Idz2vYwWtXrx0xl3VIrYLH03hVlarYLoHlZjan+VQjw==; _yasc=zbfOUZCD2VRuDcJ56B/We1y6IbfxvVfDkP0EexZ2QVFbrEe1ZYDaRqx1eUI7xoiNsQ==; sopr_session=1e3dcee3e8a042cc; cookieUserID=8098251; _ym_visorc=b; uxfb_card_satisfaction=%5B323633012%2C319363085%2C322859138%2C319931163%5D; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1763474406$o363$g1$t1763475916$j58$l0$h0',
}

json_data = {
    'jsonQuery': {
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'page': {
            'type': 'term',
            'value': 3,
        },
        'object_type': {
            'type': 'terms',
            'value': [
                3,
            ],
        },
    },
}



def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


current_date = datetime.date.today()

repair_ids = [1, 2, 3, 4]
repair_ids_dict = {1: 'Без отделки', 2: 'Косметический', 3: 'Евроремонт', 4: 'Дизайнерский'}
rooms_ids = [4,5,6]

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

    rooms_ids = [[4, 5, 6]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [4, 5, 6]
    total_floor_list = [[1, 100]]

elif items_count >= 2500:

    rooms_ids = [4, 5, 6]
    total_floor_list = [[1, 100]]

print(json_data)

flats = []
counter = 1
total_count = 1


while len(flats) < total_count:

    if counter > 1:
        sleep_time = random.uniform(7, 9)
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
            finish_type = 'Дизайнерский'
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
    sleep_time = random.uniform(7, 9)
    time.sleep(sleep_time)

    counter += 1


base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{geo1}_{current_date}_{finish_type}_1.xlsx"

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

# merge_and_clean(folder_path, f'Вторичка_{geo1}_{current_date}.xlsx')


