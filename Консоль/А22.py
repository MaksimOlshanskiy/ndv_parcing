import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functions import save_flats_to_excel
from selenium.common.exceptions import TimeoutException



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

web_site = f'https://a-22.ru/kvartiry/'
driver = webdriver.Chrome()
driver.get(url=web_site)

while True:

    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    soup = BeautifulSoup(page_content, 'html.parser')
    flats_soup = soup.find_all('div', class_="kvartiry__item")

    for f in flats_soup:

        url = ''
        date = datetime.date.today()
        project = "А22"
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
        developer = "Консоль"
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
        type = 'Квартиры'
        finish_type = "Без отделки"
        area = float(f.find('div', class_="kvartiry__props mt-1 p4 d-flex align-items-center flex-wrap").text.split()[2])
        price_per_metr = ''
        old_price = int(f.find('div', class_="kvartiry__price").text.strip().replace(' ', '').replace('₽', ''))
        room_count = f.find('div', class_="kvartiry__title h5 mb-0").text.split()[0]
        if room_count == 'Однокомнатная':
            room_count = 1
        elif room_count == 'Двухкомнатная':
            room_count = 2
        elif room_count == 'Трехкомнатная':
            room_count = 3
        elif room_count == 'Квартира-студия':
            room_count = 0
        else:
            room_count = f.find('div', class_="kvartiry__title h5 mb-0").text.split()[0]
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = ''
        flat_number = ''

        print(
            f"{project}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'body > main > div > div.kvartiry__catalog.pt-4.pb-4 > div:nth-child(4) > div > div > div.pagination.d-flex.align-items-center.justify-content-center.flex-wrap.align-self-end > a.pagination-item.d-flex.align-items-center.justify-content-center.flex-shrink-0.text-decoration-none.to-end.default')
            )
        )

        # Кликаем
        button.click()
        print("Переходим на следующую страницу")
    except:
        print("Кнопка перехода отсутствует. Завершаем цикл.")
        break



save_flats_to_excel(flats, project, developer)


