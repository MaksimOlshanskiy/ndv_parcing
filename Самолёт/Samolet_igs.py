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
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'cted': 'modId%3Dhtlowve6%3Bclient_id%3D1264916353.1741678184%3Bya_client_id%3D1741678176664168974',
    '_ct_site_id': '36409',
    '_ym_isad': '2',
    'nxt-city': '%7B%22id%22%3A1%2C%22pk%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22name_prep%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5%22%2C%22url_prefix%22%3A%22%22%2C%22active%22%3Atrue%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%2C%22has_active_office%22%3Atrue%2C%22translate%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%7D',
    'vp_width': '2560',
    'user_account_return_url_session': '%2F',
    'city_was_suggested': '1',
    'domain_sid': 'pPz3-bLEHe1VOjIhFyQ_1%3A1755673264235',
    'csrftoken': '8ZTuBDhOidNWwP3cY1ItnukmYyZeffA8',
    'tmr_detect': '0%7C1755673303618',
    'was_called_in_current_session_104054': '1',
    'undefined': '2955.282',
    'pageviewTimerAll': '2955.282',
    'pageviewTimerMSK': '2955.282',
    'pageviewTimerHoses': '2955.282',
    'pageviewTimerHoses150seconds': '1',
    'pageviewTimerHoses300seconds': '1',
    'pageviewTimerHoses600seconds': '1',
    'pageviewTimerAllFired1min': 'true',
    'pageviewTimerAllFired2min': 'true',
    'pageviewTimerAllFired5min': 'true',
    'pageviewTimerAllFired10min': 'true',
    'pageviewTimerAllFired15sec': 'true',
    'pageviewTimerAllFired15min': 'true',
    'pageviewTimerAllFired45min': 'true',
    'pageviewTimerAllFired30min': 'true',
    'pageviewTimerMSKFired1min': 'true',
    'pageviewTimerMSKFired2min': 'true',
    'pageviewTimerMSKFired5min': 'true',
    'pageviewTimerMSKFired10min': 'true',
    'pageviewTimerMSKFired15min': 'true',
    'pageviewTimerMSKFired45min': 'true',
    'qrator_jsr': '1755676254.160.OqFg7b6aWeg0lhzE-72flj9rcgck5hu5uo3lu4ijcbjpg8dee-00',
    'seconds_on_page_104054': '2981',
    'qrator_jsid': '1755676254.160.OqFg7b6aWeg0lhzE-f8einsd6utgq46rmtpf0b0ubt7pkae0c',
    '_ym_visorc': 'b',
    '_ct_ids': 'htlowve6%3A36409%3A905520004',
    '_ct_session_id': '905520004',
    'call_s': '___htlowve6.1755678060.905520004.363119:1024273|2___',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-fast-track-250818,sentry-public_key=e92b18b752b5a57fcab9400337321152,sentry-trace_id=00394d8333484a7eb5331c8c8e9f08ce,sentry-sample_rate=0.1,sentry-sampled=true',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/houses/objects/?project=69077&ordering=filter_price,pk&type=%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%91%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%BD%D0%B8,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%93%D0%B0%D1%80%D0%B4%D0%B8%D0%B0%D0%BD,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%94%D0%B5%D0%BB%D1%8C%D1%82%D0%B0,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%94%D1%8D%D0%BD%D1%84%D0%BE%D1%80%D0%B4,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%9D%D0%BE%D1%80%D1%82%D1%85%D0%B8%D0%BB,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0%20%D0%A4%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%81,XXS,XS,S,M,L,XL,%D0%92%D0%B8%D0%BB%D0%BB%D0%B0&utm_referrer=https%3A%2F%2Fsamolet.ru%2Fhouses%2Fistra_dom%2F',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-viewport-height': '945',
    'sec-ch-viewport-width': '1323',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '00394d8333484a7eb5331c8c8e9f08ce-9dd18105fd7f9e08-1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    # 'cookie': 'popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ct=1300000000514654067; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ymab_param=8XRBcNsyXKtIDbacrAc2BACgO21rCm8Ag3D9zrGpvAndIxB0P18Yxc_5KjOr3ip1jyUFVoI_vSab5fXPK7ntewsKWyM; suggested_city=1; _ym_uid=1741678176664168974; _ym_d=1741678176; _ga=GA1.1.1264916353.1741678184; FPID=FPID2.2.CDdF7rEkFIS%2FekBLl3jtW7K80kFov3hiqvjbDmcAEcw%3D.1741678184; tmr_lvid=609b80c61abf0ce366c33bbd78503b61; tmr_lvidTS=1741678183827; cookies_accepted=1; _smt=1bdc3b2d-db01-43f7-9fc0-bb05e3cca9e5; _ga_2WZB3B8QT0=deleted; sessionid=fjwvpzyyv4mdr7fqyunk6j9z5niagehb; tmr_lvid=609b80c61abf0ce366c33bbd78503b61; tmr_lvidTS=1741678183827; _ga_2WZB3B8QT0=GS2.1.s1751029258$o36$g1$t1751029931$j58$l0$h2027757047; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; cted=modId%3Dhtlowve6%3Bclient_id%3D1264916353.1741678184%3Bya_client_id%3D1741678176664168974; _ct_site_id=36409; _ym_isad=2; nxt-city=%7B%22id%22%3A1%2C%22pk%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22name_prep%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B5%22%2C%22url_prefix%22%3A%22%22%2C%22active%22%3Atrue%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%2C%22has_active_office%22%3Atrue%2C%22translate%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%7D; vp_width=2560; user_account_return_url_session=%2F; city_was_suggested=1; domain_sid=pPz3-bLEHe1VOjIhFyQ_1%3A1755673264235; csrftoken=8ZTuBDhOidNWwP3cY1ItnukmYyZeffA8; tmr_detect=0%7C1755673303618; was_called_in_current_session_104054=1; undefined=2955.282; pageviewTimerAll=2955.282; pageviewTimerMSK=2955.282; pageviewTimerHoses=2955.282; pageviewTimerHoses150seconds=1; pageviewTimerHoses300seconds=1; pageviewTimerHoses600seconds=1; pageviewTimerAllFired1min=true; pageviewTimerAllFired2min=true; pageviewTimerAllFired5min=true; pageviewTimerAllFired10min=true; pageviewTimerAllFired15sec=true; pageviewTimerAllFired15min=true; pageviewTimerAllFired45min=true; pageviewTimerAllFired30min=true; pageviewTimerMSKFired1min=true; pageviewTimerMSKFired2min=true; pageviewTimerMSKFired5min=true; pageviewTimerMSKFired10min=true; pageviewTimerMSKFired15min=true; pageviewTimerMSKFired45min=true; qrator_jsr=1755676254.160.OqFg7b6aWeg0lhzE-72flj9rcgck5hu5uo3lu4ijcbjpg8dee-00; seconds_on_page_104054=2981; qrator_jsid=1755676254.160.OqFg7b6aWeg0lhzE-f8einsd6utgq46rmtpf0b0ubt7pkae0c; _ym_visorc=b; _ct_ids=htlowve6%3A36409%3A905520004; _ct_session_id=905520004; call_s=___htlowve6.1755678060.905520004.363119:1024273|2___',
}



