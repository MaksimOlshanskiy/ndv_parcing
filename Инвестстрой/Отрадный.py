import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()

cookies = {
    'PHPSESSID': '1j7f30ldtelgl88i1ihm3gl0a6',
    '_ym_uid': '1743776661403332867',
    '_ym_d': '1743776661',
    '_ym_isad': '2',
    '_cmg_csstqQXud': '1743776663',
    '_comagic_idqQXud': '10090297548.14299687238.1743776661',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://jk-otradny.ru',
    'priority': 'u=1, i',
    'referer': 'https://jk-otradny.ru/room/page/6/?slg=post&mdf_cat=7&page_mdf=0e73715f4716d2f56ed75357a742be9f&mdf_page_num=6',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=1j7f30ldtelgl88i1ihm3gl0a6; _ym_uid=1743776661403332867; _ym_d=1743776661; _ym_isad=2; _cmg_csstqQXud=1743776663; _comagic_idqQXud=10090297548.14299687238.1743776661',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

counter = 1

while True:

    web_site = f'https://jk-otradny.ru/room/page/{counter}/?slg=post&mdf_cat=7&page_mdf=0e73715f4716d2f56ed75357a742be9f'

    response = requests.get(web_site,
        cookies=cookies, headers=headers)

    print(response.status_code)
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")

    # все карточки квартир
    flats_soup = soup.find(class_="parameter_tab").find_all('a')

    for i in flats_soup:

        param = i.text.split()
        if len(param) < 5:
            continue

        url = ''
        date = datetime.date.today()
        project = "Отрадный"
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
        developer = "Инвестстрой"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = int(param[1])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'

        if param[3] == 'Нет':
            finish_type = 'Без отделки'
        elif param[3] == 'Да':
            finish_type = 'С отделкой'

        room_count = int(param[6])

        area = float(param[7])
        price_per_metr = ''
        old_price = ''

        discount = ''
        price_per_metr_new = ''
        price = int(' '.join(param[8:]).replace(' ', ''))
        section = int(param[2])
        floor = int(param[5])
        flat_number = param[0]

        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    counter += 1

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