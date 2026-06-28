'''

требуется менять cookie, а именно 'qrator_jsid'. Запросы через сессию

'''

# id всех проектов: [68195,7,20,69054,5,57,69104,44,68189,56,41,69057,69011,68192,68188,68191,69106,69108,68199,69206,2,45,40,69103,21,68196,31,69101,68194,3,69051,55,1,49,68185,69102,4,42,69100,69110]

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
    '_ymab_param': 'sz_QgQZpMz-NbtHY7nJb1QX10-JOBmDUPkHcAkuel91YLiWgAq1GDAz4YKiumc8N8fVkJbMS3e6_tuBkRAu2aU-2IAQ',
    '_smt': 'e91f4352-6c98-49f5-a418-d40d7821171d',
    '_ct': '1300000000630721453',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'suggested_city': '1',
    'gbuuid': 'bfcf6368-44d8-4c6b-8e58-6ce4c4797275',
    'gb_cache_variant': '%7B%22exp%3Ahome_page_new_version%22%3A0%7D',
    '_ym_uid': '178021971762746810',
    '_ym_d': '1780219717',
    'tmr_lvid': '4650332b84eabbf6fe29fefaebfde699',
    'tmr_lvidTS': '1780219717487',
    'qrator_jsr': '1781628415.626.rV29Tbm4J4kZpkou-rlk3qnjkmhdcds9076nrp8h083jimdhi-00',
    'qrator_jsid': '1781628415.626.rV29Tbm4J4kZpkou-s8avleor1entuc3ru45nhg6sqt8d3iv4',
    'cted': 'modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810',
    'vp_width': '1099',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_ct_ids': 'htlowve6%3A36409%3A1031882121',
    '_ct_session_id': '1031882121',
    '_ct_site_id': '36409',
    'nxt-city': '%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'domain_sid': 'K6lBtB6ix-80M4PxMEHLX%3A1781628422972',
    'nxt-city-selected': 'true',
    'city_approved_url_prefix': '',
    'city_approved': '1',
    'Fired15sec': 'true',
    'pageviewTimerAll': '32.31',
    'pageviewTimerMSK': '32.31',
    '__flats_v3_query_params_by_slug': '%7B%7D',
    'pageviewCount': '4',
    'pageviewCountMSK': '4',
    'call_s': '___htlowve6.1781630258.1031882121.185717:571622|2___',
    'csrftoken': 'ScXvg6Cpvq3Udav18kJSpYKMfogW6no60IhUO9pNOR5lTraly4oexXprVTBeXaxG',
    'user_account_return_url_session': '%2Fflats%2F%3FnameType%3Dsale%26free%3D0%26type%3D100000000%26ordering%3D-order_manual%2Cfilter_price_package%2Cpk%26group_mode%3Dlayout',
    'tmr_detect': '0%7C1781628464598',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-major-260610,sentry-public_key=6f0fe185684eda71da9741fe58c43591,sentry-trace_id=4b573af086794f00aaeb51b804dcc4c9,sentry-transaction=%2Fflats,sentry-sampled=false,sentry-sample_rand=0.587803015324636,sentry-sample_rate=0.05',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/flats/?nameType=sale&free=0&type=100000000&ordering=-order_manual,filter_price_package,pk&group_mode=layout',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-height': '945',
    'sec-ch-viewport-width': '1099',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '4b573af086794f00aaeb51b804dcc4c9-8df88bed708b27ca-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_ymab_param=sz_QgQZpMz-NbtHY7nJb1QX10-JOBmDUPkHcAkuel91YLiWgAq1GDAz4YKiumc8N8fVkJbMS3e6_tuBkRAu2aU-2IAQ; _smt=e91f4352-6c98-49f5-a418-d40d7821171d; _ct=1300000000630721453; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; suggested_city=1; gbuuid=bfcf6368-44d8-4c6b-8e58-6ce4c4797275; gb_cache_variant=%7B%22exp%3Ahome_page_new_version%22%3A0%7D; _ym_uid=178021971762746810; _ym_d=1780219717; tmr_lvid=4650332b84eabbf6fe29fefaebfde699; tmr_lvidTS=1780219717487; qrator_jsr=1781628415.626.rV29Tbm4J4kZpkou-rlk3qnjkmhdcds9076nrp8h083jimdhi-00; qrator_jsid=1781628415.626.rV29Tbm4J4kZpkou-s8avleor1entuc3ru45nhg6sqt8d3iv4; cted=modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810; vp_width=1099; _ym_isad=2; _ym_visorc=b; _ct_ids=htlowve6%3A36409%3A1031882121; _ct_session_id=1031882121; _ct_site_id=36409; nxt-city=%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; domain_sid=K6lBtB6ix-80M4PxMEHLX%3A1781628422972; nxt-city-selected=true; city_approved_url_prefix=; city_approved=1; Fired15sec=true; pageviewTimerAll=32.31; pageviewTimerMSK=32.31; __flats_v3_query_params_by_slug=%7B%7D; pageviewCount=4; pageviewCountMSK=4; call_s=___htlowve6.1781630258.1031882121.185717:571622|2___; csrftoken=ScXvg6Cpvq3Udav18kJSpYKMfogW6no60IhUO9pNOR5lTraly4oexXprVTBeXaxG; user_account_return_url_session=%2Fflats%2F%3FnameType%3Dsale%26free%3D0%26type%3D100000000%26ordering%3D-order_manual%2Cfilter_price_package%2Cpk%26group_mode%3Dlayout; tmr_detect=0%7C1781628464598',
}


params = {
    "ordering": "price,pk",
    "free": 1,
    "project": 49,
    "filter_type": "standard",
    "type": 100000000,
    "name": "sale"
}

projects = [20,69054,5,57,44,68189,56,41,69057,69011,68192,68188,69106,68199,69206,69208,45,40,68195,69103,21,68196,31,69101,68194,3,69051,55,1,49,69109,68185,7,4,42,69100,69110]


session = requests.Session()


parsed_flat_count = 0
flats = []

for project in projects:


    offset = 0
    params['project'] = project
    params['offset'] = 0
    params['page'] = 1
    print(f"ЖК ID : {project}")

    while True:

        url = "https://samolet.ru/api_redesign/commercial_premises/"

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
            type = ''
            finish_type = "Без отделки"
            room_count = ''
            try:
                area = float(i["area"])
            except:
                area = ''
            try:
                price = int(i["price"])

            except:
                price = ''
            try:
                old_price = ''
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
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            price_per_metr = ''
            discount = ''
            price_per_metr_new = ''
            date = datetime.now().date()

            print(
                f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck, distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
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

save_flats_to_excel(flats, 'all', developer, kvartirografia=False)

