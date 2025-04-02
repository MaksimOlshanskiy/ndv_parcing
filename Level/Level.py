# не нашёл откуда вытягивать данные об отделке!!!

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'i': 'ZJuzB3Ny53/QmLq1zLaM0WuzLQrqGYfMlZEgeAIjGcotZy8SaPH/JS41hmLy7hBdWtMEA0poPmoUP+iwGA1Si9+MTik=',
    'yandexuid': '3880545341741613131',
    'yashr': '6772694461741613131',
    'yuidss': '3880545341741613131',
    'ymex': '2056973131.yrts.1741613131',
    'yabs-sid': '424464271741613131',
    'yabs-dsp': 'mts_banner.dUV1bWhncnJUYTZXejdjR1JtSW9CUQ==',
    'yabs-vdrf': 'A0',
    'is_gdpr': '1',
    'is_gdpr_b': 'COiFURCqtAIYAQ==',
    'receive-cookie-deprecation': '1',
    'bh': 'EkEiQ2hyb21pdW0iO3Y9IjEzNCIsICJOb3Q6QS1CcmFuZCI7dj0iMjQiLCAiR29vZ2xlIENocm9tZSI7dj0iMTM0IioCPzA6CSJXaW5kb3dzImCh58S+Bmoe3Mrh/wiS2KGxA5/P4eoD+/rw5w3r//32D8eDzocI',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'text/plain',
    'origin': 'https://level.ru',
    'priority': 'u=1, i',
    'referer': 'https://level.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'i=ZJuzB3Ny53/QmLq1zLaM0WuzLQrqGYfMlZEgeAIjGcotZy8SaPH/JS41hmLy7hBdWtMEA0poPmoUP+iwGA1Si9+MTik=; yandexuid=3880545341741613131; yashr=6772694461741613131; yuidss=3880545341741613131; ymex=2056973131.yrts.1741613131; yabs-sid=424464271741613131; yabs-dsp=mts_banner.dUV1bWhncnJUYTZXejdjR1JtSW9CUQ==; yabs-vdrf=A0; is_gdpr=1; is_gdpr_b=COiFURCqtAIYAQ==; receive-cookie-deprecation=1; bh=EkEiQ2hyb21pdW0iO3Y9IjEzNCIsICJOb3Q6QS1CcmFuZCI7dj0iMjQiLCAiR29vZ2xlIENocm9tZSI7dj0iMTM0IioCPzA6CSJXaW5kb3dzImCh58S+Bmoe3Mrh/wiS2KGxA5/P4eoD+/rw5w3r//32D8eDzocI',
}

params = {
    'project': '',
    'limit': '12',
    'offset': "0",
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://level.ru/api/filter/', params=params, cookies=cookies, headers=headers)
    items = response.json()["results"]

    for i in items:

        url = f"https://level.ru{i["url"]}"

        date = datetime.date.today()
        project = i["project"]
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
        developer = "Level"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = extract_digits_or_original(i["building_name"])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = ''
        if project == "Level Звенигородская, этап 1" and i["section_title"] == '1':
            finish_type = "Предчистовая отделка"
        elif project == "Level Звенигородская, этап 1" and i["section_title"] == '2':
            finish_type = "Без отделки"
        else:
            finish_type = ""
        room_count = int(i["room"])
        area = i["area"]
        price_per_metr = ''
        old_price = i["old_price"]
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        section = int(i["section_title"])
        floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["offset"] = str(int(params["offset"]) + 12)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        break

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

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Level"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

