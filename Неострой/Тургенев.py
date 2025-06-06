import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from datetime import datetime


import requests

import requests

cookies = {
    'roistat_visit': '737803',
    'roistat_first_visit': '737803',
    'roistat_visit_cookie_expire': '1209600',
    '_ym_uid': '1742905226910671713',
    '_ym_d': '1742905226',
    'tmr_lvid': 'c5be22bbe96ea033210c29015de5a266',
    'tmr_lvidTS': '1742905225780',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit',
    'cted': 'modId%3D534idqi1%3Bclient_id%3D1321169503.1742905226%3Bya_client_id%3D1742905226910671713',
    '_gid': 'GA1.2.1867998545.1742905226',
    '_ct_ids': '534idqi1%3A34963%3A839105841',
    '_ct_session_id': '839105841',
    '_ct_site_id': '34963',
    '_ct': '1300000000518946007',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '___dc': '4f7545a1-24c9-4ab2-b89e-7f0a9765cc09',
    'domain_sid': 'fOH5Ci0Bny9vRhUWNWFtQ%3A1742905227952',
    '_ga': 'GA1.2.1321169503.1742905226',
    'call_s': '___534idqi1.1742907076.839105841.172513:530192|2___',
    'tmr_detect': '0%7C1742905278076',
    '_ga_G106EZYGX3': 'GS1.1.1742905226.1.1.1742905429.60.0.0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://turgenev-dom.ru/select/params',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'roistat_visit=737803; roistat_first_visit=737803; roistat_visit_cookie_expire=1209600; _ym_uid=1742905226910671713; _ym_d=1742905226; tmr_lvid=c5be22bbe96ea033210c29015de5a266; tmr_lvidTS=1742905225780; _ym_isad=2; _ym_visorc=w; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit; cted=modId%3D534idqi1%3Bclient_id%3D1321169503.1742905226%3Bya_client_id%3D1742905226910671713; _gid=GA1.2.1867998545.1742905226; _ct_ids=534idqi1%3A34963%3A839105841; _ct_session_id=839105841; _ct_site_id=34963; _ct=1300000000518946007; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; ___dc=4f7545a1-24c9-4ab2-b89e-7f0a9765cc09; domain_sid=fOH5Ci0Bny9vRhUWNWFtQ%3A1742905227952; _ga=GA1.2.1321169503.1742905226; call_s=___534idqi1.1742907076.839105841.172513:530192|2___; tmr_detect=0%7C1742905278076; _ga_G106EZYGX3=GS1.1.1742905226.1.1.1742905429.60.0.0',
}

params = {
    'page': '1',
    'lang': 'ru',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s




while True:

    response = requests.get('https://turgenev-dom.ru/backend/api/apartments', params=params, cookies=cookies,
                            headers=headers)
    print(response.status_code)
    items = response.json()['result']['items']

    for i in items:

        url = ''


        date = datetime.now()
        project = "Тургенев"


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
        developer = "Неострой"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = 'С отделкой'
        room_count = int(i['rooms'])

        area = float(i['area'])

        price_per_metr = ''
        old_price = ''
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(i["price"])
        except:
            price = i["price"]
        section = i['section']
        floor = i['floor']
        flat_number = ''



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
    params["page"] = int(params["page"]) + 1


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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Неострой"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)