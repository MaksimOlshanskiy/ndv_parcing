import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

import requests

cookies = {
    'PHPSESSID': '23bce2006c519e31a97d3d37a7b43309',
    '_ga': 'GA1.1.78696301.1744199825',
    'tmr_lvid': '90b120c5b664ffcb7746c2877fa742c4',
    'tmr_lvidTS': '1744199825310',
    '_ym_uid': '1744199826589358100',
    '_ym_d': '1744199826',
    '_ym_visorc': 'w',
    'domain_sid': 'Rq92cYaewhxIHaO8BJ8TL%3A1744199826355',
    'cted': 'modId%3Dqtdubh9r%3Bclient_id%3D78696301.1744199825%3Bya_client_id%3D1744199826589358100',
    '_ct_ids': 'qtdubh9r%3A51029%3A789028857',
    '_ct_session_id': '789028857',
    '_ct_site_id': '51029',
    'call_s': '___qtdubh9r.1744201626.789028857.240032:742690|2___',
    '_ct': '2100000000444084324',
    '_ym_isad': '2',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'tmr_detect': '0%7C1744199829032',
    '_ga_VV5JQT0JNR': 'GS1.1.1744199825.1.1.1744199837.0.0.0',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://megalit-korolev.ru',
    'priority': 'u=1, i',
    'referer': 'https://megalit-korolev.ru/choose/apartments/?page=3',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=23bce2006c519e31a97d3d37a7b43309; _ga=GA1.1.78696301.1744199825; tmr_lvid=90b120c5b664ffcb7746c2877fa742c4; tmr_lvidTS=1744199825310; _ym_uid=1744199826589358100; _ym_d=1744199826; _ym_visorc=w; domain_sid=Rq92cYaewhxIHaO8BJ8TL%3A1744199826355; cted=modId%3Dqtdubh9r%3Bclient_id%3D78696301.1744199825%3Bya_client_id%3D1744199826589358100; _ct_ids=qtdubh9r%3A51029%3A789028857; _ct_session_id=789028857; _ct_site_id=51029; call_s=___qtdubh9r.1744201626.789028857.240032:742690|2___; _ct=2100000000444084324; _ym_isad=2; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; tmr_detect=0%7C1744199829032; _ga_VV5JQT0JNR=GS1.1.1744199825.1.1.1744199837.0.0.0',
}

params = {
    'page': '3',
}

data = {
    'user_changed': '',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://megalit-korolev.ru/choose/apartments/', params=params, cookies=cookies, headers=headers, data=data)

    items = response.json()['components'][1403]['rendered']




    for i in items:

        url = ''
        developer = ""
        project = ''
        korpus = ''
        type = ''
        finish_type = ''
        room_count = ''
        try:
            area = float()
        except:
            area = ''
        try:
            old_price = int()
        except:
            old_price = ''
        try:
            price = int()
        except:
            price = ''
        section = ''
        try:
            floor = int()
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

    if not items:
        break
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

df = pd.DataFrame(flats, columns=['Дата обновления',
 'Название проекта',
 'на англ',
 'промзона',
 'Местоположение',
 'Метро',
 'Расстояние до метро, км',
 'Время до метро, мин',
 'МЦК/МЦД/БКЛ',
 'Расстояние до МЦК/МЦД, км',
 'Время до МЦК/МЦД, мин',
 'БКЛ',
 'Расстояние до БКЛ, км',
 'Время до БКЛ, мин',
 'статус',
 'старт',
 'Комментарий',
 'Девелопер',
 'Округ',
 'Район',
 'Адрес',
 'Эскроу',
 'Корпус',
 'Конструктив',
 'Класс',
 'Срок сдачи',
 'Старый срок сдачи',
 'Стадия строительной готовности',
 'Договор',
 'Тип помещения',
 'Отделка',
 'Кол-во комнат',
 'Площадь, кв.м',
 'Цена кв.м, руб.',
 'Цена лота, руб.',
 'Скидка,%',
 'Цена кв.м со ск, руб.',
 'Цена лота со ск, руб.',
 'секция',
 'этаж',
 'номер'])



# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Мегалит"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

