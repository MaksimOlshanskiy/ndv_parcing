import requests
import datetime
import time
import pandas as pd
import os
import random

from jedi.api import file_name

from functions import merge_and_clean, haversine
import json

# noinspection PyDictDuplicateKeys
cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
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
    'forever_region_id': '4593',
    'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobFn5tI1ULEF9APV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXSlRCg4Ybkp1cyxDaSFneFwldlYKCVdPRggnKwoPEGNuRip7X0BuH2RPFyRKV1UzWxxCNW4mCRAUYEBIdHQqQB4PWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdSCCcZF3twJ1J7dScOCSplMy0tWRgIH2N4JRlrcmY=6fyd8A==',
    'cfidsw-cian': 'diusco/HSHrB9muzOk+431TeS6cQwA2I56HMt/7brov/94HTt6PZxKAttqRA7cknvlkPExofzYUUaNpGYM2H3DX5+hW6lp34e+dk6dKONIrD4BtCmA9ax5zv9A5uVB4jEA/l10JrXkqxq87yHcnzszymNb9JyssBbvtBWHxb',
    'gsscw-cian': 'fWi9cwYAjXKpsYlye2CIqEFatNR4EzAzID3Zv8nXkSLj2gG3G+rhCtmTIBBXqIffuzxFFT0I3QaemDa69+WG6yhz8jocBX9XoM1QZ9WOLsAbuE554o6WsFW2SlrMKXGaXvZx38BtHWGZTxEUGCedMrZGjNCnDnyWb6wDb+lhWZ/3ICCKy8gqOujBw7e44OzzFAx5nLhMDNDyVOf8JUYkPc2St/9z2O7Gz+ihq/Kr7XZw5LL+akepnMYjfqpBEVBBwoKgBCYOkI/4/TKnYg==',
    'fgsscw-cian': '5dqc76ef4ba5a714de38640aa08605216bfb216e',
    'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
    '_gcl_au': '1.1.730586332.1753699444',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:52037806106|ad:16202020484|grp:5454186765|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&yclid=4414867700825718783',
    'DMIR_AUTH': 'KaxPvqgCTBCI5zCe%2FjZEmCDp2qM0RCK2hIVrc%2BBeEt7NRmQr1%2BnsiC%2BbHZ3iUSROflUa18%2BMHTLVVCblh6fvxHSLY6xnYFAHzAPDGcpuV03ZLPabLxOU4bSj2cQYuC%2B4UVbQP%2FkU%2BbmhOCHACsyC4ouWMMu2h9bVJeu458AFWWE%3D',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'rrpvid': '771260525504896',
    'rcuid': '67e27578d41e2c9a8a114add',
    'F6_CIAN_SID': '2d0d2794e97e6e79802163da7bbe16360dd116dd0dffcd58a510b35388de706f',
    '_ym_isad': '2',
    'session_region_id': '4820',
    'session_main_town_region_id': '4820',
    'countCallNowPopupShowed': '1%3A1754392030516',
    '_yasc': 'Rx8/kjbQXML3XheE7gdCnjr4dL1FnqxkN3Id+8soVKYUe2bV2BKe+O8g0t+/0D6GYaM=',
    'F6_CIAN_UID': '8098251',
    '_yasc': 't3zeYqoVISApPynimhXVtQIVX+VEjCKgXC68pqmluVwnCpBhUUoX73uKe5e/9UwPW1c=',
    'sopr_session': '4809e916fe2040e4',
    'cookieUserID': '8098251',
    '_ym_visorc': 'b',
    'uxfb_card_satisfaction': '%5B305455884%2C319149332%2C314358350%2C306236662%5D',
    'cfidsw-cian': 'JevClYyqu4xnr5IdnzWEyvxjvYh/gulO8h6lncNqo/8wDciHJ8rCKlHGpsDIJ9hl+BANTmVzBf1f/WtRHkkCyIDK2E3CJ4Zs6x26Ka0BBL2UQGj86QfHoS0uJBR/P52AlB5pcoiOm9W2PmNflPpUCJlST1M2uA6elKA8+2mu',
    'fgsscw-cian': 'M7sx47635bb5b204cb5a694ab604226b42610fbf',
    'gsscw-cian': 'hEt7/3Xo0ldTvJsb9jO5itQ53tJCNytOmREaShRa6BgWuO6hLtbkYoB8qC8KcP1mngKjvyJ2RBfhvVEodXPOGyevTbDLv1jTfsgU7eAWrcqsdcs2UJkD9ik+31xHsxVs5HRKeSpront7+4px7pVzUBrBz2pLEmC4QhB1bs2h8K9J/seT5oa27eHfDQAnitxRwlj4/wV79dSZzMoWUK2hUUVhLcth2KTwp+AWXb9MaUNuDi+8wAy0whjdtifVwnD6cpWUxVxr+RRu9cJIieK4RUGMv1Q=',
    '_ga_3369S417EL': 'GS2.1.s1754403489$o143$g1$t1754404041$j43$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://krasnodar.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://krasnodar.cian.ru/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; _ga=GA1.1.460280003.1749468781; uxfb_usertype=searcher; uxs_uid=1ed08180-4604-11f0-94f5-19dbce91137e; seen_cpd_landing=1; cian_ruid=8098251; map_preview_onboarding_counter=3; frontend-serp.offer_chat_onboarding_shown=1; forever_region_id=4593; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobFn5tI1ULEF9APV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXSlRCg4Ybkp1cyxDaSFneFwldlYKCVdPRggnKwoPEGNuRip7X0BuH2RPFyRKV1UzWxxCNW4mCRAUYEBIdHQqQB4PWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdSCCcZF3twJ1J7dScOCSplMy0tWRgIH2N4JRlrcmY=6fyd8A==; cfidsw-cian=diusco/HSHrB9muzOk+431TeS6cQwA2I56HMt/7brov/94HTt6PZxKAttqRA7cknvlkPExofzYUUaNpGYM2H3DX5+hW6lp34e+dk6dKONIrD4BtCmA9ax5zv9A5uVB4jEA/l10JrXkqxq87yHcnzszymNb9JyssBbvtBWHxb; gsscw-cian=fWi9cwYAjXKpsYlye2CIqEFatNR4EzAzID3Zv8nXkSLj2gG3G+rhCtmTIBBXqIffuzxFFT0I3QaemDa69+WG6yhz8jocBX9XoM1QZ9WOLsAbuE554o6WsFW2SlrMKXGaXvZx38BtHWGZTxEUGCedMrZGjNCnDnyWb6wDb+lhWZ/3ICCKy8gqOujBw7e44OzzFAx5nLhMDNDyVOf8JUYkPc2St/9z2O7Gz+ihq/Kr7XZw5LL+akepnMYjfqpBEVBBwoKgBCYOkI/4/TKnYg==; fgsscw-cian=5dqc76ef4ba5a714de38640aa08605216bfb216e; frontend-offer-card.newbuilding_broker_onboarding_shown=1; _gcl_au=1.1.730586332.1753699444; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:52037806106|ad:16202020484|grp:5454186765|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&yclid=4414867700825718783; DMIR_AUTH=KaxPvqgCTBCI5zCe%2FjZEmCDp2qM0RCK2hIVrc%2BBeEt7NRmQr1%2BnsiC%2BbHZ3iUSROflUa18%2BMHTLVVCblh6fvxHSLY6xnYFAHzAPDGcpuV03ZLPabLxOU4bSj2cQYuC%2B4UVbQP%2FkU%2BbmhOCHACsyC4ouWMMu2h9bVJeu458AFWWE%3D; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; rrpvid=771260525504896; rcuid=67e27578d41e2c9a8a114add; F6_CIAN_SID=2d0d2794e97e6e79802163da7bbe16360dd116dd0dffcd58a510b35388de706f; _ym_isad=2; session_region_id=4820; session_main_town_region_id=4820; countCallNowPopupShowed=1%3A1754392030516; _yasc=Rx8/kjbQXML3XheE7gdCnjr4dL1FnqxkN3Id+8soVKYUe2bV2BKe+O8g0t+/0D6GYaM=; F6_CIAN_UID=8098251; _yasc=t3zeYqoVISApPynimhXVtQIVX+VEjCKgXC68pqmluVwnCpBhUUoX73uKe5e/9UwPW1c=; sopr_session=4809e916fe2040e4; cookieUserID=8098251; _ym_visorc=b; uxfb_card_satisfaction=%5B305455884%2C319149332%2C314358350%2C306236662%5D; cfidsw-cian=JevClYyqu4xnr5IdnzWEyvxjvYh/gulO8h6lncNqo/8wDciHJ8rCKlHGpsDIJ9hl+BANTmVzBf1f/WtRHkkCyIDK2E3CJ4Zs6x26Ka0BBL2UQGj86QfHoS0uJBR/P52AlB5pcoiOm9W2PmNflPpUCJlST1M2uA6elKA8+2mu; fgsscw-cian=M7sx47635bb5b204cb5a694ab604226b42610fbf; gsscw-cian=hEt7/3Xo0ldTvJsb9jO5itQ53tJCNytOmREaShRa6BgWuO6hLtbkYoB8qC8KcP1mngKjvyJ2RBfhvVEodXPOGyevTbDLv1jTfsgU7eAWrcqsdcs2UJkD9ik+31xHsxVs5HRKeSpront7+4px7pVzUBrBz2pLEmC4QhB1bs2h8K9J/seT5oa27eHfDQAnitxRwlj4/wV79dSZzMoWUK2hUUVhLcth2KTwp+AWXb9MaUNuDi+8wAy0whjdtifVwnD6cpWUxVxr+RRu9cJIieK4RUGMv1Q=; _ga_3369S417EL=GS2.1.s1754403489$o143$g1$t1754404041$j43$l0$h0',
}

