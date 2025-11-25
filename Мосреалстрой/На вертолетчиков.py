import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions import save_flats_to_excel

cookies = {
    'PHPSESSID': '2bdc703dd1d617ce66711f8b282f7e22',
    '_ym_uid': '1742901130463078591',
    '_ym_d': '1753358089',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://ЖК На Вертолетчиков',
    'priority': 'u=1, i',
    'referer': 'https://xn----7sbhaoavqgppeu2ad4f.xn--p1ai/prices/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=2bdc703dd1d617ce66711f8b282f7e22; _ym_uid=1742901130463078591; _ym_d=1753358089; _ym_isad=2; _ym_visorc=w',
}

data = {
    'config[orderby]': 'price',
    'config[orderto]': 'asc',
    'config[page]': '1',
    'config[perpage]': '20',
    'config[return_type]': 'prices/flats',
    'filter': 'price_from=0.5&price_to=21.2&square_from=5&square_to=120&corpus=&layout=&floor_from=1&floor_to=18&sort-flats=on&term=&is_filter=yes&ac=1',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


web_site = f'https://xn----7sbhaoavqgppeu2ad4f.xn--p1ai/prices/flats#&orderby=price&orderto=asc&page=2&perpage=20&return_type=prices%2Fflats&price_from=0.5&price_to=21.2&square_from=5&square_to=120&corpus=&layout=&floor_from=1&floor_to=18&sort-flats=on&term=&is_filter=yes&ac=1'
driver = webdriver.Chrome()
driver.get(url=web_site)
time.sleep(2)
try:
    button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[3]/div/div/a")
    button.click()
    time.sleep(1)
except:
    pass
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all(class_="flat-item")

for i in flats_soup:
    try:

        url = ''
        date = datetime.now()
        project = "На вертолетчиков"
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
        developer = "Мосреалстрой"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            if '(' in i.text.split()[5]:
                korpus = ' '.join(i.text.split()[4:6])
            else:
                korpus = str(i.text.split()[4])
        except:
            korpus = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = 'С отделкой'
        room_count = i.find(class_='room-title').text.split('-')[0]
        try:
            area = float(i.text.split()[1])
        except:
            area = ''
        price_per_metr = ''
        try:
            old_price = ''
        except:
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        price = int(i.find(class_='price').text.strip().replace(' ', '').replace('₽', ''))
        section = ''
        floor = ''
        flat_number = ''
    except:
        print('Ошибка при обработке лота, пропускаем')
        print(i.text.split())
        continue

    print(
        f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

save_flats_to_excel(flats, project, developer)