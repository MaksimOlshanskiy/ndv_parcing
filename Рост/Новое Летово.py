# отдельно выгрузка с отделкой и отдельно без отделки  'finish_option': '1' - с отделкой

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from datetime import datetime


import requests

cookies = {
    'session': '3a3e139cfbf2b8537b8e21c45060d5c3a1cbbc19d5fdec06cccc8e500aeb5f05',
    'tmr_lvid': '5d5f2bd56eca9e775b392465b470cf88',
    'tmr_lvidTS': '1742910059220',
    '_ga': 'GA1.1.1884967195.1742910059',
    'session_timer_104054': '1',
    'session_timer_104055': '1',
    'session_timer_104056': '1',
    'session_timer_104057': '1',
    '_ym_uid': '1742910059476931813',
    '_ym_d': '1742910059',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstfoQF7': '1742910060',
    '_comagic_idfoQF7': '9219458852.13157208757.1742910059',
    'domain_sid': 'R7uMIH0_ahjSIFayMODUP%3A1742910061018',
    'seconds_on_page_104054': '18',
    'seconds_on_page_104055': '18',
    'seconds_on_page_104056': '18',
    'seconds_on_page_104057': '18',
    'pageCount': '2',
    'tmr_detect': '0%7C1742910080629',
    '_ga_Z0HNVGBMKF': 'GS1.1.1742910059.1.1.1742910144.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://novoe-letovo.ru/flats?finishing_type=no',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 'novoe-letovo.ru',
    # 'cookie': 'session=3a3e139cfbf2b8537b8e21c45060d5c3a1cbbc19d5fdec06cccc8e500aeb5f05; tmr_lvid=5d5f2bd56eca9e775b392465b470cf88; tmr_lvidTS=1742910059220; _ga=GA1.1.1884967195.1742910059; session_timer_104054=1; session_timer_104055=1; session_timer_104056=1; session_timer_104057=1; _ym_uid=1742910059476931813; _ym_d=1742910059; _ym_isad=2; _ym_visorc=w; _cmg_csstfoQF7=1742910060; _comagic_idfoQF7=9219458852.13157208757.1742910059; domain_sid=R7uMIH0_ahjSIFayMODUP%3A1742910061018; seconds_on_page_104054=18; seconds_on_page_104055=18; seconds_on_page_104056=18; seconds_on_page_104057=18; pageCount=2; tmr_detect=0%7C1742910080629; _ga_Z0HNVGBMKF=GS1.1.1742910059.1.1.1742910144.0.0.0',
}

params = {
    'project_id': '23388869-3da0-4291-828b-2979c6fb0622',
    'status': 'free',
    'offset': '0',
    'limit': '48',
    'finishing_type': [
        'no',
        'white_box',
    ],
    'order_by': 'total_area',
}





flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s




while True:

    response = requests.get(
        'https://novoe-letovo.ru/api/realty-filter/residential/real-estates',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    items = response.json()

    for i in items:

        url = ''


        date = datetime.now()
        project = i['project_name']


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
        developer = "Рост"
        okrug = ''
        district = ''
        adress = i['address']
        eskrou = ''
        korpus = i['building_int_number']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        if i['finishing_type'] == "white_box":
            finish_type = 'Предчистовая отделка'
        else:
            finish_type = 'Без отделки'

        room_count = i['rooms']

        area = float(i['total_area'])

        price_per_metr = ''
        old_price = i['old_price']
        discount = ''
        price_per_metr_new = ''
        price = i["price"]

        section = int(i['section_number'])
        floor = int(i['floor_number'])
        flat_number = i['number']



        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not items:
        break
    params["offset"] = int(params["offset"]) + 48
    sleep_time = random.uniform(1, 4)
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

current_date = datetime.now().date()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Рост"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)