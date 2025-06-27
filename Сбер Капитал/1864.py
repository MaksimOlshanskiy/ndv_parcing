import datetime
import time
from re import findall
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

web_site = f'https://r1864.ru/search'
driver = webdriver.Chrome()
driver.get(url=web_site)
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all('a', class_=["SearchDesktopResultsRow"])

for f in flats_soup:

    url = ''
    date = datetime.date.today()
    project = "1864 Резиденция"
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
    developer = "Сбер Капитал"
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
    finish_type = "Без отделки"
    area = float(f.select_one('div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_sq.sq').text)
    price_per_metr = ''
    old_price = ''
    room_count = f.select_one("div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_rc.rc").text
    discount = ''
    price_per_metr_new = ''
    price = int(float(f.select_one('div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_tc.tc').text.replace(' ', ''))*1000000)
    section = ''
    floor = f.select_one("div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_f.f").text
    flat_number = f.select_one("div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_n.n").text

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


