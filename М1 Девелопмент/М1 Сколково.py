import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': '693271b3bc792732aedf9207d9191db5',
    'uls_start_page': 'https%3A%2F%2Fm1-skolkovo.ru%2F%23prices',
    'uls_user': '52177244201',
    'BX_USER_ID': '0637000992907e90803d486cd4459565',
    '_ym_uid': '1742546248299393599',
    '_ym_d': '1742546248',
    '_ct_ids': '2seisbk8%3A31330%3A948672552',
    '_ct_session_id': '948672552',
    '_ct_site_id': '31330',
    'call_s': '___2seisbk8.1742548047.948672552.242951:993158|2___',
    '_ct': '1100000000647429852',
    '_ym_visorc': 'w',
    '_ym_isad': '1',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    '_ga': 'GA1.2.168199590.1742546255',
    '_gid': 'GA1.2.2082679752.1742546255',
    '_gat_UA-140922374-1': '1',
    '_fbp': 'fb.1.1742546256944.993850831743809857',
    '_ga_H6WL8PX0RC': 'GS1.2.1742546257.1.0.1742546257.60.0.0',
    'cted': 'modId%3D2seisbk8%3Bya_client_id%3D1742546248299393599%3Bclient_id%3D168199590.1742546255%3Bfbp%3Dfb.1.1742546256944.993850831743809857',
    'uls_visit': '1',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://m1-skolkovo.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=693271b3bc792732aedf9207d9191db5; uls_start_page=https%3A%2F%2Fm1-skolkovo.ru%2F%23prices; uls_user=52177244201; BX_USER_ID=0637000992907e90803d486cd4459565; _ym_uid=1742546248299393599; _ym_d=1742546248; _ct_ids=2seisbk8%3A31330%3A948672552; _ct_session_id=948672552; _ct_site_id=31330; call_s=___2seisbk8.1742548047.948672552.242951:993158|2___; _ct=1100000000647429852; _ym_visorc=w; _ym_isad=1; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; _ga=GA1.2.168199590.1742546255; _gid=GA1.2.2082679752.1742546255; _gat_UA-140922374-1=1; _fbp=fb.1.1742546256944.993850831743809857; _ga_H6WL8PX0RC=GS1.2.1742546257.1.0.1742546257.60.0.0; cted=modId%3D2seisbk8%3Bya_client_id%3D1742546248299393599%3Bclient_id%3D168199590.1742546255%3Bfbp%3Dfb.1.1742546256944.993850831743809857; uls_visit=1',
}



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


response = requests.get('https://m1-skolkovo.ru/create_json.php', cookies=cookies, headers=headers)

items = response.json()

for i in items:

    url = f'https://m1-skolkovo.ru{i["URL"]}'

    date = datetime.date.today()
    project = "М1 Сколково"

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
    developer = "М1 Девелопмент"
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
    type = 'Апартаменты'
    finish_type = 'Без отделки'

    room_count = int(i['FlatRoomsCount'])

    area = float(i["TotalArea"])
    price_per_metr = ''
    old_price = int(i["Price"])
    discount = ''
    price_per_metr_new = ''
    price = ''
    section = int(i["SectionNumber"])
    floor = int(i["FloorNumber"])
    flat_number = ''

    print(
        f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)


save_flats_to_excel(flats, project, developer)