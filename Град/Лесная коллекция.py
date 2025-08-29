import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from functions import save_flats_to_excel
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


cookies = {
    'ced': 'iogu7qg4r9p33u3bhr1lohcus4tmmavd',
    '_ym_uid': '1756294013692050523',
    '_ym_d': '1756294013',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cookie': 'yes',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary0wLME6EGEy1Kk0PM',
    'Origin': 'https://lyesnaya.ru',
    'Referer': 'https://lyesnaya.ru/catalog/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ced=iogu7qg4r9p33u3bhr1lohcus4tmmavd; _ym_uid=1756294013692050523; _ym_d=1756294013; _ym_isad=2; _ym_visorc=w; cookie=yes',
}

params = {
    'nc_ctpl': '228',
    'isNaked': '1',
}

files = [
    ('building[]', (None, '1')),
    ('building[]', (None, '2')),
    ('building[]', (None, '3')),
    ('building[]', (None, '4')),
    ('building[]', (None, '5')),
    ('rooms[]', (None, '1')),
    ('rooms[]', (None, '2')),
    ('rooms[]', (None, '3')),
    ('price-from', (None, '8')),
    ('price-to', (None, '25')),
    ('square-from', (None, '28')),
    ('square-to', (None, '80')),
    ('sorting', (None, '1')),
    ('more', (None, '20')),
]



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


driver = webdriver.Chrome()
driver.get("https://lyesnaya.ru/catalog/")

wait = WebDriverWait(driver, 5)  # небольшое ожидание

while True:
    try:
        # ждём появления кнопки
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-more-btn]")))

        try:
            # пробуем обычный клик
            button.click()
        except:
            # если перекрыта элементом, скроллим и кликаем через JS
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            driver.execute_script("arguments[0].click();", button)

    except TimeoutException:
        print("Кнопка 'Показать еще' больше не найдена. Выход из цикла.")
        break

driver.quit()


page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all('a', class_="flat-card catalog-view__item")
for i in flats_soup:

    url = ''
    date = datetime.date.today()
    project = ("Обручева 30")
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
    korpus = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    finish_type = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    room_count = ''
    area = ''
    price_per_metr = ''
    old_price = i.find('span', class_='flat-card__price-current').text.strip().replace(' ', '').replace('₽', '')
    discount = ''
    price_per_metr_new = ''
    price = ''
    section = ''
    floor = ''
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







save_flats_to_excel(flats, project, developer)