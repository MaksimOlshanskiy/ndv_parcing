import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup


import requests

cookies = {
    'PHPSESSID': 'J9wHIhcnTQBXjdHqe3SorHBl9TDjsyUP',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1743465540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    'roistat_visit': '102334',
    'roistat_first_visit': '102334',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit',
    '_ym_uid': '1743415929559311987',
    '_ym_d': '1743415929',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '___dc': 'a754551e-265e-4d6b-9f95-8a533f4aa9bc',
    '_cmg_csstZgRm6': '1743415931',
    '_comagic_idZgRm6': '10067765488.14273203563.1743415930',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'bx-ajax': 'true',
    'priority': 'u=1, i',
    'referer': 'https://1-ng.ru/catalog/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=J9wHIhcnTQBXjdHqe3SorHBl9TDjsyUP; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1743465540%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; roistat_visit=102334; roistat_first_visit=102334; roistat_visit_cookie_expire=1209600; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit; _ym_uid=1743415929559311987; _ym_d=1743415929; _ym_isad=2; _ym_visorc=w; ___dc=a754551e-265e-4d6b-9f95-8a533f4aa9bc; _cmg_csstZgRm6=1743415931; _comagic_idZgRm6=10067765488.14273203563.1743415930',
}

params = {
    'PAGEN_1': '1',
}
# catalogFilter_92=124380902



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:


    response = requests.get('https://1-ng.ru/catalog/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.text
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('tr')
    counter = 1
    for i in flats_soup:
        if counter == 1:
            counter += 1
            continue
        if i.text.split() == []:
            continue
        # print(i.text.split())

        flats = i.find_all('td')


        url = ''

        date = datetime.date.today()
        project = "Первый Нагатинский"

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
        developer = "Хант-Холдинг"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            korpus = ''
        except ValueError:
            korpus = ''
        konstruktiv = ''
        klass = ''
        finish_type = ''
        srok_sdachi = ''

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        room_count = i.text.split()[0]
        area = extract_digits_or_original(i.text.split()[7])
        price_per_metr = ''
        old_price = ''

        discount = ''
        price_per_metr_new = ''
        if len(i.text.split()) == 15:
            price = ''.join(i.text.split()[11:14])
        else:
            price = ''.join(i.text.split()[-4:-1])
        section = ''
        floor = i.text.split()[3]
        flat_number = extract_digits_or_original(i.text.split()[6])

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params['PAGEN_1'] = str(int(params['PAGEN_1']) + 1)
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

    page_counter += 1
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

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Хант-Холдинг"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)