params = {
    "project": "69077",
    "ordering": "filter_price,pk",
    "type": "Вилла Британии,Вилла Гардиан,Вилла Дельта,Вилла Дэнфорд,Вилла Нортхил,Вилла Фортрес,XXS,XS,S,M,L,XL,Вилла",
    "offset": "12",
    "limit": "12"
}

projects = ['69299']

session = requests.Session()


parsed_flat_count = 0

for project in projects:

    flats = []
    offset = 0
    params['project'] = project
    params['offset'] = 0
    params['page'] = 1
    print(f"ЖК ID : {project}")

    while True:

        url =  'https://samolet.ru/api_redesign/houses/'
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
            highway = 'Ярославское'
            url = i['url']
            developer = "Самолет"
            kp = i["project"]
            uchastok_area = i['land_area']
            house_area = i['area']
            price = i['filter_price']
            poselok = ''
            property_from = ''

            print(
                f"Шоссе {highway}, {url}, Участок: {uchastok_area}, дом: {house_area}, цена: {price}, посёлок {poselok}, кп: {kp}, объявление {property_from}")
            result = [highway, uchastok_area, house_area, price, poselok, kp, property_from, url]
            flats.append(result)

        if not items:
            print("Всё скачано. Переходим к загрузке в файл")
            break
        # print(f"Выполнено на {round(parsed_flat_count * 100 / total_flat_count, 2)} процентов")

        params['offset'] += 12
        params['page'] += 1

        sleep_time = random.uniform(1, 4)
        time.sleep(sleep_time)


current_date = datetime.now().date()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{kp}-{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Шоссе',
                                  'Размер участка',
                                  'Размер дома',
                                  'Цена',
                                  'Посёлок',
                                  'Коттеджный посёлок',
                                  'Объявление от',
                                  'Ссылка'
                                  ])

# Сохранение файла в папку
df.to_excel(file_path, index=False)




