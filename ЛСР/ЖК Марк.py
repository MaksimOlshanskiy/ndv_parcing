import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from ЖК_WAVE import cookies, headers
import requests

cookies = cookies
headers = headers

data = {
    'last_delivery': '30',
    'price[min]': '1',
    'price[max]': '999',
    'price_range[min]': '1',
    'price_range[max]': '999',
    'obj[]': ['223', '223'],
    'area[min]': '1',
    'area[max]': '999',
    'area_range[min]': '1',
    'area_range[max]': '999',
    'floor[min]': '1',
    'floor[max]': '99',
    'floor_range[min]': '1',
    'floor_range[max]': '99',
    'ob[page]': '1',
    'ob[sort]': 'price',
    'ob[order]': 'asc',
    'group[t]': 'false',
    'ob[id]': '223',
    'object': '223',
    'a': 'types',
    'ok': 'L9BkJyIGWZ1fC1lLQdKcu325SphK4pYG'
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://www.lsr.ru/ajax/search/msk/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['html']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_="listingCard listingCard--isFlat")
    for i in flats_soup:

        url = ''

        date = datetime.date.today()
        project = "ЖК Марк"

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
        developer = "ЛСР"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        all_tags = i.find_all('div', class_='tag tag--isSmall')
        korpus = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = all_tags[0].text.strip()
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'

        if all_tags[2].text.strip() == "С меблировкой":
            finish_type = f"{all_tags[1].text.strip()}, С меблировкой"
        else:
            finish_type = all_tags[1].text.strip()
        if i.find('span', class_= "h4").text.strip().split()[0] == "Студия":
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('span', class_= "h4").text.strip().split()[0])
        area = float(i.find('span', class_='h4 isColorSilverChalice isTextNoWrap').text.strip().split(' ')[0])
        price_per_metr = ''
        old_price = ''

        discount = ''
        price_per_metr_new = ''
        price = extract_digits_or_original(i.find('span', class_= 'h4 isHiddenInGrid').text)
        section = ''
        try:
            floor = int(i.find('div', class_= 'listingCard__label').text.strip().split()[2])
        except:
            floor = i.find('div', class_='listingCard__label').text.strip().split()[2]
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

    print('--------------------------------------------------------------------------------')

    data['ob[page]'] = str(int(data['ob[page]']) + 1)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ЛСР"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)