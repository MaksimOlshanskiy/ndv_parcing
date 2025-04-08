# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам, например

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

ids = [843911
       ]  # id ЖК для парсинга

proxies = {
    'https': '47.95.203.57:8080'
}

cookies = {
    '_CIAN_GK': '787699e3-fc12-4a31-a77a-6cfd610b499c',
    '_gcl_au': '1.1.1422723987.1740731465',
    'tmr_lvid': 'b47c6c39b48ce8d68592cfa9ff9beaf0',
    'tmr_lvidTS': '1740731465513',
    '_ga': 'GA1.1.582149124.1740731467',
    '_ym_uid': '1740731467185025844',
    '_ym_d': '1740731467',
    'uxfb_usertype': 'searcher',
    'uxs_uid': '5b193cf0-f5ae-11ef-8867-1b8844357aae',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'afUserId': 'be3c106f-b0b6-4cef-af07-257ce88c47d3-p',
    'login_button_tooltip_key': '1',
    'cookie_agreement_accepted': '1',
    '__zzatw-cian': 'MDA0dBA=Fz2+aQ==',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'login_mro_popup': '1',
    'AF_SYNC': '1741934640332',
    'uxfb_card_satisfaction': '%5B314449567%2C314109440%2C304829381%2C308541124%2C313898469%5D',
    'session_region_id': '4584',
    'session_main_town_region_id': '4820',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742068546693%2C%22sl%22%3A%7B%22224%22%3A1741982146693%2C%221228%22%3A1741982146693%7D%7D',
    'cf_clearance': '9bFfKFzrTyhJoXh6aUwmAUOw7.BpxIzlXSVpaOItWN8-1742045497-1.2.1.1-KPUokSd_FdfMVYehorc1zC2Quny6JE2i8yrzcZ01XILzjkP7zxqgscaMzMKBg4CuFeRhC97Bv87CgJRcVM2tYAILfmFG0rKUqsSm6QiquIjpes0g7s64Gw9AcWqKjNrofZ61T6Q300fL.dSxfRredQ55XAjzhsSsfVI4do_RJ6krlopy9BFfj1yfRBzXHYEBkbZi3uYeJjTKAc45DoW19.npfYLQeKT1xwCH6Ggy6Gz_p2V1Mnr_X9pb0L8vTvi3K2sWC3ioMZMl6yn_qKZ5hP.2MuXPEqPt_MYIBj2ovOvQzeabrtARIcHxaESCyv.AEg9nB9Wyv6FeDAuAVXNCpXl0qEIDDK_ornkhkkxLyFo',
    'countCallNowPopupShowed': '1%3A1742045479686',
    'sopr_session': '84b470aec35341e6',
    'adrdel': '1742045514747',
    '_ym_visorc': 'b',
    '_ym_isad': '1',
    '__cf_bm': 'ePtk5p8wMH3.xlQDOOiuz5wZaPNU7A1zwvjnCkoNHV0-1742045698-1.0.1.1-dxq.c.moLRQKtPve.MgKmqOenHlr9ek_ABNjKvJvQx3pd5l3tn4.N52Z8LHlvVNlw6v3qvBGoEt8_6Vw_y.Is_dZVXmPBR7mvjqXUzrN34g',
    '_ga_3369S417EL': 'GS1.1.1742045476.23.1.1742045996.15.0.0',
    'cfidsw-cian': 'AxdMvlRRvR6My2+fKjo4YJdkzCoF/jlq91PsPICw1gb/lQoINg65e35zgs3rWzmh2HHtC2h8oQGhyYkaGNzM90nGR60NqOhPs2Bve5PCL6Z7YKfyZwxq/LC162B50yseaP2lR8ETH+7tgalQtQ+SVZ/4D6qFYMITcwYMzoQ=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://krasnodar.cian.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://krasnodar.cian.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=787699e3-fc12-4a31-a77a-6cfd610b499c; _gcl_au=1.1.1422723987.1740731465; tmr_lvid=b47c6c39b48ce8d68592cfa9ff9beaf0; tmr_lvidTS=1740731465513; _ga=GA1.1.582149124.1740731467; _ym_uid=1740731467185025844; _ym_d=1740731467; uxfb_usertype=searcher; uxs_uid=5b193cf0-f5ae-11ef-8867-1b8844357aae; adrcid=A0r9KB4fc8duMUv2jPsp-tg; afUserId=be3c106f-b0b6-4cef-af07-257ce88c47d3-p; login_button_tooltip_key=1; cookie_agreement_accepted=1; __zzatw-cian=MDA0dBA=Fz2+aQ==; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; login_mro_popup=1; AF_SYNC=1741934640332; uxfb_card_satisfaction=%5B314449567%2C314109440%2C304829381%2C308541124%2C313898469%5D; session_region_id=4584; session_main_town_region_id=4820; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742068546693%2C%22sl%22%3A%7B%22224%22%3A1741982146693%2C%221228%22%3A1741982146693%7D%7D; cf_clearance=9bFfKFzrTyhJoXh6aUwmAUOw7.BpxIzlXSVpaOItWN8-1742045497-1.2.1.1-KPUokSd_FdfMVYehorc1zC2Quny6JE2i8yrzcZ01XILzjkP7zxqgscaMzMKBg4CuFeRhC97Bv87CgJRcVM2tYAILfmFG0rKUqsSm6QiquIjpes0g7s64Gw9AcWqKjNrofZ61T6Q300fL.dSxfRredQ55XAjzhsSsfVI4do_RJ6krlopy9BFfj1yfRBzXHYEBkbZi3uYeJjTKAc45DoW19.npfYLQeKT1xwCH6Ggy6Gz_p2V1Mnr_X9pb0L8vTvi3K2sWC3ioMZMl6yn_qKZ5hP.2MuXPEqPt_MYIBj2ovOvQzeabrtARIcHxaESCyv.AEg9nB9Wyv6FeDAuAVXNCpXl0qEIDDK_ornkhkkxLyFo; countCallNowPopupShowed=1%3A1742045479686; sopr_session=84b470aec35341e6; adrdel=1742045514747; _ym_visorc=b; _ym_isad=1; __cf_bm=ePtk5p8wMH3.xlQDOOiuz5wZaPNU7A1zwvjnCkoNHV0-1742045698-1.0.1.1-dxq.c.moLRQKtPve.MgKmqOenHlr9ek_ABNjKvJvQx3pd5l3tn4.N52Z8LHlvVNlw6v3qvBGoEt8_6Vw_y.Is_dZVXmPBR7mvjqXUzrN34g; _ga_3369S417EL=GS1.1.1742045476.23.1.1742045996.15.0.0; cfidsw-cian=AxdMvlRRvR6My2+fKjo4YJdkzCoF/jlq91PsPICw1gb/lQoINg65e35zgs3rWzmh2HHtC2h8oQGhyYkaGNzM90nGR60NqOhPs2Bve5PCL6Z7YKfyZwxq/LC162B50yseaP2lR8ETH+7tgalQtQ+SVZ/4D6qFYMITcwYMzoQ=',
}

