import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

import requests

cookies = {
    '__5ef7e0433e4ed89e1ed6401318dbd504': 'd9adbb3436f0082d7fd4c7bf9c607aa1',
    'tmr_lvid': '6baabad62ed97e0c8cac51d222b836a3',
    'tmr_lvidTS': '1743769149664',
    '_cmg_csst9Qnhc': '1743769150',
    '_comagic_id9Qnhc': '10557529454.14690325474.1743769148',
    '_ym_uid': '174376915093858061',
    '_ym_d': '1743769150',
    '_ym_isad': '2',
    'domain_sid': 'Z0B8lqisAdcpj4Arm6MOk%3A1743769150745',
    '_ym_visorc': 'w',
    'cto_bundle': 'A2jldl9Rbmd2USUyQiUyRnpCcXY5dyUyQjglMkJzNE5SUWdTT2o5U0RSMzNKZFRoUmJ1UE1GTTRSU0I5eEIlMkI3ejVydXNxVjZmaXlnbmZYV01ickJBU0loQmclMkZDWVNUdVNWbmJBbVBydHRjbm9MaDlZaUdLNTVidnRFNGN4Y01ZVndUcU9jbUVOclAlMkJsNDkxZDJuSzlVT0dqdFNkNTdxcXkyWWlpYUNVRDAxY2dCQkpJWVp2WUhWOCUzRA',
    'tmr_detect': '0%7C1743769565320',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'if-modified-since': 'Fri, 04 Apr 2025 12:26:03 GMT',
    'priority': 'u=1, i',
    'referer': 'https://novo-molokovo.ru/kvartiry/choice-of-apartments/view-grid/?price_from=4+498+000&price_to=128+842+000&property_145_from=16&property_145_to=682&property_208=0&status_build=0&property_167=0&filter=1',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '__5ef7e0433e4ed89e1ed6401318dbd504=d9adbb3436f0082d7fd4c7bf9c607aa1; tmr_lvid=6baabad62ed97e0c8cac51d222b836a3; tmr_lvidTS=1743769149664; _cmg_csst9Qnhc=1743769150; _comagic_id9Qnhc=10557529454.14690325474.1743769148; _ym_uid=174376915093858061; _ym_d=1743769150; _ym_isad=2; domain_sid=Z0B8lqisAdcpj4Arm6MOk%3A1743769150745; _ym_visorc=w; cto_bundle=A2jldl9Rbmd2USUyQiUyRnpCcXY5dyUyQjglMkJzNE5SUWdTT2o5U0RSMzNKZFRoUmJ1UE1GTTRSU0I5eEIlMkI3ejVydXNxVjZmaXlnbmZYV01ickJBU0loQmclMkZDWVNUdVNWbmJBbVBydHRjbm9MaDlZaUdLNTVidnRFNGN4Y01ZVndUcU9jbUVOclAlMkJsNDkxZDJuSzlVT0dqdFNkNTdxcXkyWWlpYUNVRDAxY2dCQkpJWVp2WUhWOCUzRA; tmr_detect=0%7C1743769565320',
}

params = {
    'sorting': '0',
    'price_from': '4498000',
    'price_to': '128842000',
    'property_145_from': '16',
    'property_145_to': '682',
    'property_167': '0',
    'filter': '1',
    'action': '',
}



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

counter = 1

while True:

    if counter == 1:
        response = requests.get(
            'https://novo-molokovo.ru/kvartiry/choice-of-apartments/view-grid/',
            params=params,
            cookies=cookies,
            headers=headers,
        )
    else:
        response = requests.get(
            f'https://novo-molokovo.ru/kvartiry/choice-of-apartments/view-grid/page-{counter}/',
            params=params,
            cookies=cookies,
            headers=headers,
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # все карточки квартир
    flats_soup = soup.find_all("div", class_= 'param_resultList__item _new')

    for i in flats_soup:



        url = ''

        date = datetime.date.today()
        project = "Ново-Молоково"

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
        developer = "Ар Ди Ай"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            korpus = int(i.find('div', class_= 'param_resultList__item--place').text.split()[1])
        except:
            korpus = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = "С отделкой"
        if 'Е' in i.find('div', class_='param_resultList__item--name').text.split()[1]:
            room_count = str(extract_digits_or_original(i.find('div', class_='param_resultList__itemInfo--room').text))+'Е'
        else:
            room_count = extract_digits_or_original(i.find('div', class_='param_resultList__itemInfo--room').text)

        area = float(i.find('div', class_='param_resultList__itemInfo--square').text.replace(' м²', ''))
        price_per_metr = ''
        old_price = int(i.find('span', class_= 'param_resultList__itemInfoPrice--old').text.strip().replace('₽', '').replace(' ', ''))

        discount = ''
        price_per_metr_new = ''
        price = int(i.find('span', class_= 'param_resultList__itemInfoPrice--hot').text.strip().replace('₽', '').replace(' ', ''))
        section = int(i.find('div', class_= 'param_resultList__item--place').text.split()[-6])
        floor = int(i.find('div', class_= 'param_resultList__item--place').text.split()[-3])
        flat_number = int(i.find('div', class_= 'param_resultList__item--place').text.split()[-1].replace('№', ''))

        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    counter += 1
    if not flats_soup:
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
base_path = r"C:\\Users\\m.olshanskiy\\PycharmProjects\\ndv_parsing\\Ар Ди Ай"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}_отделка.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
