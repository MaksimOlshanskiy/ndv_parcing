# отдельно с отделкой и без, в 'params[finishing]'

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup


cookies = {
    '_ym_uid': '1742827436146654235',
    '_ym_d': '1742827436',
    '_ct': '2900000000083277762',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'cookiesApply': '1',
    'cted': 'modId%3D46cqnlyv%3Bya_client_id%3D1742827436146654235%7CmodId%3Dli0xsjag%3Bya_client_id%3D1742827436146654235',
    '_ct_ids': '46cqnlyv%3A61236%3A228189572_li0xsjag%3A70248%3A126686309',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'city': 'moscow',
    '_ct_session_id': '126686309',
    '_ct_site_id': '70248',
    'call_s': '___46cqnlyv.1743165798.228189572.335118:959616|li0xsjag.1743165799.126686309.427067:1195816|2___',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://unikey.space',
    'Referer': 'https://unikey.space/category/?complex=2325',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1742827436146654235; _ym_d=1742827436; _ct=2900000000083277762; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; cookiesApply=1; cted=modId%3D46cqnlyv%3Bya_client_id%3D1742827436146654235%7CmodId%3Dli0xsjag%3Bya_client_id%3D1742827436146654235; _ct_ids=46cqnlyv%3A61236%3A228189572_li0xsjag%3A70248%3A126686309; _ym_isad=2; _ym_visorc=w; city=moscow; _ct_session_id=126686309; _ct_site_id=70248; call_s=___46cqnlyv.1743165798.228189572.335118:959616|li0xsjag.1743165799.126686309.427067:1195816|2___',
}

data = {
    'action': 'get_more_apartments',
    'page': '1',
    'params[complex]': '2325',
    'params[finishing]': '0',
}


flats = []
flats_nums = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for i in range(2):
    print(flats_nums)
    if i == 0:
        data['params[finishing]'] = '1'
    else:
        data['params[finishing]'] = '0'


    while True:

        response = requests.post('https://unikey.space/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)

        soup = BeautifulSoup(response.text, 'html.parser')
        flats_soup = soup.find_all('li', class_="layouts-parameters__item")
        for flat in flats_soup:

            if int(flat.find('div', class_='layout-card__info-wrp').text.split()[9]) in flats_nums:
                    continue





            # print(flat.text.strip().split())
            price_div = soup.find('div', class_='layout-card__price')

            url = ''
            developer = "Юникей"
            project = 'Новые смыслы'
            korpus = flat.find('div', class_='layout-card__info-wrp').text.split()[4]
            type = 'Квартира'
            if data['params[finishing]'] == '0':
                finish_type = 'Без отделки'
            else:
                finish_type = 'С отделкой'
            if flat.find('span', class_='layout-card__count').text.split()[0] == 'Студия':
                room_count = 0
            else:
                room_count = extract_digits_or_original(flat.find('span', class_='layout-card__count').text.split()[0])
            try:
                area = float(flat.find('div', class_='layout-card__info-wrp').text.split()[11])
            except:
                area = ''
            try:
                old_price = extract_digits_or_original(price_div.find('span', class_='layout-card__title').get_text(strip=True))
            except:
                old_price = ''
            try:
                price = extract_digits_or_original(price_div.find('span', class_='layout-card__count').find('span', class_='is-red').get_text(
                strip=True))
            except:
                price = extract_digits_or_original(price_div.find('span', class_='layout-card__count').get_text(
                strip=True))
            section = ''
            try:
                floor = int(flat.find('div', class_='layout-card__info-wrp').text.split()[6].split('/')[0])
            except:
                floor = ''
            flat_number = int(flat.find('div', class_='layout-card__info-wrp').text.split()[9])

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
            flats_nums.append(flat_number)

        if not flats_soup:
            break
        data['page'] = str(int(data['page']) + 1)
        sleep_time = random.uniform(1, 3)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Юникей"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{date}_Без.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

