import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
from datetime import datetime
import random

cookies = {
    'auth.strategy': 'local',
    'adrdel': '1748506330496',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1748592730505%2C%22sl%22%3A%7B%22224%22%3A1748506330505%2C%221228%22%3A1748506330505%7D%7D',
    'scbsid_old': '2746015342',
    '_cmg_cssttGbx8': '1748506331',
    '_comagic_idtGbx8': '9453719617.13433207912.1748506330',
    '_ym_uid': '1748506331775341849',
    '_ym_d': '1748506331',
    'PHPSESSID': '0jt5s9dl4rqce73som55vrp7ha',
    'startSession': 'true',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22f0a18207107a745e280d9357abcbd51d%22%5D',
    'SCBstart': '1748506334942',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_session_id': '2310216424',
    'SCBindexAct': '810',
    'PageNumber': '8',
    'pageviewTimer': '344',
    'startDate': '1748506676061',
    'sma_index_activity': '4233',
    'SCBindexAct': '3709',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://ice-towers.ru/search',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': 'auth.strategy=local; adrdel=1748506330496; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1748592730505%2C%22sl%22%3A%7B%22224%22%3A1748506330505%2C%221228%22%3A1748506330505%7D%7D; scbsid_old=2746015342; _cmg_cssttGbx8=1748506331; _comagic_idtGbx8=9453719617.13433207912.1748506330; _ym_uid=1748506331775341849; _ym_d=1748506331; PHPSESSID=0jt5s9dl4rqce73som55vrp7ha; startSession=true; _ym_isad=2; _ym_visorc=w; SCBfrom=https%3A%2F%2Fyandex.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%22f0a18207107a745e280d9357abcbd51d%22%5D; SCBstart=1748506334942; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_session_id=2310216424; SCBindexAct=810; PageNumber=8; pageviewTimer=344; startDate=1748506676061; sma_index_activity=4233; SCBindexAct=3709',
}

response = requests.get('https://ice-towers.ru/api/hydra/data', cookies=cookies, headers=headers)

data = response.json()["apartments"]
flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for key, inner_dict in data.items():

    url = ''
    developer = "Град"
    project = 'ICE TOWERS'
    korpus = inner_dict['b']
    if inner_dict['t'] == 'Квартира':
        type = 'Квартиры'
    finish_type = 'Без отделки'
    room_count = inner_dict['rc']
    try:
        area = inner_dict['sq']
    except:
        area = ''
    try:
        old_price = int()
    except:
        old_price = ''
    try:
        price = inner_dict['tc']
    except:
        price = ''
    if price == 0:
        continue
    section = inner_dict['s']
    try:
        floor = int(inner_dict['f'])
    except:
        floor = ''
    flat_number = inner_dict['tr_n']


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

