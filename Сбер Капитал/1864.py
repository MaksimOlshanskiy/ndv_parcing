import datetime
import time
from re import findall
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver

from functions import save_flats_to_excel

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
    old_price = int(float(f.select_one('div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_tc.tc').text.replace(' ', ''))*1000000)
    room_count = f.select_one("div.SearchDesktopResultsRow__cell.SearchDesktopResultsRow__cell_rc.rc").text
    discount = ''
    price_per_metr_new = ''
    price = ''
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


save_flats_to_excel(flats, project, developer)


