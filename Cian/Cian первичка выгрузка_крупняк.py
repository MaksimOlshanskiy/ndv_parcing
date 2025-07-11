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
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'polygon',
                    'name': 'Область поиска',
                    'coordinates': [
                        [
                            '20.3571312',
                            '54.7479954',
                        ],
                        [
                            '20.3543846',
                            '54.7273584',
                        ],
                        [
                            '20.3557579',
                            '54.7067214',
                        ],
                        [
                            '20.3598778',
                            '54.6876718',
                        ],
                        [
                            '20.3406517',
                            '54.6710035',
                        ],
                        [
                            '20.309066',
                            '54.6646536',
                        ],
                        [
                            '20.2774803',
                            '54.6590975',
                        ],
                        [
                            '20.2445213',
                            '54.6567163',
                        ],
                        [
                            '20.2033226',
                            '54.6527477',
                        ],
                        [
                            '20.1703636',
                            '54.6471915',
                        ],
                        [
                            '20.1360313',
                            '54.6440166',
                        ],
                        [
                            '20.0989525',
                            '54.6392542',
                        ],
                        [
                            '20.0632469',
                            '54.6392542',
                        ],
                        [
                            '20.0302879',
                            '54.6360793',
                        ],
                        [
                            '19.997329',
                            '54.6297295',
                        ],
                        [
                            '19.9616234',
                            '54.6233796',
                        ],
                        [
                            '19.9286644',
                            '54.6186172',
                        ],
                        [
                            '19.8970787',
                            '54.6130611',
                        ],
                        [
                            '19.8627464',
                            '54.6114736',
                        ],
                        [
                            '19.832534',
                            '54.6194109',
                        ],
                        [
                            '19.8215477',
                            '54.6376668',
                        ],
                        [
                            '19.8297875',
                            '54.6590975',
                        ],
                        [
                            '19.8490135',
                            '54.6757659',
                        ],
                        [
                            '19.8696129',
                            '54.6948154',
                        ],
                        [
                            '19.8833458',
                            '54.7162462',
                        ],
                        [
                            '19.8929588',
                            '54.7400581',
                        ],
                        [
                            '19.9011986',
                            '54.7630763',
                        ],
                        [
                            '19.9053185',
                            '54.7845071',
                        ],
                        [
                            '19.9066917',
                            '54.8043504',
                        ],
                        [
                            '19.9066917',
                            '54.828956',
                        ],
                        [
                            '19.9053185',
                            '54.8535617',
                        ],
                        [
                            '19.898452',
                            '54.8741987',
                        ],
                        [
                            '19.8902123',
                            '54.8964232',
                        ],
                        [
                            '19.8860924',
                            '54.9162665',
                        ],
                        [
                            '19.8902123',
                            '54.9376973',
                        ],
                        [
                            '19.9039452',
                            '54.9551593',
                        ],
                        [
                            '19.9245445',
                            '54.9726214',
                        ],
                        [
                            '19.9575035',
                            '54.9845274',
                        ],
                        [
                            '19.997329',
                            '54.9924647',
                        ],
                        [
                            '20.0371544',
                            '54.9948459',
                        ],
                        [
                            '20.0742333',
                            '54.9948459',
                        ],
                        [
                            '20.115432',
                            '54.9948459',
                        ],
                        [
                            '20.1634972',
                            '54.9932585',
                        ],
                        [
                            '20.2033226',
                            '54.9892898',
                        ],
                        [
                            '20.2486412',
                            '54.9853211',
                        ],
                        [
                            '20.309066',
                            '54.9805587',
                        ],
                        [
                            '20.3433983',
                            '54.9773838',
                        ],
                        [
                            '20.3873436',
                            '54.9750026',
                        ],
                        [
                            '20.4340355',
                            '54.9742089',
                        ],
                        [
                            '20.4752342',
                            '54.9750026',
                        ],
                        [
                            '20.5191795',
                            '54.979765',
                        ],
                        [
                            '20.5521385',
                            '54.9813525',
                        ],
                        [
                            '20.6098167',
                            '54.9837337',
                        ],
                        [
                            '20.6523888',
                            '54.9829399',
                        ],
                        [
                            '20.6977074',
                            '54.9781776',
                        ],
                        [
                            '20.7375328',
                            '54.9757964',
                        ],
                        [
                            '20.785598',
                            '54.9742089',
                        ],
                        [
                            '20.8254234',
                            '54.9694465',
                        ],
                        [
                            '20.8721153',
                            '54.9638904',
                        ],
                        [
                            '20.9050743',
                            '54.959128',
                        ],
                        [
                            '20.9448998',
                            '54.9511907',
                        ],
                        [
                            '20.9847252',
                            '54.9448408',
                        ],
                        [
                            '21.0163109',
                            '54.938491',
                        ],
                        [
                            '21.0163109',
                            '54.9186477',
                        ],
                        [
                            '20.9929649',
                            '54.9043605',
                        ],
                        [
                            '20.9627525',
                            '54.8932483',
                        ],
                        [
                            '20.9284203',
                            '54.8861047',
                        ],
                        [
                            '20.8913414',
                            '54.8837235',
                        ],
                        [
                            '20.851516',
                            '54.8797549',
                        ],
                        [
                            '20.8130638',
                            '54.8797549',
                        ],
                        [
                            '20.7746117',
                            '54.8797549',
                        ],
                        [
                            '20.7279198',
                            '54.8861047',
                        ],
                        [
                            '20.6812279',
                            '54.8908671',
                        ],
                        [
                            '20.6400292',
                            '54.8956295',
                        ],
                        [
                            '20.601577',
                            '54.8995981',
                        ],
                        [
                            '20.5672447',
                            '54.9051543',
                        ],
                        [
                            '20.5301659',
                            '54.9099167',
                        ],
                        [
                            '20.4944603',
                            '54.9130916',
                        ],
                        [
                            '20.4615013',
                            '54.9154728',
                        ],
                        [
                            '20.4230492',
                            '54.9162665',
                        ],
                        [
                            '20.3859703',
                            '54.9162665',
                        ],
                        [
                            '20.3461449',
                            '54.917854',
                        ],
                        [
                            '20.3131859',
                            '54.9170602',
                        ],
                        [
                            '20.2747337',
                            '54.9154728',
                        ],
                        [
                            '20.2390282',
                            '54.9154728',
                        ],
                        [
                            '20.200576',
                            '54.9130916',
                        ],
                        [
                            '20.1648705',
                            '54.9115041',
                        ],
                        [
                            '20.1277916',
                            '54.9075355',
                        ],
                        [
                            '20.0934593',
                            '54.9027731',
                        ],
                        [
                            '20.0577538',
                            '54.8980107',
                        ],
                        [
                            '20.0344078',
                            '54.8845172',
                        ],
                        [
                            '20.0247948',
                            '54.8654677',
                        ],
                        [
                            '20.0124352',
                            '54.8464181',
                        ],
                        [
                            '20.0096886',
                            '54.8273686',
                        ],
                        [
                            '20.0083153',
                            '54.8075253',
                        ],
                        [
                            '20.0083153',
                            '54.7868883',
                        ],
                        [
                            '20.0151817',
                            '54.7678387',
                        ],
                        [
                            '20.0412743',
                            '54.7511704',
                        ],
                        [
                            '20.0742333',
                            '54.7440268',
                        ],
                        [
                            '20.1085655',
                            '54.7384707',
                        ],
                        [
                            '20.1428978',
                            '54.7360895',
                        ],
                        [
                            '20.190963',
                            '54.7352957',
                        ],
                        [
                            '20.2417748',
                            '54.7337083',
                        ],
                        [
                            '20.2870934',
                            '54.7392644',
                        ],
                        [
                            '20.3200523',
                            '54.7416456',
                        ],
                        [
                            '20.3530113',
                            '54.746408',
                        ],
                        [
                            '20.3571312',
                            '54.7479954',
                        ],
                    ],
                },
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

rooms_ids = [1,2,3,4,5,6,7,9]
total_floor_list = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 11], [12, 14], [15, 20], [21, 200]]

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
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'newobject',
                    'id': 4013017,
                },
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 99,
            },
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
    flats_total = []

    if y in []:
        continue

    print(f"Новый ЖК, {y}, {ids.index(y) + 1} из {len(ids)}")

    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y
    time.sleep(10)

    for room_id in rooms_ids:

        session = requests.Session()

        for f in total_floor_list:

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

