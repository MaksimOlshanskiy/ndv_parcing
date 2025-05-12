import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    '__ddg9_': '91.108.227.31',
    '__ddg1_': 'ZRyROBeQARGk2nXIvwj2',
    'tmr_lvid': 'c30c50b0541ba21ba401a8b744a17f78',
    'tmr_lvidTS': '1746432915678',
    '_ym_uid': '1746432917635770962',
    '_ym_d': '1746432917',
    '_ym_isad': '2',
    '_ct_ids': 'zuel8ymv%3A69926%3A152824808',
    '_ct_session_id': '152824808',
    '_ct_site_id': '69926',
    '_ct': '2900000000101622311',
    'domain_sid': '7Ro2Ltfg-4qeRRN0H52AO%3A1746432917575',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dzuel8ymv%3Bya_client_id%3D1746432917635770962',
    'call_s': '___zuel8ymv.1746434714.152824808.424919:1190337|2___',
    'tmr_detect': '0%7C1746432924369',
    '__ddg10_': '1746433137',
    '__ddg8_': 'spbiDQJM0E2DLY3n',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://mechta.su',
    'priority': 'u=1, i',
    'referer': 'https://mechta.su/catalog/?currentType=%5B%7B%22value%22%3A%22cottage%22%2C%22label%22%3A%22%D0%9A%D0%BE%D1%82%D1%82%D0%B5%D0%B4%D0%B6%22%7D%5D',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '__ddg9_=91.108.227.31; __ddg1_=ZRyROBeQARGk2nXIvwj2; tmr_lvid=c30c50b0541ba21ba401a8b744a17f78; tmr_lvidTS=1746432915678; _ym_uid=1746432917635770962; _ym_d=1746432917; _ym_isad=2; _ct_ids=zuel8ymv%3A69926%3A152824808; _ct_session_id=152824808; _ct_site_id=69926; _ct=2900000000101622311; domain_sid=7Ro2Ltfg-4qeRRN0H52AO%3A1746432917575; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ym_visorc=w; cted=modId%3Dzuel8ymv%3Bya_client_id%3D1746432917635770962; call_s=___zuel8ymv.1746434714.152824808.424919:1190337|2___; tmr_detect=0%7C1746432924369; __ddg10_=1746433137; __ddg8_=spbiDQJM0E2DLY3n',
}

data = {
    'action': 'get_realty',
    'nextPostIndex': '1',
    'amount': '500',
    'housesParsed': '',
    'filters[currentType][]': [
        'flat',
        'townhouse',
        'ready-townhouse',
        'cottage',
    ],
    'filters[currentSort]': 'cheap',
    'filters[currentCheckInData]': '',
    'filters[currentFloors]': '',
    'filters[currentBuildings]': '',
    'filters[currentLayoutType]': '',
    'filters[currentWindowView]': '',
    'filters[currentFeatures]': '',
    'filters[currentAdvantages]': '',
    'onlyAmount': '',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://mechta.su/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['realty']

    for i in items:

        url = ''
        developer = "ГК Мега-Мечта"
        project = 'Мечта'
        try:
            korpus = i['building_number']
        except:
            korpus = ''
        section = ''
        if i['realty_type'] == 'cottage':
            type = 'Коттеджи'
        elif i['realty_type'] == 'flat':
            type = 'Квартиры'
        elif i['realty_type'] == 'townhouse' or i['realty_type'] == 'ready-townhouse':
            type = 'Таунхаусы'
        else:
            type = i['realty_type']
        try:
            if i['finishing'] == 'base':
                finish_type = 'Без отделки'
            elif i['finishing'] == 'semiclear':
                finish_type = 'Предчистовая'
            elif i['finishing'] == 'clear':
                finish_type = 'С отделкой'
        except:
            finish_type = ''


        try:
            room_count = i['layout_rooms_amount']
        except:
            room_count = ''
        try:
            flat_number = i['title']
        except:
            flat_number = ''
        try:
            area = float(i['layout_square'])
        except:
            area = ''
        if not area:
            continue
        try:
            old_price = int(i['price_old'])
        except:
            old_price = ''
        try:
            price = int(i['price'])
        except:
            price = ''
        try:
            floor = i['floor']
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

    break
    data['nextPostIndex'] = str(int(data['nextPostIndex']) + 1)
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

