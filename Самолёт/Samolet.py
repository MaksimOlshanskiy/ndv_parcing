'''

требуется менять cookie, а именно 'qrator_jsid'. Запросы через сессию

'''

# id всех проектов: [20,69054,5,57,44,68189,56,41,69057,69011,68192,68188,69106,68199,69206,69208,45,40,68195,69103,21,68196,31,69101,68194,3,69051,55,1,49,69109,68185,7,4,42,69100,69110]

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from Developer_dict import developer_dict, name_dict
from functions import save_flats_to_excel

cookies = {
    '_ymab_param': 'P15BM57IFcN4znqAS1vVwHOk9DT3n9SIZ8GVWjDL2Hib40HmRUaEiWD7VOriRwJ7sCBjxJyYprvjSOkY-ihlYEJ8l08',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'suggested_city': '1',
    '_ym_uid': '178021971762746810',
    '_ym_d': '1782932192',
    'gbuuid': '88b4e310-7552-4933-a9f1-dd5b83503396',
    'tmr_lvid': '4650332b84eabbf6fe29fefaebfde699',
    'tmr_lvidTS': '1780219717487',
    'cookies_accepted': '1',
    'gb_cache_variant': '%7B%22exp%3Ahome_page_new_version%22%3A0%7D',
    '_ct': '1300000000641807662',
    '_ct_client_global_id': '089407ce-d8b4-596e-88ef-eee2bfcb3172',
    'city_approved': '1',
    'qrator_jsr': '1787686542.298.g9r3Gv9lGGvB03EO-ds5b22l9lcpjfnjfc7e9117v66vh6bl3-00',
    'qrator_jsid': '1787686542.298.g9r3Gv9lGGvB03EO-qkfvtv48mefnruogn5s4e8b0vgnqi235',
    '__flats_v3_query_params_by_slug': '%7B%7D',
    'cted': 'modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810',
    'vp_width': '1600',
    '_ct_ids': 'htlowve6%3A36409%3A1052520215',
    '_ct_session_id': '1052520215',
    '_ct_site_id': '36409',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'nxt-city': '%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D',
    'call_s': '___htlowve6.1787688356.1052520215.185717:571622|2___',
    'user_account_return_url_session': '%2Fflats%2F',
    'csrftoken': 'u3JOihJBZuJbf9ml7lkIoBB0HUgOw44ghKw4wBcNut8wvOMae8MDIYEtIJCYOPfK',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-major-260819,sentry-public_key=6f0fe185684eda71da9741fe58c43591,sentry-trace_id=91ceb15f9767426ab463c4f8b4a99076,sentry-transaction=%2Fflats,sentry-sampled=true,sentry-sample_rand=0.00986633829473793,sentry-sample_rate=0.05',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/flats/',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-height': '865',
    'sec-ch-viewport-width': '1017',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '91ceb15f9767426ab463c4f8b4a99076-b187413b0b3cc305-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    # 'cookie': '_ymab_param=P15BM57IFcN4znqAS1vVwHOk9DT3n9SIZ8GVWjDL2Hib40HmRUaEiWD7VOriRwJ7sCBjxJyYprvjSOkY-ihlYEJ8l08; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; suggested_city=1; _ym_uid=178021971762746810; _ym_d=1782932192; gbuuid=88b4e310-7552-4933-a9f1-dd5b83503396; tmr_lvid=4650332b84eabbf6fe29fefaebfde699; tmr_lvidTS=1780219717487; cookies_accepted=1; gb_cache_variant=%7B%22exp%3Ahome_page_new_version%22%3A0%7D; _ct=1300000000641807662; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; city_approved=1; qrator_jsr=1787686542.298.g9r3Gv9lGGvB03EO-ds5b22l9lcpjfnjfc7e9117v66vh6bl3-00; qrator_jsid=1787686542.298.g9r3Gv9lGGvB03EO-qkfvtv48mefnruogn5s4e8b0vgnqi235; __flats_v3_query_params_by_slug=%7B%7D; cted=modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810; vp_width=1600; _ct_ids=htlowve6%3A36409%3A1052520215; _ct_session_id=1052520215; _ct_site_id=36409; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; nxt-city=%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D; call_s=___htlowve6.1787688356.1052520215.185717:571622|2___; user_account_return_url_session=%2Fflats%2F; csrftoken=u3JOihJBZuJbf9ml7lkIoBB0HUgOw44ghKw4wBcNut8wvOMae8MDIYEtIJCYOPfK',
}


params = {
    "nameType": "sale",
    "free": 1,
    "type": 100000000,
    "ordering": "-order_manual,filter_price_package,pk",
    "offset": 0,
    "limit": 12,
    "page": 1
}

projects = [20,69054,5,57,44,68189,56,41,69057,69011,68192,68188,69106,68199,69206,69208,45,40,68195,69103,21,68196,31,69101,68194,3,69051,55,1,49,69109,68185,7,4,42,69100,69110]


session = requests.Session()


parsed_flat_count = 0
flats = []


while True:

    url = 'https://samolet.ru/backend/api_redesign/flats/'
    response = session.get(
        url=url,
        headers=headers,
        cookies=cookies,
        params=params
    )

    print(response.status_code)

    items = response.json()["results"]
    # total_flat_count = response.json()["count"]



    for i in items:

        url = i['url']
        developer = "Самолет"
        project = i["project"]
        korpus = i["building"]
        if i['is_apartment'] is True:
            type = 'Апартаменты'
        else:
            type = 'Квартиры'
        if i["default_decor_type"] == None:
            finish_type = "Без отделки"
        elif i["default_decor_type"] == 1 or i["default_decor_type"] == 0 or i["default_decor_type"] == 2:
            if i["is_kitchen_included_in_price"] == False:
                finish_type = "С отделкой"
            else:
                finish_type = "С отделкой и доп опциями"
        elif i["default_decor_type"] == 3:
            finish_type = "Предчистовая"
        else:
            finish_type = i["default_decor_type"]
        if i["rooms"] == 0 or i["rooms"] == -1:
            room_count = 'Студия'
        else:
            room_count = int(i["rooms"])
        if i['euro'] is True and room_count != 'Студия':
            room_count += 1
            room_count = str(room_count) + 'е'

        try:
            area = float(i["area"])
        except:
            area = ''
        try:
            price = int(i["filter_price_package"])

        except:
            price = ''
        try:
            old_price = int(i["old_filter_price_package"])
        except:
            old_price = ''
        if not old_price:
            old_price = price

        section = i["section"]
        try:
            floor = int(i["floor_number"])
        except:
            floor = ''
        flat_number = ''
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
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = i['settling_date_formatted']
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        date = datetime.now().date()

        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type}, срок сдачи: {srok_sdachi}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                  mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, url, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break
    # print(f"Выполнено на {round(parsed_flat_count * 100 / total_flat_count, 2)} процентов")

    params['offset'] += 12
    params['page'] += 1

    sleep_time = random.uniform(0.5, 2)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

