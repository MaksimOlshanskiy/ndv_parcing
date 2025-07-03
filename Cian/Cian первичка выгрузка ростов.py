# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам

import numpy
import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, clean_filename


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrdel': '1744094487237',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
    '_gcl_au': '1.1.358370826.1745923014',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'newbuilding-search-frontend.consultant_cian_chat_onboarding_shown': '1',
    'cookie_agreement_accepted': '1',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'map_preview_onboarding_counter': '1',
    '_ga': 'GA1.1.781516742.1746453483',
    'uxfb_usertype': 'searcher',
    'afUserId': '01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p',
    'AF_SYNC': '1746453484323',
    'uxs_uid': 'f7e2e9d0-29b8-11f0-9dbd-830a513100bc',
    'cian_ruid': '8098251',
    'F6_CIAN_SID': 'a9a48f63f662387d3c35ca6c6cb20740d7c86bb81f0c2b9767f62a64e8087c55',
    '_ym_isad': '2',
    'login_mro_popup': '1',
    'login_button_tooltip_key': '1',
    'countCallNowPopupShowed': '2%3A1746517081809',
    '_yasc': '8R9/wr218vWJMfK05fBo5KUPxW5J6smlJc3lsbzK7vnwV/2oYgxkWZAv+aGBmHZLlQc=',
    '_yasc': '7EJRUjZIw8befWCH7Q8prRioIBnENtPFjOfuiUI6eC63hgTnMLGHoaCZZVuwd2dtOK4=',
    'sopr_session': 'ee304049ec614f4a',
    '_ym_visorc': 'b',
    'session_region_id': '4827',
    'session_main_town_region_id': '4827',
    '_ga_3369S417EL': 'GS2.1.s1746519290$o4$g1$t1746519322$j28$l0$h0',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://krasnoyarsk.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://krasnoyarsk.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; _gcl_au=1.1.358370826.1745923014; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; map_preview_onboarding_counter=1; _ga=GA1.1.781516742.1746453483; uxfb_usertype=searcher; afUserId=01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p; AF_SYNC=1746453484323; uxs_uid=f7e2e9d0-29b8-11f0-9dbd-830a513100bc; cian_ruid=8098251; F6_CIAN_SID=a9a48f63f662387d3c35ca6c6cb20740d7c86bb81f0c2b9767f62a64e8087c55; _ym_isad=2; login_mro_popup=1; login_button_tooltip_key=1; countCallNowPopupShowed=2%3A1746517081809; _yasc=8R9/wr218vWJMfK05fBo5KUPxW5J6smlJc3lsbzK7vnwV/2oYgxkWZAv+aGBmHZLlQc=; _yasc=7EJRUjZIw8befWCH7Q8prRioIBnENtPFjOfuiUI6eC63hgTnMLGHoaCZZVuwd2dtOK4=; sopr_session=ee304049ec614f4a; _ym_visorc=b; session_region_id=4827; session_main_town_region_id=4827; _ga_3369S417EL=GS2.1.s1746519290$o4$g1$t1746519322$j28$l0$h0',
}

json_data = {
    'jsonQuery': {
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'region': {
            'type': 'terms',
            'value': [
                4959,
            ],
        },
    },
    'uri': '/newobjects/list?deal_type=sale&engine_version=2&from_developer=1&offer_type=newobject&region=2&p=4',
    'subdomain': 'spb',
    'offset': 0,
    'count': 25,
    'userCanUseHiddenBase': False,
}

ids = []
rooms_ids = [    1,
    2,
    3,
    4,
    5,
    6,
    7,
    9,
]
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
        if i['fromDeveloperPropsCount'] < 1:
            continue
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
                    'id': 2,
                },
            ],
        },
        'room': {
            'type': 'terms',
            'value': [
                1
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
ids = [4362585, 4815246, 3877206, 1258683, 50732, 4095940, 8172, 3952382, 4691157, 3260347, 7984, 4800628, 4499896, 900192, 5238228, 4130711, 2038797, 3910227, 5283548, 4441515, 219525, 3923317, 43956, 4019247, 4927010]
for y in ids:

    if y == 4731130:
        continue

    session = requests.Session()
    flats_total = []

    if y in []:
        continue

    print(f"Новый ЖК, {y}, {ids.index(y) + 1} из {len(ids)}")

    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y
    time.sleep(10)

    for room_id in rooms_ids:

        json_data["jsonQuery"]["page"]["value"] = 1
        flats = []
        json_data["jsonQuery"]["room"]["value"][0] = room_id
        counter = 1
        total_count = 1

        while len(flats) < total_count:

            print(f"Число комнат: {room_id}")
            if counter > 1:
                sleep_time = random.uniform(7, 11)
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
                flats_total.append(result)

            if not items:
                break
            json_data["jsonQuery"]["page"]["value"] += 1
            print("-----------------------------------------------------------------------------")
            total_count = response.json()["data"]["offerCount"]
            downloaded = len(flats)
            print(f'ID ЖК: {y}, {ids.index(y)+1} из {len(ids)}. Загружено {downloaded} предложений из {total_count}')
            counter += 1



    if len(flats_total) > 1:



        df = pd.DataFrame(flats_total, columns=['Дата обновления',
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
        base_path = r""

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        def sanitize_filename(name):
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                name = name.replace(char, '_')
            return name

        project = sanitize_filename(project)
        filename = f"{project}__{current_date}.xlsx"

        # Полный путь к файлу0
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        try:
            df.to_excel(file_path, index=False)
        except:
            filename = f"{project}_{current_date}_2.xlsx"
            file_path = os.path.join(folder_path, filename)
            df.to_excel(file_path, index=False)

