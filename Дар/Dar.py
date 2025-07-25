'''

Подстановка названия ЖК и номеров корпусов идёт через словари. При добавлении нового ЖК нужно обновить и словари тоже.
Снимаем сразу оба ЖК

'''

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from Developer_dict import developer_dict, name_dict

jks = {1317 : "SOLOS", 1316: "Rakurs"}
houses = {1183: '2', 1184: '3', 1185: '4', 1186 : '1', 1187: '2'}

projects_id = ['883', '258']

for pr in projects_id:

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'apptoken': 'e66a54282eb3dfcb12383577c08fe6c4',
        'content-type': 'application/json',
        'origin': 'https://rakurs.moscow',
        'priority': 'u=0, i',
        'referer': 'https://rakurs.moscow/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }

    params = {
            'AgentCostStart': '1',
            'AgentCostEnd': '57368927999',
            'allSquareStart': '1',
            'allSquareEnd': '500',
            'floorStart': '1',
            'floorEnd': '999',
            'id_house': '',
            'windowView': '',
            'viewsType': '',
            'repair': '',
            'placeAttr[]': 'noBooking',
            'page': '1',
            'category[]': 'Квартира',
            'orderBy': 'AgentCost ASC',
            'id_projects[]': pr,
            'saleStatus[]': '1',
        }



    flats = []
    date = datetime.now().date()

    def extract_digits_or_original(s):
        digits = ''.join([char for char in s if char.isdigit()])
        return int(digits) if digits else s

    while True:

        url = 'https://v2.planetarf.ru/api/v3/places'


        response = requests.get(url, headers = headers, params=params)

        items = response.json()["places"]


        for i in items:

            url = ''
            developer = "Дар"
            project = jks.get(i['id_jk'])
            korpus = houses.get(i["id_house"])
            type = 'Квартиры'
            if i["repair"] == 'Предчистовая отделка':
                finish_type = 'Предчистовая'
            else:
                finish_type = i["repair"]
            room_count = int(i["rooms"])
            try:
                area = float(i["allSquare"])
            except:
                area = ''
            try:
                old_price = int(i['AgentCost_old'])
            except:
                old_price = ''
            try:
                price = int(i["AgentCost"])
            except:
                price = ''
            section = ''
            try:
                floor = int(i["floor"])
            except:
                floor = i["floor"]
            flat_number = int(i["id"])

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

    df["Название проекта"] = df["Название проекта"].replace(name_dict)
    df["Девелопер"] = df["Девелопер"].replace(developer_dict)



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

