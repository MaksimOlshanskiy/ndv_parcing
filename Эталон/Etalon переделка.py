import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from functions import save_flats_to_excel
import json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

"""
Скрипт очень медленный, часа на три, но рабочий, нужно менять number_of_flats на верное количество квартир с сайта
"""

number_of_flats = 665

cookies = {
    'PHPSESSID': 'kLhpYpDU4pBf5qEWlalRohUJEv3FHoQh',
    'scbsid_old': '2750244825',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic',
    'origin': 'https://etalongroup.ru',
    'priority': 'u=1, i',
    'referer': 'https://etalongroup.ru/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

pagination = {
    "haveItem": True,
    "page": 1,
    "object": None,
    "offset": 0,
    "limit": 9
}




# Параметры пагинации

page_number = 1

have_item = True  # Флаг наличия данных


flats = []
count = 1

retry_strategy = Retry(
    total=5,
    backoff_factor=2,  # 2s, 4s, 8s...
    status_forcelist=[500, 502, 503, 504]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)
session.mount("https://", adapter)

while pagination['offset'] < number_of_flats:

    params = {
        "pagination": json.dumps(pagination),
        "getAuctionSlider": "false"
    }

    print(params)

    url = f'https://newsite.etalongroup.ru/api/filter/msk/flat/list/'

    response = session.get(url, cookies=cookies, headers=headers, params=params)
    print(response.status_code)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        break

    try:
        items = response.json()['data']['itemList']


        if not items:
            print("Данные закончились, выхожу из цикла.")
            break

        options = Options()
        options.add_argument("--headless=new")
        options.page_load_strategy = "eager"

        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

        for i in items:
            project = i['objectTitle']
            date = datetime.date.today()
            status = ''
            developer = 'Эталон'
            okrug = ''
            district = ''
            room_count = ''
            type = i["title"].split()

            if type[0] == 'Студия':
                room_count = 'Студия'
            else:
                if type[0] == 'Однокомнатная':
                    room_count = 1
                elif type[0] == 'Двухкомнатная':
                    room_count = 2
                elif type[0] == 'Трехкомнатная':
                    room_count = 3
                elif type[0] == 'Четырехкомнатная':
                    room_count = 4
                elif type[0] == 'Пятикомнатная':
                    room_count = 5

            type = 'Квартира'
            finish_type = 'Без отделки'
            area = i["area"]
            old_price = i["price"]
            discount = ''
            price = i["priceTotal"]
            section = ''
            floor = i["floor"]
            flat_number = ''
            srok_sdachi_old = i['deliveryName']

            flat_url = i.get("link", "")
            driver.get(flat_url)

            try:
                korpus = driver.find_element(
                    By.XPATH,
                    "//div[p[text()='Корпус']]/p[last()]"
                ).text
            except:
                korpus = ''



            if old_price == price:
                price = None

            print(
                f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, okrug,
                      district, '', '', korpus, '', '', '', srok_sdachi_old, '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', price, section, floor, flat_number]
            flats.append(result)

            count += 1
        driver.quit()
        pagination['offset'] = response.json()['data']['pagination']['offset']
        pagination['page'] = response.json()['data']['pagination']['page']
        pagination['limit'] = response.json()['data']['pagination']['limit']
        print(pagination)

        page_number += 1

    except Exception as e:
        print(f"Ошибка обработки JSON: {e}")
        continue

save_flats_to_excel(flats, 'all', developer)