json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'newobject',
                    'id': 4825183,
                },
            ],
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
}



def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

current_date = datetime.date.today()


for y in ids:

    session = requests.Session()

    flats = []
    counter = 1
    total_count = 1
    json_data["jsonQuery"]["page"]["value"] = 1

    print("Новый ЖК", y)

    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y

    while len(flats) < total_count:

        if counter > 1:
            sleep_time = random.uniform(30, 45)
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
                if i['building']['deadline']['isComplete'] == True:
                    srok_sdachi = "Дом сдан"
                elif i['building']['deadline']['quarterEnd'] is None:
                    srok_sdachi = ''
                else:
                    srok_sdachi = f"Cдача ГК: {i['building']['deadline']['quarterEnd']}"
            except:
                srok_sdachi = ''
            try:
                url = i['fullUrl']
            except:
                url = ''

            try:
                if i['isApartments'] == True:
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
                project = i['geo']['jk']['displayName']
            except:
                project = ''
            try:
                if i['decoration'] == "fine":
                    finish_type = "С отделкой"
                elif i['decoration'] == "without" or i['decoration'] == "rough":
                    finish_type = "Без отделки"
                else:
                    finish_type = i['decoration']
            except:
                finish_type = ''

            #try:
            #    decoration2 = i['offerFeatureLabels'][0]
            #except:
            #    decoration2 = ''
            try:
                adress = i['geo']['userInput']
            except:
                adress = ""

            try:
                korpus = extract_digits_or_original(i["geo"]["jk"]["house"]["name"])
            except:
                korpus = ''

            try:
                developer = i['geo']['jk']['developer']['name']
            except:
                developer = ""

            try:
                if i["roomsCount"] == None:
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

            eskrou = ''
            konstruktiv = ''
            klass = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            old_price = ''
            discount = ''
            price_per_metr = ''
            price_per_metr_new = ''

            section = ''
            flat_number = ''


            print(
                f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck, distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        json_data["jsonQuery"]["page"]["value"] += 1
        print("-----------------------------------------------------------------------------")
        total_count = response.json()["data"]["offerCount"]
        downloaded = len(flats)
        print(f'ID ЖК: {y}. Загружено {downloaded} предложений из {total_count}')
        counter += 1

    counter += 1

    # Базовый путь для сохранения
    base_path = r"C:\PycharmProjects\SeleniumParcer\Cian"

    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    project = project.replace("/", "-")

    filename = f"{project}_{current_date}.xlsx"

    # Полный путь к файлу
    file_path = os.path.join(folder_path, filename)

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

    current_date = datetime.date.today()

    # Базовый путь для сохранения
    base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian"

    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{project}_{current_date}.xlsx"

    # Полный путь к файлу
    file_path = os.path.join(folder_path, filename)

    # Сохранение файла в папку
    df.to_excel(file_path, index=False)


def classify_renovation():
    return None