json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'region': {
            'type': 'terms',
            'value': [
                5024,
            ],
        },
        'repair': {
            'type': 'terms',
            'value': [
                2,
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 99,
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
        'flat_share': {
            'type': 'term',
            'value': 2,
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
        'electronic_trading': {
            'type': 'term',
            'value': 2,
        },
    },
}

cities_dict = {
    'Москва': 1,
    'Санкт-Петербург': 2,
    'Новосибирск': 4897,
    'Екатеринбург': 4743,
    'Казань': 4777,
    'Красноярск': 4827,
    'Нижний Новгород': 4885,
    'Челябинск': 5048,
    'Уфа': 176245,
    'Краснодар': 4820,
    'Самара': 4966,
    'Ростов-на-Дону': 4959,
    'Омск': 4914,
    'Воронеж': 4713,
    'Пермь': 4927,
    'Волгоград': 4704
}


print("Список доступных регионов:")
for city, city_id in cities_dict.items():
    print(f"{city}: {city_id}")

user_input = input("\nВведите ID нужного региона или введите свой: ")

with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

coords = city_centers.get(user_input)

try:
    user_id = int(user_input)
    if user_id in cities_dict.values():
        selected_city = [city for city, cid in cities_dict.items() if cid == user_id][0]
        print(f"\nВы выбрали город: {selected_city}")
    else:
        print("\nГород не в списке")
except ValueError:
    print("\nОшибка: введите числовой ID.")

json_data['jsonQuery']['region']['value'] = [user_input]

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

start_time = time.time()
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
city_in_work = response.json()['data']['breadcrumbs'][0]['title']
print(city_in_work)


if items_count <=  1500:

    rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
    total_floor_list = [[1, 100]]

elif  1500 < items_count < 2500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 100]]

