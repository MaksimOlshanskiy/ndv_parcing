import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

from functions import save_flats_to_excel

cookies = {
    'LANG_UI': 'RU',
    'PHPSESSID': 'Rt7VJHsJQ2ifkUIyrRYMnGAPUwnc34a1',
    'scbsid_old': '2746015342',
    '_ym_uid': '1742892078401907143',
    '_ym_d': '1742892078',
    '_ym_isad': '2',
    '_ga': 'GA1.1.1917105018.1742892078',
    '_ym_visorc': 'w',
    '_ct_ids': 'uj5crw78%3A61515%3A269316141',
    '_ct_session_id': '269316141',
    '_ct_site_id': '61515',
    '_ct': '2500000000191388534',
    'cted': 'modId%3Duj5crw78%3Bclient_id%3D1917105018.1742892078%3Bya_client_id%3D1742892078401907143',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    'sma_session_id': '2237244775',
    'SCBfrom': 'https%3A%2F%2Fduo.moscow%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1742892079608',
    'SCBFormsAlreadyPulled': 'true',
    '_ga_MRTR3VNQFF': 'GS1.1.1742892078.1.1.1742892158.0.0.0',
    'call_s': '___uj5crw78.1742893958.269316141.339240:968190|2___',
    'sma_index_activity': '7227',
    'SCBindexAct': '1515',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://duo.moscow',
    'priority': 'u=1, i',
    'referer': 'https://duo.moscow/flats/parametrical/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'LANG_UI=RU; PHPSESSID=Rt7VJHsJQ2ifkUIyrRYMnGAPUwnc34a1; scbsid_old=2746015342; _ym_uid=1742892078401907143; _ym_d=1742892078; _ym_isad=2; _ga=GA1.1.1917105018.1742892078; _ym_visorc=w; _ct_ids=uj5crw78%3A61515%3A269316141; _ct_session_id=269316141; _ct_site_id=61515; _ct=2500000000191388534; cted=modId%3Duj5crw78%3Bclient_id%3D1917105018.1742892078%3Bya_client_id%3D1742892078401907143; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; sma_session_id=2237244775; SCBfrom=https%3A%2F%2Fduo.moscow%2F; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBporogAct=5000; SCBstart=1742892079608; SCBFormsAlreadyPulled=true; _ga_MRTR3VNQFF=GS1.1.1742892078.1.1.1742892158.0.0.0; call_s=___uj5crw78.1742893958.269316141.339240:968190|2___; sma_index_activity=7227; SCBindexAct=1515',
}

json_data = {
    'square': [
        1,
        11830,
    ],
    'price': [
        1,
        42560.7,
    ],
    'offset': 0,
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://duo.moscow/local/components/idem/search.apartments/templates/.default/ajax/getFlat.php',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    print(response.status_code)

    try:
        items = response.json()["items"]
    except:
        break

    for i in items:

        url = f"https://duo.moscow{i["url"]}"

        date = datetime.date.today()
        project = "Дом Дуо"
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
        developer = "Хаттон"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = "Без отделки"
        try:
            room_count = int(i["rooms"])
        except:
            room_count = i["rooms"]
        area = float(i["square"].replace(",", ".").replace(' ', ''))
        price_per_metr = ''
        old_price = int(i["price"])
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = int(i["floor"])
        try:
            flat_number = int(extract_digits_or_original(i['title']))
        except:
            flat_number = i['title']

        print(
            f"{url}, {project}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    json_data["offset"] = int(json_data["offset"]) + 10
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

save_flats_to_excel(flats, project, developer)