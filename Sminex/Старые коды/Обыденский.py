import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'JpFUZrkkKsniHj4QxoK9M7zfFDnHo8LH',
    'scbsid_old': '2746015342',
    '_cmg_csstqF6Gk': '1753689524',
    '_comagic_idqF6Gk': '10650188318.14948809898.1753689521',
    '_gid': 'GA1.2.6558764.1753689524',
    '_ym_uid': '1753689525113224654',
    '_ym_d': '1753689525',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'sma_session_id': '2373043955',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D',
    'SCBstart': '1753689528069',
    'SCBporogAct': '5000',
    'sma_index_activity': '1189',
    'SCBindexAct': '1189',
    '_gat_gtag_UA_81340848_30': '1',
    '_ga_73PD1LSHMN': 'GS2.1.s1753689523$o1$g1$t1753689740$j56$l0$h0',
    '_ga': 'GA1.1.1429365699.1753689524',
    '_ga_4JRM31FXXH': 'GS2.1.s1753689524$o1$g1$t1753689740$j56$l0$h0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://obydenskiy-1.ru/kvartiry/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=JpFUZrkkKsniHj4QxoK9M7zfFDnHo8LH; scbsid_old=2746015342; _cmg_csstqF6Gk=1753689524; _comagic_idqF6Gk=10650188318.14948809898.1753689521; _gid=GA1.2.6558764.1753689524; _ym_uid=1753689525113224654; _ym_d=1753689525; _ym_isad=2; _ym_visorc=w; sma_session_id=2373043955; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D; SCBstart=1753689528069; SCBporogAct=5000; sma_index_activity=1189; SCBindexAct=1189; _gat_gtag_UA_81340848_30=1; _ga_73PD1LSHMN=GS2.1.s1753689523$o1$g1$t1753689740$j56$l0$h0; _ga=GA1.1.1429365699.1753689524; _ga_4JRM31FXXH=GS2.1.s1753689524$o1$g1$t1753689740$j56$l0$h0',
}

params = {
    'filter': '{"price":[0,0],"sq":[0,0],"price_mlnusd":[0,0],"price_mlneur":[0,0],"price_sqm":[0,0],"price_sqmusd":[0,0],"price_sqmeur":[0,0],"project":[],"stage":[],"rooms":[],"floor":[],"ids":[],"typeofsize":[],"type":[],"views":[],"worldsides":[],"section":[],"building":[],"advantages":[],"penthouse":[],"plantype":[],"balcony":[],"hide_reserved":["Y"],"flat":""}',
    'sort': '{"price":2}',
    'page': '1',
    'cnt': '30',
    'trigger': ''
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:


    response = requests.get('https://obydenskiy-1.ru/ajax/flats/', params=params, cookies=cookies, headers=headers)

    items = response.json()["data"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = "Обыденский"
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
            korpus = '1'
        except:
            korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
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