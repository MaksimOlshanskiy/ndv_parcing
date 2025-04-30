# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'DMIR_AUTH': '6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744095038128%2C%22sl%22%3A%7B%22224%22%3A1744008638128%2C%221228%22%3A1744008638128%7D%7D',
    '_yasc': 'QG4aPQs+5Fze4KmEjttcFE3EtmDAdt73mR3RN89Q5nU15dTfMQ1AYAnVGj/cPRzX9IU=',
    '_yasc': 'fKvML3PgmyiDQnB5q4cqA2Uk3/gQzlZKpKasfXTV1IghUVHOdEbwCc2GNi9raBchUKw=',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'adrdel': '1744094487237',
    'F6_CIAN_SID': 'e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956',
    'F6_CIAN_UID': '8098251',
    'session_region_id': '4619',
    'session_main_town_region_id': '176083',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCkdEQhvKE8PFFtDPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVhUPT1dPXZyc1tBISViTGBUdlxVMiseFngoKVUJPmBCdHQuLTxnHWJ9XyV1D1N6WyAZM3EqDAg+Y0ZCcHoyQGsPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomR1lNCikeEX90I1d7dScOCSplMy0tWRgIH2N4JRlrcmY=qOrDWA==',
    '_gcl_au': '1.1.150541652.1744094509',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'sopr_utm': '%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D',
    'sopr_session': '24dfe084219d480f',
    'cookieUserID': '8098251',
    '_ga': 'GA1.1.2141111618.1744094510',
    'uxfb_usertype': 'searcher',
    'afUserId': '01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p',
    'AF_SYNC': '1744094510966',
    'cian_ruid': '8098251',
    '_ga_3369S417EL': 'GS1.1.1744094510.1.1.1744094538.32.0.0',
    'cfidsw-cian': 'H1vjqn5vmj+YGg5Xm86d7UR8gnDIoCNFY8gdrCFcTqtHKZYUgdtgp9iKpXdSSbGFVM3wIOb0e7OaMH1QrB3vP/D7z3Lo7OVWAPrjxgKydnUn4xnnv+F/ykNQmUGqLP3wFn3hu6LKswrIKqeD9Q72FwQBVpK60oRaOJC1yJU=',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://tver.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://tver.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; DMIR_AUTH=6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744095038128%2C%22sl%22%3A%7B%22224%22%3A1744008638128%2C%221228%22%3A1744008638128%7D%7D; _yasc=QG4aPQs+5Fze4KmEjttcFE3EtmDAdt73mR3RN89Q5nU15dTfMQ1AYAnVGj/cPRzX9IU=; _yasc=fKvML3PgmyiDQnB5q4cqA2Uk3/gQzlZKpKasfXTV1IghUVHOdEbwCc2GNi9raBchUKw=; _ym_isad=2; _ym_visorc=b; adrdel=1744094487237; F6_CIAN_SID=e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956; F6_CIAN_UID=8098251; session_region_id=4619; session_main_town_region_id=176083; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCkdEQhvKE8PFFtDPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVhUPT1dPXZyc1tBISViTGBUdlxVMiseFngoKVUJPmBCdHQuLTxnHWJ9XyV1D1N6WyAZM3EqDAg+Y0ZCcHoyQGsPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomR1lNCikeEX90I1d7dScOCSplMy0tWRgIH2N4JRlrcmY=qOrDWA==; _gcl_au=1.1.150541652.1744094509; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; sopr_utm=%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D; sopr_session=24dfe084219d480f; cookieUserID=8098251; _ga=GA1.1.2141111618.1744094510; uxfb_usertype=searcher; afUserId=01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p; AF_SYNC=1744094510966; cian_ruid=8098251; _ga_3369S417EL=GS1.1.1744094510.1.1.1744094538.32.0.0; cfidsw-cian=H1vjqn5vmj+YGg5Xm86d7UR8gnDIoCNFY8gdrCFcTqtHKZYUgdtgp9iKpXdSSbGFVM3wIOb0e7OaMH1QrB3vP/D7z3Lo7OVWAPrjxgKydnUn4xnnv+F/ykNQmUGqLP3wFn3hu6LKswrIKqeD9Q72FwQBVpK60oRaOJC1yJU=',
}

json_data = {
    'jsonQuery': {
        'region': {
            'type': 'terms',
            'value': [
                5024,
            ],
        },
    },
    'uri': '/newobjects/list?deal_type=sale&engine_version=2&offer_type=newobject&region=5024&p=2',
    'subdomain': 'tyumen',
    'offset': 0,
    'count': 25,
    'userCanUseHiddenBase': False,
}

ids = []
json_data['offset'] = 0

while True:

    response = requests.post(
        'https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )


    items = response.json()['newbuildings']

    for i in items:
        id = i['id']
        ids.append(id)
    if not items:
        break
    json_data['offset'] += 25

print(response.json()['breadcrumbs'][0]['title'])
print(response.json()['breadcrumbs'][1]['title'])
print(ids)
print(f'Количество ЖК: {len(ids)}'
)


proxies = {
    'https': '47.95.203.57:8080'
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
                    'id': 37206,
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
            sleep_time = random.uniform(10, 15)
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
                elif i['building']['deadline']['quarterEnd'] is None and i['building']['deadline']['year'] is None:
                    srok_sdachi = ''
                else:
                    srok_sdachi = f"Cдача ГК: {i['newbuilding']['house']['finishDate']['quarter']} квартал, {i['newbuilding']['house']['finishDate']['year']} года".replace('None', '')
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
                project = i['geo']['jk']['displayName'].replace('ЖК ', '').replace('«', '').replace('»', '')
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
            if not finish_type:
                finish_type = classify_renovation(i['description'])

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
            try:
                added = i['added']
            except:
                added = ''


            print(
                f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
            result = [date, srok_sdachi, url, project, developer, adress, korpus, type, finish_type, room_count, area, price, floor, added]
            flats.append(result)

        if not items:
            break
        json_data["jsonQuery"]["page"]["value"] += 1
        print("-----------------------------------------------------------------------------")
        total_count = response.json()["data"]["offerCount"]
        downloaded = len(flats)
        print(f'ID ЖК: {y}. Загружено {downloaded} предложений из {total_count}')
        counter += 1

    counter += 1

    if len(flats) > 10:

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
                                          'Срок сдачи',
                                          'Ссылка',
                                          'Название проекта',
                                          'Девелопер',
                                          'Адрес',
                                          'Корпус',
                                          'Тип помещения',
                                          'Отделка',
                                          'Кол-во комнат',
                                          'Площадь, кв.м',
                                          'Цена лота, руб.',
                                          'Этаж',
                                          'Дата объявления'])

        current_date = datetime.date.today()

        # Базовый путь для сохранения
        base_path = r"Cian"

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = f"{project}_{current_date}.xlsx"

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        df.to_excel(file_path, index=False)
