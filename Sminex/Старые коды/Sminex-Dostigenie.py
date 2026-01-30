import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import json

from functions import save_flats_to_excel

filter_params = {
    "price": [0, 0],
    "sq": [0, 0],
    "price_sqm": [0, 0],
    "price_mlnusd": [0, 0],
    "price_mlneur": [0, 0],
    "price_sqmusd": [0, 0],
    "price_sqmeur": [0, 0],
    "project": [],
    "stage": [],
    "rooms": [],
    "floor": [],
    "ids": [],
    "typeofsize": [],
    "type": [],
    "typeofkitchen": [],
    "views": [],
    "worldsides": [],
    "section": [],
    "advantages": [],
    "penthouse": [],
    "plantype": [],
    "balcony": [],
    "flat": "",
    "hide_reserved": ["Y"]
}

sort_params = {
    "sq": 1
}

params = {
    "filter": json.dumps(filter_params, ensure_ascii=False),
    "sort": json.dumps(sort_params),
    "page": 3,
    "cnt": 30,
    "trigger": ""
}

cookies = {
    'PHPSESSID': 'lvS93Ac165jLqic3B9uM74bvBWka6Fog',
    'scbsid_old': '2746015342',
    '_gcl_au': '1.1.1447140527.1769517913',
    '_ga_session_id': '27012026.05207779',
    '_pageCount': '1',
    '_ga_FMTVD1KRZ2': 'GS2.1.s1769517912$o1$g0$t1769517912$j60$l0$h0',
    '_ga': 'GA1.2.1929839925.1769517913',
    '_gid': 'GA1.2.1971847651.1769517913',
    '_dc_gtm_UA-81340848-1': '1',
    '_dc_gtm_UA-81340848-20': '1',
    'tmr_lvid': '8f0e44119f15b36924f914c8b83e7ded',
    'tmr_lvidTS': '1741861319713',
    '_ym_uid': '1741861320350429111',
    '_ym_d': '1769517913',
    '_ym_visorc': 'w',
    '_ga_LB22FX8W2T': 'GS2.2.s1769517913$o1$g0$t1769517913$j60$l0$h0',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769604314514%2C%22sl%22%3A%7B%22224%22%3A1769517914514%2C%221228%22%3A1769517914514%7D%7D',
    '_ym_isad': '2',
    'adrdel': '1769517914733',
    'domain_sid': 'iZjhkvY0APz4f3UGa0YFg%3A1769517915188',
    'sma_session_id': '2580193036',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%5D',
    'SCBnotShow': '-1',
    'tmr_detect': '0%7C1769517916785',
    'SCBstart': '1769517916900',
    'sma_postview_ready': '1',
    'SCBporogAct': '5000',
    'sma_index_activity': '186',
    'SCBindexAct': '186',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://dom-dostigenie.ru/katalog-kvartir/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=lvS93Ac165jLqic3B9uM74bvBWka6Fog; scbsid_old=2746015342; _gcl_au=1.1.1447140527.1769517913; _ga_session_id=27012026.05207779; _pageCount=1; _ga_FMTVD1KRZ2=GS2.1.s1769517912$o1$g0$t1769517912$j60$l0$h0; _ga=GA1.2.1929839925.1769517913; _gid=GA1.2.1971847651.1769517913; _dc_gtm_UA-81340848-1=1; _dc_gtm_UA-81340848-20=1; tmr_lvid=8f0e44119f15b36924f914c8b83e7ded; tmr_lvidTS=1741861319713; _ym_uid=1741861320350429111; _ym_d=1769517913; _ym_visorc=w; _ga_LB22FX8W2T=GS2.2.s1769517913$o1$g0$t1769517913$j60$l0$h0; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769604314514%2C%22sl%22%3A%7B%22224%22%3A1769517914514%2C%221228%22%3A1769517914514%7D%7D; _ym_isad=2; adrdel=1769517914733; domain_sid=iZjhkvY0APz4f3UGa0YFg%3A1769517915188; sma_session_id=2580193036; SCBfrom=; smFpId_old_values=%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%5D; SCBnotShow=-1; tmr_detect=0%7C1769517916785; SCBstart=1769517916900; sma_postview_ready=1; SCBporogAct=5000; sma_index_activity=186; SCBindexAct=186',
}


params = { 'page': 1
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    url = "https://dom-dostigenie.ru/local/ajax/flats/"

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=15
    )
    print(response.status_code)
    items = response.json()["data"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = "Достижение"
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
        developer = "Sminex"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["building"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['type'] == 'Квартира':
            type = 'Квартиры'
        if i["finishing"] == '':
            finish_type = "Без отделки"
        else:
            finish_type = i["finishing"]
        if i["rooms"] == "S":
            room_count = 0
        else:
            room_count = int(i["rooms"])
        area = float(i["sq"])
        price_per_metr = ''
        old_price = int(i["price"].replace(" ", ""))
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = int(i["section"])
        floor = int(i["floor"])
        try:
            flat_number = int(i['num'])
        except:
            flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(2, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)