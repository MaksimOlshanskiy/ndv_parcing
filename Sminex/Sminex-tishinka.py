import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'scbsid_old': '2746015342',
    '_ym_uid': '1741865597656020842',
    '_ym_d': '1741865597',
    '_ga': 'GA1.1.1615918338.1741865597',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstqF6Gk': '1741865597',
    '_comagic_idqF6Gk': '9977779153.14167802418.1741865597',
    'sma_session_id': '2221916830',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBstart': '1741865600584',
    'PHPSESSID': 'Dy0Nt8UpEm7jabl3HBm8GpVTyfYmFqNg',
    'SCBFormsAlreadyPulled': 'true',
    'sma_index_activity': '2377',
    'SCBindexAct': '1874',
    '_ga_TG4QB7KZS7': 'GS1.1.1741865597.1.1.1741867114.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://tishinskiy-b.ru/vibor-kvartir/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2746015342; _ym_uid=1741865597656020842; _ym_d=1741865597; _ga=GA1.1.1615918338.1741865597; _ym_isad=2; _ym_visorc=w; _cmg_csstqF6Gk=1741865597; _comagic_idqF6Gk=9977779153.14167802418.1741865597; sma_session_id=2221916830; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBstart=1741865600584; PHPSESSID=Dy0Nt8UpEm7jabl3HBm8GpVTyfYmFqNg; SCBFormsAlreadyPulled=true; sma_index_activity=2377; SCBindexAct=1874; _ga_TG4QB7KZS7=GS1.1.1741865597.1.1.1741867114.0.0.0',
}

params = {
    'filter[price_mln][0]': '0',
    'filter[price_mln][1]': '0',
    'filter[price_mlnusd][0]': '0',
    'filter[price_mlnusd][1]': '0',
    'filter[price_mlneur][0]': '0',
    'filter[price_mlneur][1]': '0',
    'filter[price_sqm][0]': '0',
    'filter[price_sqm][1]': '0',
    'filter[price_sqmusd][0]': '0',
    'filter[price_sqmusd][1]': '0',
    'filter[price_sqmeur][0]': '0',
    'filter[price_sqmeur][1]': '0',
    'filter[sq][0]': '0',
    'filter[sq][1]': '0',
    'filter[hide_reserved][0]': 'Y',
    'filter[flat]': '',
    'sort[sq]': '1',
    'page': '1',
    'cnt': '130',
    'trigger': '',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://tishinskiy-b.ru/local/ajax/flats/', params=params, cookies=cookies, headers=headers)

    items = response.json()["data"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = "Тишинский бульвар"
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