elif 2500 <= items_count <= 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 6], [7, 12], [13, 200]]

elif items_count > 4500:

    rooms_ids = [[1], [2], [3], [4], [5], [6], [7], [9]]
    total_floor_list = [[1, 3], [4, 7], [8, 15], [16, 200]]


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
            counter = 1
            total_count = 1



            while len(flats) < total_count:

                if counter > 1:
                    sleep_time = random.uniform(7, 10)
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

                    new_result = {
                        ('mikroraion' if isinstance(v, str) and 'мкр' in v else k): v
                        for k, v in result.items()
                    }
                    result = new_result
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
                        finish_type = repair_ids_dict.get(repair_id)
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

                    print(
                        f"{url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                    result = [project, developer, location, location2, okrug, raion, mikroraion, metro, street, house,
                              korpus, distance, srok_sdachi, type,
                              finish_type, room_count, area, kitchenArea, livingArea, price, floor,
                              balconies_and_loggias_count, parking, url]
                    flats.append(result)

                if not items:
                    break
                json_data["jsonQuery"]["page"]["value"] += 1
                print(len(flats))
                print("-----------------------------------------------------------------------------")
                total_count = response.json()["data"]["offerCount"]
                downloaded = len(flats)
                print()
                counter += 1

            if len(flats) > 1:

                df = pd.DataFrame(flats, columns=['Название проекта',
                                                        'Девелопер',
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

                folder_path = os.path.join(base_path, str(current_date))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)


                def sanitize_filename(name):
                    for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                        name = name.replace(char, '_')
                    return name


                project = sanitize_filename(project)
                filename = f"{city_in_work}__{current_date}_{name_counter}.xlsx"

                # Полный путь к файлу0
                file_path = os.path.join(folder_path, filename)

                # Сохранение файла в папку
                try:
                    df.to_excel(file_path, index=False)
                    print(f'Сохранён файл {file_path}')
                except:
                    filename = f"{project}_{current_date}_2.xlsx"
                    file_path = os.path.join(folder_path, filename)
                    df.to_excel(file_path, index=False)

merge_and_clean(folder_path, f'Вторичка_{city_in_work}_{current_date}.xlsx')
