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

cookies = {
    'PHPSESSID': 'NVPjHM1uJDmzql7K1XAcJ76OpgI68j9i',
    'BITRIX_SM_TZ': 'Europe/Moscow',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    '_ga': 'GA1.2.131334750.1747895606',
    '_gid': 'GA1.2.1884430911.1747895606',
    '_ym_uid': '174789560624912562',
    '_ym_d': '1747895606',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'tmr_lvid': '88478ad87326eee1e890dae25d0baf65',
    'tmr_lvidTS': '1747895606362',
    '_fbp': 'fb.1.1747895606780.54129494801130691',
    '_cmg_csstYKFSc': '1747895607',
    '_comagic_idYKFSc': '10477872711.14723594926.1747895607',
    'domain_sid': '4rzTbpZJhOV9pXNM5uQhC%3A1747895608298',
    'metrium_cookie_closed': 'closed',
    '_ga_MJY58STQQE': 'GS2.2.s1747895606$o1$g1$t1747895830$j0$l0$h0',
    'tmr_detect': '0%7C1747895832752',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary9Id8dAoERuLLzyfB',
    'origin': 'https://www.metrium.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.metrium.ru/new-search/?flat=true&apartment=true&currency=rub&searchText=%D0%96%D0%9A%20U2&sort=ASC',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=NVPjHM1uJDmzql7K1XAcJ76OpgI68j9i; BITRIX_SM_TZ=Europe/Moscow; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; _ga=GA1.2.131334750.1747895606; _gid=GA1.2.1884430911.1747895606; _ym_uid=174789560624912562; _ym_d=1747895606; _ym_isad=2; _ym_visorc=w; tmr_lvid=88478ad87326eee1e890dae25d0baf65; tmr_lvidTS=1747895606362; _fbp=fb.1.1747895606780.54129494801130691; _cmg_csstYKFSc=1747895607; _comagic_idYKFSc=10477872711.14723594926.1747895607; domain_sid=4rzTbpZJhOV9pXNM5uQhC%3A1747895608298; metrium_cookie_closed=closed; _ga_MJY58STQQE=GS2.2.s1747895606$o1$g1$t1747895830$j0$l0$h0; tmr_detect=0%7C1747895832752',
}

files = {
    'flat': (None, 'true'),
    'apartment': (None, 'true'),
    'currency': (None, 'rub'),
    'pageNumber': (None, '1'),
    'searchText': (None, 'ЖК U2'),
    'sort': (None, 'ASC'),
    'action': (None, 'count'),
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

web_site = f'https://jk-vg.su/#flats'
driver = webdriver.Chrome()
driver.get(url=web_site)
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.find_all('div', class_="_wrapper_1p9bk_1")
for f in flats_soup:

    i = f.text
    print(i)

    url = ''
    date = datetime.date.today()
    project = "Времена года"
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
    developer = "СтартСК"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    finish_type = "Без отделки"
    area = float(f.find_all('span', class_='_valueLabel_bvxtf_24')[2].text.split(' м')[0])
    price_per_metr = ''
    try:
        old_price = int(f.find('s').get_text(strip=True).replace(',', '').replace(' млн.₽', '') + '0000')
    except:
        old_price = ''
    room_count = ''
    discount = ''
    price_per_metr_new = ''
    price = int(f.find('label').get_text(strip=True).replace(',', '').replace(' млн.₽', '') + '0000')
    section = ''
    floor = int(f.find_all('span', class_='_valueLabel_bvxtf_24')[0].text.split('/')[0])
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


