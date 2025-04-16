import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    '_ym_uid': '1743434549565008431',
    '_ym_d': '1743434549',
    '_ym_isad': '2',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ct_site_id': '57297',
    '_ct': '2300000000278829268',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ga': 'GA1.1.200739408.1743434556',
    'cted': 'modId%3Drwlsx7v3%3Bya_client_id%3D1743434549565008431%3Bclient_id%3D200739408.1743434556',
    'PHPSESSID': 'g0B7i1Q1M4nkeRK46Ca9P2A1er2Z6oQI',
    '_ym_visorc': 'w',
    '_ct_ids': 'rwlsx7v3%3A57297%3A428847818',
    '_ct_session_id': '428847818',
    'call_s': '___rwlsx7v3.1743493350.428847818.302835:873454.302836:873285|2___',
    '_ga_C9SQLMNF29': 'GS1.1.1743491557.3.0.1743491632.0.0.0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Referer': 'https://rusich.group/catalog/?view=grid',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1743434549565008431; _ym_d=1743434549; _ym_isad=2; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ct_site_id=57297; _ct=2300000000278829268; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ga=GA1.1.200739408.1743434556; cted=modId%3Drwlsx7v3%3Bya_client_id%3D1743434549565008431%3Bclient_id%3D200739408.1743434556; PHPSESSID=g0B7i1Q1M4nkeRK46Ca9P2A1er2Z6oQI; _ym_visorc=w; _ct_ids=rwlsx7v3%3A57297%3A428847818; _ct_session_id=428847818; call_s=___rwlsx7v3.1743493350.428847818.302835:873454.302836:873285|2___; _ga_C9SQLMNF29=GS1.1.1743491557.3.0.1743491632.0.0.0',
}

params = {
    'action': 'getApartments',
    'max_price': '',
    'min_price': '',
    'min_square': '',
    'max_square': '',
    'min_floor': '',
    'max_floor': '',
    'discount': '',
    'master_bedroom': '',
    'balcony': '',
    'rooms': '',
    'finish': '',
    'deadline': '',
    'corpus': '',
    'project': '',
    'min_monthly_payment': '',
    'max_monthly_payment': '',
    'sort': '',
    'order': '',
    'view': 'grid',
    'page': '1',
    'limit': '1000',
}



flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://rusich.group/ajax/catalog-filter.php', params=params, cookies=cookies, headers=headers)

    items = response.json()['result']['apartments']


    for i in items:

        url = f'https://rusich.group/{i["DETAIL_PAGE_URL"]}'
        developer = "Русич"
        project = i['PROJECT'].replace('РУСИЧ ', '')
        korpus = extract_digits_or_original(i["CORPUS"])
        type = 'Квартира'
        if i['FINISH']['value'] == 'White Box':
            finish_type = 'Предчистовая'
        else:
            finish_type = i['FINISH']['value']
        if i['NUMBER_OF_ROOMS'] == 'С-1':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i['NUMBER_OF_ROOMS'])
        try:
            area = float(i['SQUARE'])
        except:
            area = ''
        try:
            old_price = int(i['OLD_PRICE'])
        except:
            old_price = ''
        try:
            price = int(i['PRICE'])
        except:
            price = ''
        section = int(i['SECTION'])
        try:
            floor = i['FLOOR']
        except:
            floor = ''
        flat_number = ''

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



# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Русич"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

