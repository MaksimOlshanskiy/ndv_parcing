'''

требуется менять cookie, а именно 'qrator_jsid'. Запросы через сессию
квартиры по аукциону пропускаются

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
    '_ym_isad': '2',
    'domain_sid': 'K6lBtB6ix-80M4PxMEHLX%3A1786469294149',
    'city_approved': '1',
    'nxt-city': '%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D',
    'vp_width': '1920',
    'cted': 'modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810',
    '_ct_site_id': '36409',
    'nxt-city-selected': 'true',
    'city_approved_url_prefix': '',
    'helperBlockWatch': 'header',
    'sessionid': '1lk7ok5chs9kpd37t24xtrc549catcdb',
    'pageviewTimerCommercial': '2983.582',
    'pageviewTimerAll': '2983.582',
    'pageviewTimerMSK': '2983.582',
    'pageviewTimerCommercialFired1min': 'true',
    'pageviewTimerCommercialFired2min': 'true',
    'pageviewTimerCommercialFired5min': 'true',
    'pageviewTimerCommercialFired10min': 'true',
    'pageviewTimerCommercialFired15min': 'true',
    'pageviewTimerAllFired1min': 'true',
    'pageviewTimerAllFired2min': 'true',
    'pageviewTimerAllFired5min': 'true',
    'pageviewTimerAllFired10min': 'true',
    'pageviewTimerAllFired15min': 'true',
    'pageviewTimerAllFired30min': 'true',
    'pageviewTimerAllFired45min': 'true',
    'pageviewTimerMSKFired1min': 'true',
    'pageviewTimerMSKFired2min': 'true',
    'pageviewTimerMSKFired5min': 'true',
    'pageviewTimerMSKFired10min': 'true',
    'pageviewTimerMSKFired15min': 'true',
    'pageviewTimerMSKFired45min': 'true',
    'qrator_jsr': '1786533848.436.KHWTTl4pFR4jAgn3-6sed2u1roulpcni8isod30j222uhfr5r-00',
    'qrator_jsid': '1786533848.436.KHWTTl4pFR4jAgn3-gv71ms9jhui2j6uv5g3b2n362gajvdmn',
    '_ym_visorc': 'b',
    '_ct_ids': 'htlowve6%3A36409%3A1048725254',
    '_ct_session_id': '1048725254',
    'user_account_return_url_session': '%2Fcommercial%2F%3Futm_referrer%3Dhttps%3A%2F%2Fsamolet.ru%2Fcommercial%2Fobjects%2Fsale%2F%3Fproject%3D68199%2526type%3D100000000',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'pageviewCount': '2',
    'pageviewCountMSK': '2',
    'csrftoken': '2tI96drCcOXtscf8rOur5YOPGxgAdso1rFObmYEZjHxAh8eB3IuVQ5hk9hWa9G7q',
    'call_s': '___htlowve6.1786535654.1048725254.143945:445562|2___',
    'tmr_detect': '0%7C1786533858181',
    'Fired15sec': 'true',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-major-260812,sentry-public_key=e92b18b752b5a57fcab9400337321152,sentry-trace_id=0d4c23707c434ecc8bf9f640e0381080,sentry-sample_rate=0.1,sentry-sampled=false',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/commercial/objects/sale/?ordering=price,pk&free=1',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-height': '945',
    'sec-ch-viewport-width': '1095',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '0d4c23707c434ecc8bf9f640e0381080-9d6e31174956c462-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    # 'cookie': '_ymab_param=P15BM57IFcN4znqAS1vVwHOk9DT3n9SIZ8GVWjDL2Hib40HmRUaEiWD7VOriRwJ7sCBjxJyYprvjSOkY-ihlYEJ8l08; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; suggested_city=1; _ym_uid=178021971762746810; _ym_d=1782932192; gbuuid=88b4e310-7552-4933-a9f1-dd5b83503396; tmr_lvid=4650332b84eabbf6fe29fefaebfde699; tmr_lvidTS=1780219717487; cookies_accepted=1; gb_cache_variant=%7B%22exp%3Ahome_page_new_version%22%3A0%7D; _ct=1300000000641807662; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; _ym_isad=2; domain_sid=K6lBtB6ix-80M4PxMEHLX%3A1786469294149; city_approved=1; nxt-city=%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D; vp_width=1920; cted=modId%3Dhtlowve6%3Bya_client_id%3D178021971762746810; _ct_site_id=36409; nxt-city-selected=true; city_approved_url_prefix=; helperBlockWatch=header; sessionid=1lk7ok5chs9kpd37t24xtrc549catcdb; pageviewTimerCommercial=2983.582; pageviewTimerAll=2983.582; pageviewTimerMSK=2983.582; pageviewTimerCommercialFired1min=true; pageviewTimerCommercialFired2min=true; pageviewTimerCommercialFired5min=true; pageviewTimerCommercialFired10min=true; pageviewTimerCommercialFired15min=true; pageviewTimerAllFired1min=true; pageviewTimerAllFired2min=true; pageviewTimerAllFired5min=true; pageviewTimerAllFired10min=true; pageviewTimerAllFired15min=true; pageviewTimerAllFired30min=true; pageviewTimerAllFired45min=true; pageviewTimerMSKFired1min=true; pageviewTimerMSKFired2min=true; pageviewTimerMSKFired5min=true; pageviewTimerMSKFired10min=true; pageviewTimerMSKFired15min=true; pageviewTimerMSKFired45min=true; qrator_jsr=1786533848.436.KHWTTl4pFR4jAgn3-6sed2u1roulpcni8isod30j222uhfr5r-00; qrator_jsid=1786533848.436.KHWTTl4pFR4jAgn3-gv71ms9jhui2j6uv5g3b2n362gajvdmn; _ym_visorc=b; _ct_ids=htlowve6%3A36409%3A1048725254; _ct_session_id=1048725254; user_account_return_url_session=%2Fcommercial%2F%3Futm_referrer%3Dhttps%3A%2F%2Fsamolet.ru%2Fcommercial%2Fobjects%2Fsale%2F%3Fproject%3D68199%2526type%3D100000000; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; pageviewCount=2; pageviewCountMSK=2; csrftoken=2tI96drCcOXtscf8rOur5YOPGxgAdso1rFObmYEZjHxAh8eB3IuVQ5hk9hWa9G7q; call_s=___htlowve6.1786535654.1048725254.143945:445562|2___; tmr_detect=0%7C1786533858181; Fired15sec=true',
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

            if i['auction']:
                continue

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

