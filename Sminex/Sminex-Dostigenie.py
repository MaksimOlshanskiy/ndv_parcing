import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'io3mmODLNoyPf87SPJBOIq4w77kgO5I0',
    '_gcl_au': '1.1.1120234242.1741861319',
    'scbsid_old': '2746015342',
    'tmr_lvid': '8f0e44119f15b36924f914c8b83e7ded',
    'tmr_lvidTS': '1741861319713',
    '_gid': 'GA1.2.707252605.1741861320',
    '_ym_uid': '1741861320350429111',
    '_ym_d': '1741861320',
    '_ym_isad': '2',
    '_cmg_csstcg_xR': '1741861321',
    '_comagic_idcg_xR': '9977411768.14167363353.1741861320',
    'domain_sid': 'iZjhkvY0APz4f3UGa0YFg%3A1741861321776',
    'sma_session_id': '2221825661',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    '_ga_session_id': '13032025.01785565',
    '_pageCount': '3',
    '_ga_LB22FX8W2T': 'GS1.2.1741861320.1.1.1741862935.60.0.0',
    'tmr_detect': '0%7C1741862938707',
    '_ga': 'GA1.2.2115005366.1741861319',
    'SCBporogAct': '5000',
    '_dc_gtm_UA-81340848-20': '1',
    'sma_index_activity': '1501',
    'SCBindexAct': '4172',
    '_ga_FMTVD1KRZ2': 'GS1.1.1741865446.2.0.1741865446.60.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://dom-dostigenie.ru/katalog-kvartir/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=io3mmODLNoyPf87SPJBOIq4w77kgO5I0; _gcl_au=1.1.1120234242.1741861319; scbsid_old=2746015342; tmr_lvid=8f0e44119f15b36924f914c8b83e7ded; tmr_lvidTS=1741861319713; _gid=GA1.2.707252605.1741861320; _ym_uid=1741861320350429111; _ym_d=1741861320; _ym_isad=2; _cmg_csstcg_xR=1741861321; _comagic_idcg_xR=9977411768.14167363353.1741861320; domain_sid=iZjhkvY0APz4f3UGa0YFg%3A1741861321776; sma_session_id=2221825661; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; _ga_session_id=13032025.01785565; _pageCount=3; _ga_LB22FX8W2T=GS1.2.1741861320.1.1.1741862935.60.0.0; tmr_detect=0%7C1741862938707; _ga=GA1.2.2115005366.1741861319; SCBporogAct=5000; _dc_gtm_UA-81340848-20=1; sma_index_activity=1501; SCBindexAct=4172; _ga_FMTVD1KRZ2=GS1.1.1741865446.2.0.1741865446.60.0.0',
}

params = { 'page': 1
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://dom-dostigenie.ru/ajax/flats/index.php?filter=%7B%22price%22:[0,0],%22sq%22:[0,0],%22price_sqm%22:[0,0],%22price_mlnusd%22:[0,0],%22price_mlneur%22:[0,0],%22price_sqmusd%22:[0,0],%22price_sqmeur%22:[0,0],%22project%22:[],%22stage%22:[],%22rooms%22:[],%22floor%22:[],%22ids%22:[],%22typeofsize%22:[],%22type%22:[],%22typeofkitchen%22:[],%22views%22:[],%22worldsides%22:[],%22section%22:[],%22advantages%22:[],%22penthouse%22:[],%22plantype%22:[],%22balcony%22:[],%22flat%22:%22%22,%22hide_reserved%22:[%22Y%22]%7D&sort=%7B%22sq%22:1%7D&cnt=30&trigger=',
        cookies=cookies,
        headers=headers,
        params=params
    )

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
        flat_number = int(i['num'])

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