import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    'session': 'ee67d670a77185171cdddee3def5c3cda8f4aba83e98c025ef7b58dd0b782fcf',
    'tmr_lvid': 'a75bace7f8204896de9dc77cf70e4731',
    'tmr_lvidTS': '1744104565302',
    'scbsid_old': '2746015342',
    '_ym_uid': '1744104566621664155',
    '_ym_d': '1744104566',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': 'fh-vdm9bFPiPyWd_6nOnu%3A1744104566138',
    '_cmg_cssts_GL1': '1744104570',
    '_comagic_ids_GL1': '9271096832.13218694877.1744104569',
    'sma_session_id': '2254127166',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBstart': '1744104571517',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'tmr_detect': '0%7C1744104573181',
    'SCBindexAct': '492',
    'sma_index_activity': '692',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://xn----7sbfkqrmjg.xn--p1ai/flats',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-host': 'xn----7sbfkqrmjg.xn--p1ai',
    # 'cookie': 'session=ee67d670a77185171cdddee3def5c3cda8f4aba83e98c025ef7b58dd0b782fcf; tmr_lvid=a75bace7f8204896de9dc77cf70e4731; tmr_lvidTS=1744104565302; scbsid_old=2746015342; _ym_uid=1744104566621664155; _ym_d=1744104566; _ym_isad=2; _ym_visorc=w; domain_sid=fh-vdm9bFPiPyWd_6nOnu%3A1744104566138; _cmg_cssts_GL1=1744104570; _comagic_ids_GL1=9271096832.13218694877.1744104569; sma_session_id=2254127166; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%5D; SCBstart=1744104571517; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; tmr_detect=0%7C1744104573181; SCBindexAct=492; sma_index_activity=692',
}

params = {
    'project_id': '33974217-154f-492c-a9d4-b783b130d58e',
    'status': 'free',
    'offset': '0',
    'limit': '48',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get(
        'https://xn----7sbfkqrmjg.xn--p1ai/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    items = response.json()


    for i in items:

        url = ''
        developer = "Вектор"
        project = 'Олива Лесной городок'
        korpus = i['building_int_number']
        type = 'Квартиры'
        if i['finishing_type'] == 'no':
            finish_type = 'Без отделки'
        elif i['finishing_type'] == 'fine':
            finish_type = 'С отделкой'
        elif i['finishing_type'] == 'white_box':
            finish_type = 'Предчистовая'
        else:
            finish_type = i['finishing_type']
        room_count = i['rooms']
        try:
            area = float(i['total_area'])
        except:
            area = ''
        try:
            old_price = int(i['old_price'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        section = int(i['section_number'])
        try:
            floor = int(i['floor_number'])
        except:
            floor = ''
        flat_number = i['int_number']

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
        srok_sdachi = i['completion_title']
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
    params['offset'] = str(int(params['offset']) + 48)
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
base_path = r""

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

