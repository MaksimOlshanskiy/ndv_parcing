import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup


import requests

import requests

cookies = {
    'PHPSESSID': 'VKJGPKdun0aKIf2KD1Mdvf8mz7Ro5WoB',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ym_uid': '174357795115798414',
    '_ym_d': '1743577951',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cookieAccepted': 'true',
    'lastClickedComplex': '%5B%5D',
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://atlantdevelopment.ru',
    'Referer': 'https://atlantdevelopment.ru/flats/complex_name-is-%D0%B6%D0%BA%20%C2%AB%D0%B2%D0%BD%D1%83%D0%BA%D0%BE%D0%B2%D0%BE%20%D0%BF%D0%B0%D1%80%D0%BA%C2%BB-or-%D0%BA%D0%B4%20%C2%AB%D0%BC%D0%B0%D0%BB%D1%8B%D0%B5%20%D0%B2%D0%B5%D1%88%D0%BA%D0%B8%C2%BB-or-%D0%BA%D0%B4%20%C2%AB%D0%BD%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%B2%D0%B0%D1%88%D1%83%D1%82%D0%B8%D0%BD%D0%BE%C2%BB-or-%D0%B6%D0%BA%20%C2%AB%D0%B4%D0%BE%D0%BC%20%D0%BD%D0%B0%20%D0%BF%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D1%81%D0%BA%D0%BE%D0%B9%C2%BB/type-is-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%8B/apply/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'PHPSESSID=VKJGPKdun0aKIf2KD1Mdvf8mz7Ro5WoB; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ym_uid=174357795115798414; _ym_d=1743577951; _ym_isad=2; _ym_visorc=w; cookieAccepted=true; lastClickedComplex=%5B%5D',
}

data = {
    'page': '1',
    'FILTER_ITEMS_RESULT[arrFilter][PROPERTY_170][]': [
        'AVAILABLE',
        'BOOKED',
    ],
    'FILTER_ITEMS_RESULT[arrFilter][=PROPERTY_2][]': [
        'ЖК «Внуково Парк»',
        'КД «Новое Вашутино»',
    ],
    'FILTER_ITEMS_RESULT[COUNT]': '55',
    'FILTER_ITEMS_RESULT[NEW_URL]': '',
}








flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:

    response = requests.post(
        'https://atlantdevelopment.ru/local/templates/.default/components/bitrix/catalog/flats/filter_catalog_result.php',
        cookies=cookies,
        headers=headers,
        data=data,
    )
    print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')
    flats_soup = soup.find_all('div', class_= 'catalogCard')


    for i in flats_soup:
        url = ''

        date = datetime.date.today()
        project = i.find('span', class_= 'catalogCard__text').text.replace('«', '').replace('»', '').replace('КД ', '').replace('ЖК ', '')

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
        developer = "Атлант"
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
        elements = i.find_all('span', class_='badge__text')
        finish_type = elements[1].text.replace(' отделка', '')
        srok_sdachi = ''

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if project == 'Новое Вашутино':
            type = 'Апартаменты'
        else:
            type = 'Квартира'
        if extract_digits_or_original(i.find('span', class_= 'catalogCard__smallText').text.split()[0]) == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('span', class_= 'catalogCard__smallText').text.split()[0])
        area = float(i.find('span', class_= 'catalogCard__bigText').text.replace(' м2', ''))
        price_per_metr = ''
        old_price = int(i.find('span', class_= 'catalogCard__smallText catalogCard__smallText-old-price').text.replace(' ', '').replace('₽', ''))

        discount = ''
        price_per_metr_new = ''
        price = int(i.find('span', class_= 'catalogCard__bigText textRed').text.replace(' ', '').replace('₽', ''))
        section = ''
        try:
            floor = int(i.find('div', class_= ['catalogCard__textCol catalogCard__textCol--right']).text.replace(' этаж', ''))
        except ValueError:
            floor = int(i.find('div', class_= ['catalogCard__textCol catalogCard__textCol--right']).text.split()[0])
        flat_number = ''

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

    if not flats_soup:
        break
    data['page'] = str(int(data['page']) +1)

    print('--------------------------------------------------------------------------------')

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
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)