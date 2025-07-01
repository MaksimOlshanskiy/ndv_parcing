import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'scbsid_old': '2746015342',
    '_ym_uid': '175102697733232207',
    '_ym_d': '1751026977',
    'SCBnotShow': '-1',
    'PHPSESSID': 'C2Om9gg4EGMTQYhXl1CNImuJ6LcmLXRD',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'sma_session_id': '2343651904',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    '_cmg_csstqF6Gk': '1751266777',
    '_comagic_idqF6Gk': '10515642908.14792393388.1751266776',
    'smFpId_old_values': '%5B%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D',
    'SCBstart': '1751266777282',
    'SCBporogAct': '5000',
    'sma_index_activity': '3440',
    'SCBindexAct': '1940',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://foriver.ru/vibor-kvartir/po-parametram/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2746015342; _ym_uid=175102697733232207; _ym_d=1751026977; SCBnotShow=-1; PHPSESSID=C2Om9gg4EGMTQYhXl1CNImuJ6LcmLXRD; _ym_isad=2; _ym_visorc=w; sma_session_id=2343651904; SCBfrom=https%3A%2F%2Fyandex.ru%2F; _cmg_csstqF6Gk=1751266777; _comagic_idqF6Gk=10515642908.14792393388.1751266776; smFpId_old_values=%5B%22f0a18207107a745e280d9357abcbd51d%22%2C%22d3b2a7a62667c988953915d7d3b4139e%22%2C%22ca505640ddf99ec8d4755fa1299dcd1a%22%2C%22a7ea49fc46c5a5b146d731ca169a44ef%22%5D; SCBstart=1751266777282; SCBporogAct=5000; sma_index_activity=3440; SCBindexAct=1940',
}

params = {
    'filter[price_mln][0]': '0',
    'filter[price_mln][1]': '0',
    'filter[price_mlnusd][0]': '0',
    'filter[price_mlnusd][1]': '0',
    'filter[price_mlneur][0]': '0',
    'filter[price_mlneur][1]': '0',
    'filter[price_sqm][0]': '0',
    'filter[price_sqm][1]': '0',
    'filter[price_sqmusd][0]': '0',
    'filter[price_sqmusd][1]': '0',
    'filter[price_sqmeur][0]': '0',
    'filter[price_sqmeur][1]': '0',
    'filter[sq][0]': '0',
    'filter[sq][1]': '0',
    'filter[hide_reserved][0]': 'Y',
    'filter[flat]': '',
    'sort[sq]': '1',
    'page': '1',
    'cnt': '30',
    'trigger': '',
}




flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://foriver.ru/local/ajax/flats/', params=params, cookies=cookies, headers=headers)
    items = response.json()['data']
    print(items)

    for i in items:

        url = ''
        developer = "Sminex"
        project = i['project']
        korpus = i['building']
        section = i['section']
        type = i['type']
        finish_type = i['finishing']
        room_count = i['rooms']
        flat_number = i['flats_num_maket']
        try:
            area = float(i['sq'])
        except:
            area = ''
        try:
            old_price = int(i['price'].replace(' ', ''))
        except:
            old_price = ''
        try:
            price = int(i['real_price'].replace(' ', ''))
        except:
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
    params['page'] = str(int(params['page']) + 1)
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

