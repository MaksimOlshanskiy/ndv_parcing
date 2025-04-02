import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    'PHPSESSID': 'PQTvoXciTxIIKgasSy2S2VIH9D6VRnBY',
    'scbsid_old': '2746015342',
    '_ym_uid': '1741869673948987914',
    '_ym_d': '1741869673',
    '_ym_isad': '2',
    '_gid': 'GA1.2.147016623.1741869673',
    '_gat_UA-226991067-1': '1',
    '_ym_visorc': 'w',
    '_ga_YHY9WGMHMM': 'GS1.2.1741869672.1.0.1741869674.0.0.0',
    'sma_session_id': '2222003872',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBstart': '1741869674455',
    '_cmg_csstqF6Gk': '1741869675',
    '_comagic_idqF6Gk': '9978135203.14168228683.1741869674',
    'SCBFormsAlreadyPulled': 'true',
    'PageNumber': '2',
    '_ga': 'GA1.2.2105420816.1741869673',
    '_ga_S5EPW7DCRD': 'GS1.1.1741869672.1.1.1741869691.0.0.0',
    'sma_index_activity': '1174',
    'SCBindexAct': '921',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://ilyinka.ru/flats/list/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=PQTvoXciTxIIKgasSy2S2VIH9D6VRnBY; scbsid_old=2746015342; _ym_uid=1741869673948987914; _ym_d=1741869673; _ym_isad=2; _gid=GA1.2.147016623.1741869673; _gat_UA-226991067-1=1; _ym_visorc=w; _ga_YHY9WGMHMM=GS1.2.1741869672.1.0.1741869674.0.0.0; sma_session_id=2222003872; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBstart=1741869674455; _cmg_csstqF6Gk=1741869675; _comagic_idqF6Gk=9978135203.14168228683.1741869674; SCBFormsAlreadyPulled=true; PageNumber=2; _ga=GA1.2.2105420816.1741869673; _ga_S5EPW7DCRD=GS1.1.1741869672.1.1.1741869691.0.0.0; sma_index_activity=1174; SCBindexAct=921',
}

params = {
    'filter[price][0]': '0',
    'filter[price][1]': '0',
    'filter[sq][0]': '0',
    'filter[sq][1]': '0',
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
    'filter[hide_reserved][0]': 'Y',
    'filter[flat]': '',
    'sort[sq]': '1',
    'page': '1',
    'cnt': '300',
    'trigger': '',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:


    response = requests.get('https://ilyinka.ru/ajax/flats/', params=params, cookies=cookies, headers=headers)

    items = response.json()["data"]

    for i in items:

        url = ""

        date = datetime.date.today()
        project = "West Garden"
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
        developer = "Sminex"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            korpus = int(i["building"])
        except:
            korpus = i["building"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = ''
        if i["finishing"] == '':
            finish_type = "Без отделки"
        else:
            finish_type = i["finishing"]
        try:
            if i["rooms"] == "S":
                room_count = 0
            else:
                room_count = int(i["rooms"])
        except:
            room_count = i["rooms"]
        area = float(i["sq"])
        price_per_metr = ''
        old_price = ""
        discount = ''
        price_per_metr_new = ''
        price =  int(i["price"].replace(" ", ""))
        try:
            section = int(i["section"])
        except:
            section = i["section"]
        floor = int(i["floor"])
        try:
            flat_number = int(i['num'])
        except:
            flat_number = i['num']

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = str(int(params["page"]) + 1)
    sleep_time = random.uniform(2, 10)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Sminex"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_Ильинка_3-8_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)