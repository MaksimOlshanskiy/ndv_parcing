import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    '_ym_uid': '174358513932310668',
    '_ym_d': '1743585139',
    'XSRF-TOKEN': 'eyJpdiI6IkRzeEU4bU5rUXErK080cGxab2ZybVE9PSIsInZhbHVlIjoiRU1SS2pVOERmMzN3TktZSGxYTXgvZXVHMURFSmVqdW5LUHZaUE44WXVpYmNZdm4xdGdlV2ZjSUN4Y1dmNTBXRmg1T2l5L09YcHF0SlJkbUhrY2orcktqUDhtakdDeEk1bzZkNDFaMzdqclE2WEg3dm1sRVFXc29wTG9VREF0ZWQiLCJtYWMiOiJmNjQ2MzRiZTNmNTU1MDdjMmY1YzMxYzk1ZGI0NzQzNmZlZjAzYmJkNmNkNmVlNzFlYWY4YmUxODE3OGZjMGU1IiwidGFnIjoiIn0%3D',
    'aist_session': 'eyJpdiI6IkJUcVo4N01XRmFpN2s2WUh2dzVTZWc9PSIsInZhbHVlIjoic2NWTjFsMFlRWWZSZWZLWExUNnhVNGFvZU01aDdjZkZjK3pRL1Y1N21yc2hnWklKNm5LVHE4VEVqdXRuOTFhNnNGSHlRazg4dXN2QnJmc3VRN1JndkxCd1Bvdzl2ZTVFZGZVRlArSk5jb1QwelBLWDRPYmtuYnl1WG8rMjQzTzUiLCJtYWMiOiJjNTk1OWQxODEyYTI4NTgxOTNjZDcwYTBmZDhjNzIxOWVlYmU3YWZmMWE0YzU0ZmU1YjEzOWJlZTllYjFhMGQyIiwidGFnIjoiIn0%3D',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    # 'content-length': '0',
    'origin': 'https://aist-residence.com',
    'priority': 'u=1, i',
    'referer': 'https://aist-residence.com/ceni-i-planirovki?group_type%5B0%5D=1&group_type%5B1%5D=2&group_type%5B2%5D=3&group_type%5B3%5D=4&page=2',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-csrf-token': 'Mz2WyQdzfr0cJDjfYekNxfL5AmnH0FHh1SdM4smD',
    # 'cookie': '_ym_uid=174358513932310668; _ym_d=1743585139; XSRF-TOKEN=eyJpdiI6IkRzeEU4bU5rUXErK080cGxab2ZybVE9PSIsInZhbHVlIjoiRU1SS2pVOERmMzN3TktZSGxYTXgvZXVHMURFSmVqdW5LUHZaUE44WXVpYmNZdm4xdGdlV2ZjSUN4Y1dmNTBXRmg1T2l5L09YcHF0SlJkbUhrY2orcktqUDhtakdDeEk1bzZkNDFaMzdqclE2WEg3dm1sRVFXc29wTG9VREF0ZWQiLCJtYWMiOiJmNjQ2MzRiZTNmNTU1MDdjMmY1YzMxYzk1ZGI0NzQzNmZlZjAzYmJkNmNkNmVlNzFlYWY4YmUxODE3OGZjMGU1IiwidGFnIjoiIn0%3D; aist_session=eyJpdiI6IkJUcVo4N01XRmFpN2s2WUh2dzVTZWc9PSIsInZhbHVlIjoic2NWTjFsMFlRWWZSZWZLWExUNnhVNGFvZU01aDdjZkZjK3pRL1Y1N21yc2hnWklKNm5LVHE4VEVqdXRuOTFhNnNGSHlRazg4dXN2QnJmc3VRN1JndkxCd1Bvdzl2ZTVFZGZVRlArSk5jb1QwelBLWDRPYmtuYnl1WG8rMjQzTzUiLCJtYWMiOiJjNTk1OWQxODEyYTI4NTgxOTNjZDcwYTBmZDhjNzIxOWVlYmU3YWZmMWE0YzU0ZmU1YjEzOWJlZTllYjFhMGQyIiwidGFnIjoiIn0%3D; _ym_isad=2; _ym_visorc=w',
}

params = {
    'group_type[0]': '1',
    'group_type[1]': '2',
    'group_type[2]': '3',
    'group_type[3]': '4',
    'page': '1',
}



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    response = requests.post('https://aist-residence.com/api/v1/flats/kvartiry', params=params, cookies=cookies, headers=headers)
    items = response.json()['data']

    for i in items:

        url = i['link']

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
        korpus = extract_digits_or_original(i['corpus_name'])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Апартаменты'
        finish_type = 'Без отделки'
        if i['flat_type'] == 'Студии':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i['flat_type'])
        area = i["area_total"]
        price_per_metr = ''
        old_price = ''
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        section = ''
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
    params['page'] = str(int(params['page']) + 1)
    if not items:
        break
    print('------------------------------------------------------')


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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Монарх"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
