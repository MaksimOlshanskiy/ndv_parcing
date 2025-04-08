import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

cookies = {
    'PHPSESSID': 'e27f2cc6bec9301a7ce623455c482aaa',
    '_ym_uid': '174402831689653693',
    '_ym_d': '1744028316',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ga': 'GA1.1.1236471003.1744028316',
    '_cmg_csst9xkMh': '1744028317',
    '_comagic_id9xkMh': '9267533637.13214484387.1744028316',
    '_ga_07RX8YLWVE': 'GS1.1.1744028316.1.1.1744028339.0.0.0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://xn----dtbjjb4adhjrlq.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----dtbjjb4adhjrlq.xn--p1ai/properties/property/object-43886',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=e27f2cc6bec9301a7ce623455c482aaa; _ym_uid=174402831689653693; _ym_d=1744028316; _ym_isad=2; _ym_visorc=w; _ga=GA1.1.1236471003.1744028316; _cmg_csst9xkMh=1744028317; _comagic_id9xkMh=9267533637.13214484387.1744028316; _ga_07RX8YLWVE=GS1.1.1744028316.1.1.1744028339.0.0.0',
}

data = {
    'type': 'property',
    'view': 'list',
    'sort': 'price_az',
    'facing': '0',
    'no_booked': '0',
    'stage': '0',
    'object': 'all',
    'house': 'all',
    'ready': 'all',
    'rooms[]': 'all',
    'price_min': '0',
    'price_max': '0',
    'floor_min': '0',
    'floor_max': '0',
    'size_min': '0',
    'size_max': '0',
    'page': '1',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post(
        'https://xn----dtbjjb4adhjrlq.xn--p1ai/properties/api/load_more',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    print(response.status_code)
    html = response.json()['code']
    soup = BeautifulSoup(html, 'html.parser')
   #  items = soup.find_all(class_= 'row sale')

    developer = ""
    project = ''

    flats_list = soup.find_all('a', class_='row')

    for item in flats_list:


        # Извлекаем данные

        url = ''
        developer = "Профи Инвест"
        project = item.find(class_='object_title').get_text(strip=True)
        korpus = item.find(class_='cell col_house').get_text(strip=True).replace('Корпус ', '')
        type = ''
        if item.find(class_='finishing_label'):
            finish_type = 'С отделкой'
        else:
            finish_type = 'Без отделки'
        if item.find(class_="rooms").get_text(strip=True) == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(item.find(class_="rooms").get_text(strip=True))
        try:
            area = float(item.find(class_= 'size').get_text(strip=True).replace(' м²', ''))
        except:
            area = ''
        try:
            old_price = int(item.find(class_= 'old_price').get_text(strip=True).replace(' ', '').replace('₽', ''))
        except:
            old_price = ''
        try:
            price = int(item.find(class_= 'price').get_text(strip=True).replace(' ', '').replace('₽', ''))
        except:
            price = ''
        section = ''
        try:
            floor = int(item.find(class_= 'cell col_floor').get_text(strip=True).split()[0])
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

    if not flats_list:
        break

    data['page'] = str(int(data['page']) + 1)



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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Профи Инвест"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

