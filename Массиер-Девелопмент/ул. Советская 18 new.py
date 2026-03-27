import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random
from bs4 import BeautifulSoup
import requests


import requests

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1744269587850169750',
    '_ym_d': '1773414123',
    'tmr_lvid': 'aaa0c78e360a67dda8debedc4153b3bd',
    'tmr_lvidTS': '1744269586814',
    '_ymab_param': 'fPnRZ5rt8mvwnel4uHNvzTltAT07v7hlGcv7V8cIq8UiHnpFekRCYaO0PFW_tsAvjDcKyqAiViTwyq2bcc787tdv_n8',
    '_ct': '2900000000238074074',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cted': 'modId%3Dwl5d4l6j%3Bya_client_id%3D1744269587850169750',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'wl5d4l6j%3A69670%3A370968193',
    '_ct_session_id': '370968193',
    '_ct_site_id': '69670',
    'call_s': '___wl5d4l6j.1774619383.370968193.428573:1222923|2___',
    'kbSession': '17746175837489538',
    'kbCreated': 'Fri, 27 Mar 2026 13:19:44 GMT',
    'kbRes': 'false',
    'kbLoaded': 'true',
    'kbCheck': 'c8b554d1cf309d2426e754c7484c5d41',
    'kbT': 'true',
    'kbUserID': '274270066415224607',
    'domain_sid': 'k_6552vB4Rzqwsne_7mzN%3A1774617585625',
    'tmr_detect': '0%7C1774617586104',
    'activity': '6|20',
    'activity120': '6|20',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://messier-development.group/vybor-kvartiry/?offset=0&limit=20&pagination=true',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744269587850169750; _ym_d=1773414123; tmr_lvid=aaa0c78e360a67dda8debedc4153b3bd; tmr_lvidTS=1744269586814; _ymab_param=fPnRZ5rt8mvwnel4uHNvzTltAT07v7hlGcv7V8cIq8UiHnpFekRCYaO0PFW_tsAvjDcKyqAiViTwyq2bcc787tdv_n8; _ct=2900000000238074074; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cted=modId%3Dwl5d4l6j%3Bya_client_id%3D1744269587850169750; _ym_isad=2; _ym_visorc=w; _ct_ids=wl5d4l6j%3A69670%3A370968193; _ct_session_id=370968193; _ct_site_id=69670; call_s=___wl5d4l6j.1774619383.370968193.428573:1222923|2___; kbSession=17746175837489538; kbCreated=Fri, 27 Mar 2026 13:19:44 GMT; kbRes=false; kbLoaded=true; kbCheck=c8b554d1cf309d2426e754c7484c5d41; kbT=true; kbUserID=274270066415224607; domain_sid=k_6552vB4Rzqwsne_7mzN%3A1774617585625; tmr_detect=0%7C1774617586104; activity=6|20; activity120=6|20',
}


params = {
    'offset': '0',
    'limit': '200',
    'pagination': 'true',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



response = requests.get('https://messier-development.group/api/flats/', params=params, cookies=cookies, headers=headers)
items = response.json()['results']

for i in items:

    url = ''
    developer = "Мессиер-Девелопмент"
    project = 'Советская 18 (Мессиер 18)'
    korpus = i['building_number']
    type = 'Квартиры'
    finish_type = 'Без отделки'
    room_count = i['rooms']
    try:
        area = float(i['area'])
    except:
        area = ''
    try:
        old_price = i['origin_price']
    except:
        old_price = ''
    try:
        price = i['price']
    except:
        price = ''
    section = ''
    try:
        floor = int(i['floor'])
    except:
        floor = ''
    flat_number = ''


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


save_flats_to_excel(flats, project, developer)

