import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'scbsid_old': '2746015342',
    '_ym_uid': '176424212225671057',
    '_ym_d': '1764242122',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstKdYd_': '1764571041',
    '_comagic_idKdYd_': '12275156219.16603327389.1764571037',
    'WhiteCallback_visitorId': '21852933473',
    'WhiteCallback_visit': '34463220932',
    'WhiteSaas_uniqueLead': 'no',
    'sma_session_id': '2516722546',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%224e06371f7d7a2cb29802589f261a1f8a%22%2C%225a4ba48b0c99505318ede61cd1067357%22%5D',
    'SCBstart': '1764571042938',
    'sma_postview_ready': '1',
    'SCBporogAct': '5000',
    'SCBindexAct': '1020',
    'sma_index_activity': '7607',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'priority': 'u=1, i',
    'referer': 'https://neometria.ru/novorossiysk/kupit-kvartiru?project=oblaka',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2746015342; _ym_uid=176424212225671057; _ym_d=1764242122; _ym_isad=2; _ym_visorc=w; _cmg_csstKdYd_=1764571041; _comagic_idKdYd_=12275156219.16603327389.1764571037; WhiteCallback_visitorId=21852933473; WhiteCallback_visit=34463220932; WhiteSaas_uniqueLead=no; sma_session_id=2516722546; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%224e06371f7d7a2cb29802589f261a1f8a%22%2C%225a4ba48b0c99505318ede61cd1067357%22%5D; SCBstart=1764571042938; sma_postview_ready=1; SCBporogAct=5000; SCBindexAct=1020; sma_index_activity=7607',
}

params = {
    'city': 'novorossiysk',
    'limit': '20',
    'offset': '0',
    'order': 'price',
    'project': 'oblaka',
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://neometria.ru/api/flats/', params=params, cookies=cookies, headers=headers)
    items = response.json()['results']

    for i in items:

        url = ''
        developer = "Неометрия"
        project = 'Облака'
        korpus = f"{i['phase_number']}.{i['section']}"
        section = ''
        type = ''
        finish_type = i['finish_name']
        room_count = i['rooms']
        flat_number = i['number']
        try:
            area = float(i['area'])
        except:
            area = ''
        try:
            old_price = int(i['original_price'])
            price = int(i['price'])
        except:
            old_price = int(i['price'])
            price = ''
        try:
            floor = int(i['floor'])
        except:
            floor = ''


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
    params['offset'] = str(int(params['offset']) + 20)
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

