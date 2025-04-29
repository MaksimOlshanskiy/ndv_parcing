# требуется менять cookie, а именно 'qrator_jsid'. Запросы через сессию

# id всех проектов: [68195,7,20,69054,5,57,69104,44,68189,56,41,69057,69011,68192,68188,68191,69106,69108,68199,69206,2,45,40,69103,21,68196,31,69101,68194,3,69051,55,1,49,68185,69102,4,42,69100,69110]

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

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
    'pageviewUrlProjectEgorovoPark': 'true',
    'pageviewUrlProjectKvartalIvakino': 'true',
    'pageviewUrlProjectLyubercy': 'true',
    'pageviewUrlProjectMolzhaninovo': 'true',
    'pageviewUrlProjectMytischiPark': 'true',
    'cted': 'modId%3Dhtlowve6%3Bclient_id%3D1264916353.1741678184%3Bya_client_id%3D1741678176664168974',
    '_ym_isad': '2',
    '_ct_site_id': '36409',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'nxt-city': '%7B%22dep%22%3A%7B%22version%22%3A1%2C%22sc%22%3A0%7D%2C%22__v_isRef%22%3Atrue%2C%22__v_isShallow%22%3Afalse%2C%22_rawValue%22%3A%7B%22id%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D%2C%22_value%22%3A%7B%22id%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D%7D',
    'city_approved_url_prefix': '',
    'FPLC': '09m86SYTf5A7I09S2JXrF6CB4cS698jYVJuArBzVT%2BZWnP33yhmcdSTDpxhl2ceZHM2F5%2Fz%2FdDoYhUPpGMD9r6XwqeRUSb3%2FUdygRFxG0Av%2Bw8Nnk%2BgcER8twaIaAA%3D%3D',
    'domain_sid': 'pPz3-bLEHe1VOjIhFyQ_1%3A1743495608643',
    'tmr_detect': '0%7C1743497023475',
    'undefined': '3013.719',
    'pageviewTimerAll': '3013.719',
    'pageviewTimerMSK': '3013.719',
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
    '_ga_2WZB3B8QT0': 'GS1.1.1743500034.7.0.1743500034.0.0.1783200163',
    'qrator_jsr': '1743500035.340.lNzjMVYgUD6MhaVz-aigst9790a8lhculpspa1jnd2uv1nh48-00',
    'qrator_jsid': '1745310134.185.3tUZd7o4WlIotIQE-v6gp9sv76jgk0e59dkjaccj6h18u9qgh',
    '_ym_visorc': 'b',
    'csrftoken': 'cOTUE7JTGH5SVWNuymPfqC9iEzS9J3wXA52jhzTdYUMAhX2ePnvwS2HZx1XYHnRz',
    '_ct_ids': 'htlowve6%3A36409%3A842352338',
    '_ct_session_id': '842352338',
    'call_s': '___htlowve6.1743501837.842352338.143945:445562|2___',
}



headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=PROD,sentry-release=release-fast-track-250310,sentry-public_key=6f0fe185684eda71da9741fe58c43591,sentry-trace_id=dcd59396c8234adf87a7dabc61061167,sentry-sample_rate=0.1,sentry-transaction=flats,sentry-sampled=false',
    'priority': 'u=1, i',
    'referer': 'https://samolet.ru/flats/?project=5&free=1&from=project',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'dcd59396c8234adf87a7dabc61061167-a563fa3af621171d-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_smt=81d8713e-8dd9-4eb9-92d1-6eddb373e658; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ct_ids=htlowve6%3A36409%3A831980740; _ct_session_id=831980740; _ct_site_id=36409; _ct=1300000000514654067; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ymab_param=8XRBcNsyXKtIDbacrAc2BACgO21rCm8Ag3D9zrGpvAndIxB0P18Yxc_5KjOr3ip1jyUFVoI_vSab5fXPK7ntewsKWyM; suggested_city=1; sessionid=niscdnumbzz5ymwbd7rmpyq7ebjbcarg; _ym_uid=1741678176664168974; _ym_d=1741678176; _ym_isad=2; _ym_visorc=b; _ga=GA1.1.1264916353.1741678184; FPID=FPID2.2.CDdF7rEkFIS%2FekBLl3jtW7K80kFov3hiqvjbDmcAEcw%3D.1741678184; FPLC=FoOEkf8%2F0WCKP6j5LQsl2x8AU5S0S8sZ2h%2BBIAfkqFPt54OWbmFIwaCGSY8lusIVo86YDf%2FVnY%2Bo%2Fu0p7Ryll6gcgRA9YteMlhOhyHCbwdccs2iqKmskPhI9AiPn9g%3D%3D; tmr_lvid=609b80c61abf0ce366c33bbd78503b61; tmr_lvidTS=1741678183827; cted=modId%3Dhtlowve6%3Bya_client_id%3D1741678176664168974%3Bclient_id%3D1264916353.1741678184; domain_sid=pPz3-bLEHe1VOjIhFyQ_1%3A1741678185598; nxt-city=%7B%22dep%22%3A%7B%22version%22%3A1%2C%22sc%22%3A0%7D%2C%22__v_isRef%22%3Atrue%2C%22__v_isShallow%22%3Afalse%2C%22_rawValue%22%3A%7B%22id%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D%2C%22_value%22%3A%7B%22id%22%3A1%2C%22key%22%3A%22moscow%22%2C%22name%22%3A%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22url_prefix%22%3A%22%22%2C%22contact_number%22%3A%22%2B7%20495%20292-31-31%22%7D%7D; cookies_accepted=1; pageviewTimerAllFired5min=true; pageviewTimerAllFired10min=true; pageviewTimerAllFired15min=true; pageviewTimerAllFired45min=true; pageviewTimerAllFired30min=true; pageviewTimerMSKFired5min=true; pageviewTimerMSKFired10min=true; pageviewTimerMSKFired15min=true; pageviewTimerMSKFired45min=true; pageviewCountMSKFired9pages=true; undefined=8419.6; pageviewTimerAll=12242.995; pageviewTimerMSK=12242.995; pageviewTimerAllFired1min=true; pageviewTimerAllFired2min=true; pageviewTimerAllFired15sec=true; pageviewTimerMSKFired1min=true; pageviewTimerMSKFired2min=true; qrator_jsid=1741685054.002.Zd4H2dQq7hWf3BKE-fd64o4rfkk7q39ll3sqthu3rlgojgo2o; pageviewCountMSKFired10pages=true; call_s=___htlowve6.1741688423.831980740.185717:571622|2___; csrftoken=P0UvLuD5XsszJiZCI9WLFAfXBxnKI2hPToXXZQr6WLwuQ987ESdoHvKzKA99iSnK; pageviewCount=11; pageviewCountMSK=11; _ga_2WZB3B8QT0=GS1.1.1741678183.1.1.1741686629.0.0.272202610; tmr_detect=0%7C1741686631901',
}

params = {
    "nameType": "sale",
    "free": 1,
    "type": 100000000,
    "ordering": "-order_manual,filter_price_package,pk",
    "offset": 0,
    "limit": 12,
    "page": 1,
    "project": 68195
}

projects = [68195,7,20,69054,5,57,69104,44,68189,56,41,69057,69011,68192,68188,68191,69106,69108,68199,69206,2,45,40,69103,21,68196,31,69101,68194,3,69051,55,1,49,68185,69102,4,42,69100,69110]


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
            type = ''
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
                old_price = int(i["old_filter_price_package"])
            except:
                old_price = ''
            try:
                price = int(i["filter_price"])
            except:
                price = ''
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

        sleep_time = random.uniform(1, 4)
        time.sleep(sleep_time)







    if len(flats) >= 10:      #  сохраняем ЖК, где 10 и более квартир в наличии

        df = pd.DataFrame(flats, columns=['Дата обновления',
                                          'Название проекта',
                                          'на англ',
                                          'промзона',
                                          'Местоположение',
                                          'Метро',
                                          'Расстояние до метро, км',
                                          'Время до метро, мин',
                                          'МЦК/МЦД/БКЛ',
                                          'Расстояние до МЦК/МЦД, км',
                                          'Время до МЦК/МЦД, мин',
                                          'БКЛ',
                                          'Расстояние до БКЛ, км',
                                          'Время до БКЛ, мин',
                                          'статус',
                                          'старт',
                                          'Комментарий',
                                          'Девелопер',
                                          'Округ',
                                          'Район',
                                          'Адрес',
                                          'Эскроу',
                                          'Корпус',
                                          'Конструктив',
                                          'Класс',
                                          'Срок сдачи',
                                          'Старый срок сдачи',
                                          'Стадия строительной готовности',
                                          'Договор',
                                          'Тип помещения',
                                          'Отделка',
                                          'Кол-во комнат',
                                          'Площадь, кв.м',
                                          'Цена кв.м, руб.',
                                          'Цена лота, руб.',
                                          'Скидка,%',
                                          'Цена кв.м со ск, руб.',
                                          'Цена лота со ск, руб.',
                                          'секция',
                                          'этаж',
                                          'номер'])

        current_date = datetime.now().date()

        # Базовый путь для сохранения
        base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Самолёт"

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = f"{developer}_{project}_{current_date}.xlsx"

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        df.to_excel(file_path, index=False)


    else:
        print(f"В ЖК всего {len(flats)} квартир, поэтому не сохраняем в файл")
