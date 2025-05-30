import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'tmr_lvid': 'b53f46415e692bb8064718745f7e2f21',
    'tmr_lvidTS': '1745569317490',
    '_ym_uid': '1745569318420487600',
    '_ym_d': '1748328460',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': '8as82fa1%3A55785%3A455366553',
    '_ct_session_id': '455366553',
    '_ct_site_id': '55785',
    'call_s': '___8as82fa1.1748330259.455366553.284733:854358|2___',
    '_ct': '2300000000297765188',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_ga': 'GA1.1.139086639.1748328461',
    'domain_sid': '7iLIzStIet7l7x7kwDvlv%3A1748328461449',
    'cted': 'modId%3D8as82fa1%3Bya_client_id%3D1745569318420487600%3Bclient_id%3D139086639.1748328461',
    'tmr_detect': '0%7C1748328462715',
    '_ga_1ZPY9G3X05': 'GS2.1.s1748328460$o1$g1$t1748328545$j0$l0$h0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'If-None-Match': '"71625-kzRbropFQVZAJ00UAfhcSGpnie0"',
    'Referer': 'https://aist-residence.ru/apartamenty',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'tmr_lvid=b53f46415e692bb8064718745f7e2f21; tmr_lvidTS=1745569317490; _ym_uid=1745569318420487600; _ym_d=1748328460; _ym_isad=2; _ym_visorc=w; _ct_ids=8as82fa1%3A55785%3A455366553; _ct_session_id=455366553; _ct_site_id=55785; call_s=___8as82fa1.1748330259.455366553.284733:854358|2___; _ct=2300000000297765188; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _ga=GA1.1.139086639.1748328461; domain_sid=7iLIzStIet7l7x7kwDvlv%3A1748328461449; cted=modId%3D8as82fa1%3Bya_client_id%3D1745569318420487600%3Bclient_id%3D139086639.1748328461; tmr_detect=0%7C1748328462715; _ga_1ZPY9G3X05=GS2.1.s1748328460$o1$g1$t1748328545$j0$l0$h0',
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


response = requests.get(
    'https://aist-residence.ru/_next/data/XgsqSoht3GvtWX5Po3V1p/apartamenty.json',
    cookies=cookies,
    headers=headers,
)
print(response.status_code)
items = response.json()['pageProps']['data']['data']

for i in items:

    if i['status'] != "AVAILABLE":
        continue

    url = ''
    date = datetime.date.today()
    project = "Аист резиденс"
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
    developer = "Монарх"
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
    type = 'Апартаменты'
    finish_type = 'Без отделки'
    room_count = i['rooms']
    area = i["area"]
    price_per_metr = ''
    old_price = ''
    discount = ''
    price_per_metr_new = ''
    price = float(i["price"])
    section = i['section']
    floor = i["floor"]
    flat_number = i['number']

    print(
        f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
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

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
