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
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_ct': '1300000000514654067',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ymab_param': '8XRBcNsyXKtIDbacrAc2BACgO21rCm8Ag3D9zrGpvAndIxB0P18Yxc_5KjOr3ip1jyUFVoI_vSab5fXPK7ntewsKWyM',
    'suggested_city': '1',
    '_ym_uid': '1741678176664168974',
    '_ym_d': '1741678176',
    '_ga': 'GA1.1.1264916353.1741678184',
    'FPID': 'FPID2.2.CDdF7rEkFIS%2FekBLl3jtW7K80kFov3hiqvjbDmcAEcw%3D.1741678184',
    'tmr_lvid': '609b80c61abf0ce366c33bbd78503b61',
    'tmr_lvidTS': '1741678183827',
    'cookies_accepted': '1',
    '_smt': '1bdc3b2d-db01-43f7-9fc0-bb05e3cca9e5',
    '_ga_2WZB3B8QT0': 'deleted',
    'sessionid': 'fjwvpzyyv4mdr7fqyunk6j9z5niagehb',
    'tmr_lvid': '609b80c61abf0ce366c33bbd78503b61',
    'tmr_lvidTS': '1741678183827',
    '_ga_2WZB3B8QT0': 'GS2.1.s1751029258$o36$g1$t1751029931$j58$l0$h2027757047',
    'qrator_jsr': '1756121066.530.KkRNw6Xu0qrirtYL-ptm7unhevihgtvbb2kukmpqu4o5676sf-00',
    'qrator_jsid': '1756121066.530.KkRNw6Xu0qrirtYL-8gsmccra7jjbc0agu6realauld3pa2tt',
    'cted': 'modId%3Dhtlowve6%3Bclient_id%3D1264916353.1741678184%3Bya_client_id%3D1741678176664168974',
    '_ct_ids': 'htlowve6%3A36409%3A907792714',
    '_ct_session_id': '907792714',
    '_ct_site_id': '36409',
    'vp_width': '2560',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'city_was_suggested': '1',
    'session_timer_104054': '1',
    'domain_sid': 'pPz3-bLEHe1VOjIhFyQ_1%3A1756121085498',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'nxt-city': '%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D',
    'undefined': '2.963',
    'pageviewTimerAll': '2.963',
    'pageviewTimerMSK': '2.963',
    'tmr_detect': '0%7C1756121098270',
    'seconds_on_page_104054': '4',
    'call_s': '___htlowve6.1756122909.907792714.143945:445562|2___',
    'user_account_return_url_session': '%2Fflats%2F%3Ffrom%3Dproject%26project%3D57%26free%3D1',
    'csrftoken': 'TIVI4dAvDqVPH2REe0OnMn45xlvgCt4fJTvhs0Pslwl5MITgLzFz6Ay91e8vNcBX',
    'pageviewCount': '4',
    'pageviewCountMSK': '4',
    'PageNumber': '4',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-major-250821,sentry-public_key=6f0fe185684eda71da9741fe58c43591,sentry-trace_id=850e68beac6e416695db9c4182494233,sentry-sampled=false,sentry-sample_rand=0.4975722257377354,sentry-sample_rate=0.05',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/flats/?from=project&project=57&free=1',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-height': '945',
    'sec-ch-viewport-width': '1323',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '850e68beac6e416695db9c4182494233-81d4eaa19b21c948-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    # 'cookie': 'popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ct=1300000000514654067; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ymab_param=8XRBcNsyXKtIDbacrAc2BACgO21rCm8Ag3D9zrGpvAndIxB0P18Yxc_5KjOr3ip1jyUFVoI_vSab5fXPK7ntewsKWyM; suggested_city=1; _ym_uid=1741678176664168974; _ym_d=1741678176; _ga=GA1.1.1264916353.1741678184; FPID=FPID2.2.CDdF7rEkFIS%2FekBLl3jtW7K80kFov3hiqvjbDmcAEcw%3D.1741678184; tmr_lvid=609b80c61abf0ce366c33bbd78503b61; tmr_lvidTS=1741678183827; cookies_accepted=1; _smt=1bdc3b2d-db01-43f7-9fc0-bb05e3cca9e5; _ga_2WZB3B8QT0=deleted; sessionid=fjwvpzyyv4mdr7fqyunk6j9z5niagehb; tmr_lvid=609b80c61abf0ce366c33bbd78503b61; tmr_lvidTS=1741678183827; _ga_2WZB3B8QT0=GS2.1.s1751029258$o36$g1$t1751029931$j58$l0$h2027757047; qrator_jsr=1756121066.530.KkRNw6Xu0qrirtYL-ptm7unhevihgtvbb2kukmpqu4o5676sf-00; qrator_jsid=1756121066.530.KkRNw6Xu0qrirtYL-8gsmccra7jjbc0agu6realauld3pa2tt; cted=modId%3Dhtlowve6%3Bclient_id%3D1264916353.1741678184%3Bya_client_id%3D1741678176664168974; _ct_ids=htlowve6%3A36409%3A907792714; _ct_session_id=907792714; _ct_site_id=36409; vp_width=2560; _ym_isad=2; _ym_visorc=b; city_was_suggested=1; session_timer_104054=1; domain_sid=pPz3-bLEHe1VOjIhFyQ_1%3A1756121085498; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; nxt-city=%7B%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D; undefined=2.963; pageviewTimerAll=2.963; pageviewTimerMSK=2.963; tmr_detect=0%7C1756121098270; seconds_on_page_104054=4; call_s=___htlowve6.1756122909.907792714.143945:445562|2___; user_account_return_url_session=%2Fflats%2F%3Ffrom%3Dproject%26project%3D57%26free%3D1; csrftoken=TIVI4dAvDqVPH2REe0OnMn45xlvgCt4fJTvhs0Pslwl5MITgLzFz6Ay91e8vNcBX; pageviewCount=4; pageviewCountMSK=4; PageNumber=4',
}

params = {
    "nameType": "sale",
    "free": 1,
    "type": 100000000,
    "ordering": "-order_manual,filter_price_package,pk",
    "offset": 0,
    "limit": 12,
    "page": 1,
    "project": 68188
}

projects = [68195,7,20,69054,5,57,69104,44,68189,56,41,69057,69011,68192,68188,68191,69106,69108,68199,69206,2,45,40,69103,68196,31,69101,68194,3,69051,55,1,49,69109,68185,69102,4,42,69100,69110]


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
            if int(i["rooms"]) == 0 or int(i["rooms"]) == -1:
                room_count = 0
            else:
                room_count = int(i["rooms"])
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
            srok_sdachi = i["settling_date_formatted"]
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

save_flats_to_excel(flats, project, developer)

