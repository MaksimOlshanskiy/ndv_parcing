import datetime
import time
from re import findall

import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from functions import save_flats_to_excel

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

web_site = f'https://highlife.ru/search?square=23,347&finishing=bez_otdelki,white_box,dizaynerskaya'
driver = webdriver.Chrome()
driver.get(url=web_site)
count = 0
while True:
    try:


        wait = WebDriverWait(driver, 7)
        # Ждём появления кнопки "Показать ещё"
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button span")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # ждём подгрузку контента

        button.click()
        print("Кликнули 'Показать ещё'")
        print("_______________________________________")


    except TimeoutException:
        print("Кнопки больше нет → выходим из цикла")
        break

page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all('div', class_="flat")

for f in flats_soup:
    try:
        flat_params = f.find('div', class_="flat-info").text.split(' ')
        print(flat_params)
    except AttributeError:
        continue

    url = ''
    date = datetime.date.today()
    project = "High Life"
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
    developer = "Пионер"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = flat_params[1][1]
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'

    finish_type = f.find('div', class_="flat-params").text.strip().replace('Отделка: ', '').replace('дизайнерская', 'С отделкой').replace('без отделки', 'Без отделки').replace('Выдаем ключи', '')
    if 'Вид' in finish_type:
        finish_type = finish_type.split("Вид")[0]
    if 'Сдаем' in finish_type:
        finish_type = finish_type.split("Сдаем")[0]
    area = float(flat_params[2].replace('комната', '').replace('комнаты', '').replace('комнат', '').replace(',', '.'))
    price_per_metr = ''
    try:
        old_price = int(f.find('div', class_="flat-price-old").text.replace(' ', ''))
        price = int(f.find('div', class_="flat-price-cur").text.replace(' ', ''))
    except:
        old_price = int(f.find('div', class_="flat-price-cur").text.replace(' ', ''))
        price = ''
    room_count = flat_params[1][2]
    discount = ''
    price_per_metr_new = ''

    section = ''
    floor = ''
    flat_number = ''
    count += 1
    print(
        f"{count} | {project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
              konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)


save_flats_to_excel(flats, project, developer)


