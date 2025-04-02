import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from datetime import datetime
import requests

cookies = {
    'anonymousAccountID': '88c2ef35-d9a8-43c8-a135-ec606a9da42f',
    'businessLocationAlias': 'moscow',
    '_ym_uid': '1742813750390448864',
    '_ym_d': '1742813750',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-public_key=ccb902671fc9e0392dd67d04b2a41234,sentry-trace_id=1e0199800d884814a1beca5d1194eb27',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://dombook.plus/zhilye-kompleksy/very-na-mikluho-maklaya-b663fd',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '1e0199800d884814a1beca5d1194eb27-8bdfdddf4bb5ecdf',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'anonymousAccountID=88c2ef35-d9a8-43c8-a135-ec606a9da42f; businessLocationAlias=moscow; _ym_uid=1742813750390448864; _ym_d=1742813750; _ym_isad=2; _ym_visorc=w',
}

params = {
    'pagination[per_page]': '10',
    'pagination[page]': '1',
    'filters[rooms][0]': 'studio',
    'project_id': '80c85ea4-bf01-4f9a-b879-6e1c24cabecd',
    'lot_type_alias': 'kvartira',
}

rooms_count_list = ['studio', '1_room', '2_room', '3_room', '4_and_more_room']
rooms_count_dict = {'studio': 0, '1_room': 1, '2_room': 2, '3_room': 3, '4_and_more_room': 4}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



for rooms in rooms_count_list:
    params['filters[rooms][0]'] = rooms
    params["pagination[page]"] = '1'

    while True:

        response = requests.get('https://dombook.plus/api/v1/project/get.lots', params=params, cookies=cookies, headers=headers)

        print(response.status_code)
        items = response.json()['content']['lots']

        for i in items:

            url = ''


            date = datetime.now()
            project = i['project']['name']


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
            developer = "Айгрин"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i['building_name']
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Апартаменты'
            finish_type = ''
            room_count = rooms_count_dict.get(rooms)

            area = float(i['square'])

            price_per_metr = ''
            if i['discount_price'] is not None:
                old_price = i['price']
            else:
                old_price = ''
            discount = ''
            price_per_metr_new = ''
            if i["discount_price"] is not None:
                price = i["discount_price"]
            else:
                price = i["price"]
            section = ''
            floor = i['floor']
            flat_number = ''



            print(
                f"{project}, {url}, отделка: {finish_type}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                      klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)
        if not items:
            break
        params["pagination[page]"] = str(int(params["pagination[page]"]) + 1)
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

current_date = datetime.now().date()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Домбук"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)