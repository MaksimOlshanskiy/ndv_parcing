import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': 'dreulTzli2StjgslrOr6AycwRP9zsaJF',
    'uid': 'bc501188670593f2b86756c15477bb94',
    'tmr_lvid': 'b918edb952ac5f6deacbec8aca9466d1',
    'tmr_lvidTS': '1744026734213',
    '_ym_uid': '1744026734975016916',
    '_ym_d': '1744026734',
    'scbsid_old': '2746015342',
    '_ym_isad': '2',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_gcl_au': '1.1.1964679793.1744026734',
    '_ym_visorc': 'w',
    '_gid': 'GA1.2.111087568.1744026735',
    '_ct_ids': '8ddee7c2%3A1746%3A2339528808',
    '_ct_session_id': '2339528808',
    '_ct_site_id': '1746',
    '_ct': '2000000003422204927',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cted': 'modId%3D8ddee7c2%3Bclient_id%3D1988675492.1744026734%3Bya_client_id%3D1744026734975016916',
    'domain_sid': 'sK-t7-gApby7OcnafUdOQ%3A1744026735273',
    'sma_session_id': '2253023170',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBstart': '1744026772784',
    'SCBporogAct': '5000',
    '_ga_VF5E0MCX7N': 'GS1.1.1744026734.1.1.1744026778.0.0.0',
    '_ga_Y9H0WWD58Z': 'GS1.1.1744026734.1.1.1744026778.16.0.0',
    '_ga_5GE8L7RXLH': 'GS1.1.1744026734.1.1.1744026778.16.0.0',
    '_ga': 'GA1.2.1988675492.1744026734',
    'carrotquest_session': 'akfiihn5fqfty2qzkg89bm0jbmjedb00',
    'call_s': '___8ddee7c2.1744028578.2339528808.366284:1088978.378901:1066088.434287:1221109|2___',
    'tmr_detect': '0%7C1744026780829',
    'SCBindexAct': '457',
    'sma_index_activity': '658',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://newzelenograd.ru/kvartiry-v-novostroikah/?page=1&chess-build=13&price%5Bmin%5D=3%20813%20530&price%5Bmax%5D=13%20920%20000&area%5Bmin%5D=23&area%5Bmax%5D=60&floor%5Bmin%5D=2&floor%5Bmax%5D=17&sorting=price-asc',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=dreulTzli2StjgslrOr6AycwRP9zsaJF; uid=bc501188670593f2b86756c15477bb94; tmr_lvid=b918edb952ac5f6deacbec8aca9466d1; tmr_lvidTS=1744026734213; _ym_uid=1744026734975016916; _ym_d=1744026734; scbsid_old=2746015342; _ym_isad=2; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _gcl_au=1.1.1964679793.1744026734; _ym_visorc=w; _gid=GA1.2.111087568.1744026735; _ct_ids=8ddee7c2%3A1746%3A2339528808; _ct_session_id=2339528808; _ct_site_id=1746; _ct=2000000003422204927; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cted=modId%3D8ddee7c2%3Bclient_id%3D1988675492.1744026734%3Bya_client_id%3D1744026734975016916; domain_sid=sK-t7-gApby7OcnafUdOQ%3A1744026735273; sma_session_id=2253023170; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%5D; SCBstart=1744026772784; SCBporogAct=5000; _ga_VF5E0MCX7N=GS1.1.1744026734.1.1.1744026778.0.0.0; _ga_Y9H0WWD58Z=GS1.1.1744026734.1.1.1744026778.16.0.0; _ga_5GE8L7RXLH=GS1.1.1744026734.1.1.1744026778.16.0.0; _ga=GA1.2.1988675492.1744026734; carrotquest_session=akfiihn5fqfty2qzkg89bm0jbmjedb00; call_s=___8ddee7c2.1744028578.2339528808.366284:1088978.378901:1066088.434287:1221109|2___; tmr_detect=0%7C1744026780829; SCBindexAct=457; sma_index_activity=658',
}

params = {
    'chess-build': '13',
    'price[min]': '1 813 530',
    'price[max]': '99 920 000',
    'area[min]': '1',
    'area[max]': '999',
    'floor[min]': '1',
    'floor[max]': '99',
    'sorting': 'price-asc',
    'page': '0',
    'showMore': '',
    'getResult': ''
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://newzelenograd.ru/ajax/search.php',
        cookies=cookies,
        headers=headers,
        params = params
    )

    print(response.status_code)

    items = response.json()["elements"]


    for i in items:

        url = ''
        developer = "IKON"
        project = 'Новый Зеленоград'
        korpus = i['building']
        type = 'Квартира'
        if i['finishing']:
            finish_type = 'С отделкой'
        else:
            finish_type = 'Без отделки'
        room_count = int(i['rooms'])
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['price-old'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        section = i['section']
        try:
            floor = int(i['floor'])
        except:
            floor = ''
        flat_number = i['num']

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
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''



        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not items:
        break
    params['page'] = str(int(params['page']) + 1)
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

