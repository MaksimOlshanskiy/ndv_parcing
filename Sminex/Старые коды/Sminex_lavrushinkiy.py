import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'L3jc83bGn93STmUjoLHDRzux7r6T4Scd',
    'scbsid_old': '2746015342',
    '_ym_uid': '1741870829131999708',
    '_ym_d': '1741870829',
    '_gcl_au': '1.1.1966396159.1741870829',
    '_pageCount': '1',
    '_ga_session_id': '13032025.03141178',
    '_gid': 'GA1.2.769152437.1741870829',
    '_ym_isad': '2',
    'tmr_lvid': 'c2f4f6a59fed889a5ebbbe19df187fdb',
    'tmr_lvidTS': '1741870829168',
    '_ga_LB22FX8W2T': 'GS1.2.1741870829.1.0.1741870829.60.0.0',
    '_ym_visorc': 'w',
    'sma_session_id': '2222029281',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    '_cmg_csstqF6Gk': '1741870830',
    '_comagic_idqF6Gk': '9978232298.14168344643.1741870829',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBstart': '1741870829795',
    'domain_sid': 'dBqNyTVfAtkDp_MaFwffZ%3A1741870830215',
    'SCBFormsAlreadyPulled': 'true',
    'SCBporogAct': '5000',
    'tmr_detect': '0%7C1741870831650',
    '_ga': 'GA1.2.890676542.1741870829',
    '_ga_XJQH9S2MME': 'GS1.1.1741870829.1.1.1741870834.55.0.0',
    '_dc_gtm_UA-81340848-25': '1',
    'sma_index_activity': '3223',
    'SCBindexAct': '2973',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://chistye-prudy.ru/katalog-kvartir/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=L3jc83bGn93STmUjoLHDRzux7r6T4Scd; scbsid_old=2746015342; _ym_uid=1741870829131999708; _ym_d=1741870829; _gcl_au=1.1.1966396159.1741870829; _pageCount=1; _ga_session_id=13032025.03141178; _gid=GA1.2.769152437.1741870829; _ym_isad=2; tmr_lvid=c2f4f6a59fed889a5ebbbe19df187fdb; tmr_lvidTS=1741870829168; _ga_LB22FX8W2T=GS1.2.1741870829.1.0.1741870829.60.0.0; _ym_visorc=w; sma_session_id=2222029281; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; _cmg_csstqF6Gk=1741870830; _comagic_idqF6Gk=9978232298.14168344643.1741870829; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBstart=1741870829795; domain_sid=dBqNyTVfAtkDp_MaFwffZ%3A1741870830215; SCBFormsAlreadyPulled=true; SCBporogAct=5000; tmr_detect=0%7C1741870831650; _ga=GA1.2.890676542.1741870829; _ga_XJQH9S2MME=GS1.1.1741870829.1.1.1741870834.55.0.0; _dc_gtm_UA-81340848-25=1; sma_index_activity=3223; SCBindexAct=2973',
}

params = {
    'page': '1',
    'cnt': '300',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:


    response = requests.get('https://lavrushinskiy.ru/ajax/flats/', params=params, cookies=cookies, headers=headers)

    items = response.json()["data"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = "Лаврушинский"
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
        try:
            korpus = int(i["building"])
        except:
            korpus = i["building"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['type'] == 'Квартира':
            type = 'Квартиры'
        else:
            type = i['type']
        if i["finishing"] == '':
            finish_type = "Без отделки"
        else:
            finish_type = i["finishing"]
        try:
            if i["rooms"] == "S":
                room_count = 0
            else:
                room_count = int(i["rooms"])
        except:
            room_count = i["rooms"]
        area = float(i["sq"])
        price_per_metr = ''
        old_price = int(i["price"].replace(" ", ""))
        discount = ''
        price_per_metr_new = ''
        price = ''
        try:
            section = int(i["section"])
        except:
            section = i["section"]
        floor = int(i["floor"])
        try:
            flat_number = int(i['num'])
        except:
            flat_number = i['num']

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