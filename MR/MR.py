import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel


cookies = {
    'spid': '1741784632987_62d30c366d1e5b195ad803dff541d343_rmtsfh281m20htua',
    '_ym_uid': '1741784635438762062',
    '_ym_d': '1741784635',
    'tmr_lvid': '1c335b6614b3f392afef8213cbdc301d',
    'tmr_lvidTS': '1741784635189',
    '_ga': 'GA1.1.835945232.1741784643',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'scbsid_old': '2746015342',
    'uxs_uid': '7adaf8b0-ff42-11ef-978b-e730cc09ad57',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22d9eadf726ef363c2da5f2fae87307f58%22%5D',
    '_ga_QGFQD68LK3': 'GS2.1.s1751354084$o1$g1$t1751354305$j60$l0$h0',
    'spsc': '1753368967593_08a32317309c697a810ee13249cfa345_YFFv8xBSXhZdrc7.EyCpzzKbTS8-Ytr6EQJsc-pmpj0Z',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'PHPSESSID': '2gdimg1fd29c4ec2sa77er88k4',
    'domain_sid': 'OIbdJw_MXh1IehKOV3pwu%3A1753368970605',
    '_cmg_csstvfLiQ': '1753368971',
    '_comagic_idvfLiQ': '10634091478.14930103773.1753368970',
    'sessionId': '17533689721048969542',
    'tmr_detect': '0%7C1753368972572',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753455373760%2C%22sl%22%3A%7B%22224%22%3A1753368973760%2C%221228%22%3A1753368973760%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753455373760%2C%22sl%22%3A%7B%22224%22%3A1753368973760%2C%221228%22%3A1753368973760%7D%7D',
    'adrdel': '1753368973776',
    'adrdel': '1753368973776',
    'sma_session_id': '2369122860',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1753368974747',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'USE_COOKIE_CONSENT_STATE': '{%22session%22:true%2C%22persistent%22:true%2C%22necessary%22:true%2C%22preferences%22:true%2C%22statistics%22:true%2C%22marketing%22:true%2C%22firstParty%22:true%2C%22thirdParty%22:true}',
    'SCBindexAct': '1462',
    '_ga_H5S7YBLWM3': 'GS2.1.s17533689721048969542$o25$g1$t1753368993$j41$l0$h0',
    '_ga_70ZZHDSCR6': 'GS2.1.s1753368971$o25$g1$t1753368993$j38$l0$h0',
    'sma_index_activity': '2262',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': '',
    'baggage': 'sentry-environment=production,sentry-public_key=64d42d1ec99f4044ff0df570a905dbca,sentry-trace_id=a7a2b4f69cae4d899631d00b58e3a5e0,sentry-sample_rate=0.1,sentry-transaction=%2Fflats%2F*,sentry-sampled=false',
    'priority': 'u=1, i',
    'referer': 'https://www.mr-group.ru/flats/mys/page-2/?grid=card',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a7a2b4f69cae4d899631d00b58e3a5e0-8872997279f74bc3-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741784632987_62d30c366d1e5b195ad803dff541d343_rmtsfh281m20htua; _ym_uid=1741784635438762062; _ym_d=1741784635; tmr_lvid=1c335b6614b3f392afef8213cbdc301d; tmr_lvidTS=1741784635189; _ga=GA1.1.835945232.1741784643; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; scbsid_old=2746015342; uxs_uid=7adaf8b0-ff42-11ef-978b-e730cc09ad57; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%2C%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22d9eadf726ef363c2da5f2fae87307f58%22%5D; _ga_QGFQD68LK3=GS2.1.s1751354084$o1$g1$t1751354305$j60$l0$h0; spsc=1753368967593_08a32317309c697a810ee13249cfa345_YFFv8xBSXhZdrc7.EyCpzzKbTS8-Ytr6EQJsc-pmpj0Z; _ym_isad=2; _ym_visorc=w; PHPSESSID=2gdimg1fd29c4ec2sa77er88k4; domain_sid=OIbdJw_MXh1IehKOV3pwu%3A1753368970605; _cmg_csstvfLiQ=1753368971; _comagic_idvfLiQ=10634091478.14930103773.1753368970; sessionId=17533689721048969542; tmr_detect=0%7C1753368972572; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753455373760%2C%22sl%22%3A%7B%22224%22%3A1753368973760%2C%221228%22%3A1753368973760%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1753455373760%2C%22sl%22%3A%7B%22224%22%3A1753368973760%2C%221228%22%3A1753368973760%7D%7D; adrdel=1753368973776; adrdel=1753368973776; sma_session_id=2369122860; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; SCBstart=1753368974747; SCBporogAct=5000; sma_postview_ready=1; USE_COOKIE_CONSENT_STATE={%22session%22:true%2C%22persistent%22:true%2C%22necessary%22:true%2C%22preferences%22:true%2C%22statistics%22:true%2C%22marketing%22:true%2C%22firstParty%22:true%2C%22thirdParty%22:true}; SCBindexAct=1462; _ga_H5S7YBLWM3=GS2.1.s17533689721048969542$o25$g1$t1753368993$j41$l0$h0; _ga_70ZZHDSCR6=GS2.1.s1753368971$o25$g1$t1753368993$j38$l0$h0; sma_index_activity=2262',
}



params = {
    'category': 'flats',
    'page': '1',
    'limit': '1000',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    try:
        response = requests.get('https://www.mr-group.ru/api/sale/products', params=params, cookies=cookies, headers=headers)
    except:
        break
    try:
        items = response.json()["items"]
    except:
        break

    for i in items:

        if i['status']['code'] == 'booked':
            continue

        url = ""

        date = datetime.date.today()
        project = i["project"]["name"]
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
        developer = "MR"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["building"]["name"].replace('Корпус ', '')
        if korpus == 'Janssen':
            korpus = 'Jansson'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['subtype']['name'] == 'Апартаменты':
            type = 'Апартаменты'
        else:
            type = 'Квартиры'
        if i["decoration"]["name"] == "MR Base":
            finish_type = "Предчистовая"
        elif i["decoration"]["name"] == "MR Ready":
            finish_type = "С отделкой"
        else:
            finish_type = i["decoration"]["name"]

        room_count = int(i["rooms_number"])
        area = i["area"]
        price_per_metr = ''
        old_price = ""
        discount = ''
        price_per_metr_new = ''
        if not i['discount']:
            price = ''
            old_price = i["price"]
        else:
            price = i['discount']['price']
            old_price = i["price"]
        section = ''
        floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break
    print(len(flats))
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(7, 11)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)

