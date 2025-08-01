# запрос к сайту housing....

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': '5fKgBAhFhY2qZMXTlWCSrK21uW0BJC9h',
    'PRIVACY': '1',
    'scbsid_old': '2746015342',
    '_cmg_csstBndh0': '1751009597',
    '_comagic_idBndh0': '10701590091.14983802606.1751009597',
    'tmr_lvid': 'cb890e29ef43e5554ad57ee3ec8401a8',
    'tmr_lvidTS': '1741874377965',
    '_ym_uid': '1741874378282494327',
    '_ym_d': '1751009598',
    '_ga': 'GA1.2.1025310133.1751009598',
    '_gid': 'GA1.2.516122614.1751009598',
    '_gat_UA-98918245-1': '1',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_gcl_au': '1.1.1944922735.1751009598',
    '_ga_PJJPRF5JJB': 'GS2.2.s1751009597$o1$g0$t1751009597$j60$l0$h0',
    'domain_sid': 'kzYlcNarj1UsChOHJm6LG%3A1751009598555',
    'tmr_detect': '0%7C1751009599787',
    'sma_session_id': '2340788685',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22d3b2a7a62667c988953915d7d3b4139e%22%5D',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1751009638436',
    'sma_postview_ready': '1',
    'SCBindexAct': '549',
    'sma_index_activity': '1102',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://jk-festivalpark.ru/flats/parametrical/?page=3&by=price&order=asc&building=24.3,25,27.1,27.2,26,24.2,24.1&price=89%20%D0%BC%D0%BB%D0%BD%20%E2%82%BD&price_from=11&price_to=89&area=186%20%D0%BC2&area_from=23&area_to=186&floor=35%20&floor_from=1&floor_to=35',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=5fKgBAhFhY2qZMXTlWCSrK21uW0BJC9h; PRIVACY=1; scbsid_old=2746015342; _cmg_csstBndh0=1751009597; _comagic_idBndh0=10701590091.14983802606.1751009597; tmr_lvid=cb890e29ef43e5554ad57ee3ec8401a8; tmr_lvidTS=1741874377965; _ym_uid=1741874378282494327; _ym_d=1751009598; _ga=GA1.2.1025310133.1751009598; _gid=GA1.2.516122614.1751009598; _gat_UA-98918245-1=1; _ym_isad=2; _ym_visorc=w; _gcl_au=1.1.1944922735.1751009598; _ga_PJJPRF5JJB=GS2.2.s1751009597$o1$g0$t1751009597$j60$l0$h0; domain_sid=kzYlcNarj1UsChOHJm6LG%3A1751009598555; tmr_detect=0%7C1751009599787; sma_session_id=2340788685; SCBfrom=; smFpId_old_values=%5B%22d3b2a7a62667c988953915d7d3b4139e%22%5D; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1751009638436; sma_postview_ready=1; SCBindexAct=549; sma_index_activity=1102',
}

params = { "page": 1

}

session = requests.Session()



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = session.get(
        'https://jk-festivalpark.ru/local/components/bs-soft/search.apartments/templates/.default/ajax/housingParameter.php?by=price&order=asc&building=24.3,25,27.1,27.2,26,24.2,24.1&price=65%20%D0%BC%D0%BB%D0%BD%20%E2%82%BD&price_from=13&price_to=65&area=131%20%D0%BC2&area_from=22&area_to=131&floor=35%20&floor_from=1&floor_to=35',
        cookies=cookies,
        headers=headers,
        params=params
    )
    print(response.status_code)

    try:
        items = response.json()["list"]
    except:
        break

    for i in items:

        url = f"https://jk-festivalpark.ru{i["url"]}"

        date = datetime.date.today()
        project = "Фестиваль парк"
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
        developer = "Центр-Инвест"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["parameters"][0]["description"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = "Без отделки"
        try:
            room_count = int(i["roominess"])
        except:
            room_count = i["roominess"]
        area = float(i["parameters"][2]["description"].replace(' м2', ''))
        price_per_metr = ''
        try:
            old_price = int(extract_digits_or_original(i["price"]["old"].replace(" ", "")))
        except:
            old_price = 0
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(extract_digits_or_original(i["price"]["new"].replace(" ", "")))
        except:
            price = int(extract_digits_or_original(i["price"]["price"].replace(" ", "")))
        try:
            section = i["sectionTitle"].split()[1].strip().replace(',', '')
        except:
            section = i["sectionTitle"]
        try:
            floor = int(i["parameters"][1]["description"].split()[0])
        except:
            floor = i["parameters"][1]["description"]
        try:
            flat_number = int(i['num'])
        except:
            flat_number = i['title']

        print(
            f"{project}, {url}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = int(params["page"]) + 1
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)