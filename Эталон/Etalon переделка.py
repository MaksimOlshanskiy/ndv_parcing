import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

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


# Параметры пагинации
offset = 0
page_number = 1
if page_number == 1:
    limit = 8
else:
    limit = 9
have_item = True  # Флаг наличия данных


flats = []
count = 1

while True:

    url = f'https://newsite.etalongroup.ru/api/filter/msk/flat/list/?groupByObject=false&onlyInSale=false&pagination=%7B%22haveItem%22:true,%22page%22:{page_number},%22object%22:null,%22offset%22:{offset},%22limit%22:{limit}%7D&getAuctionSlider=false'

    print(f"Загружаю объявления с offset={offset}...")



    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        break

    try:
        items = response.json()['data']['itemList']


        if not items:
            print("Данные закончились, выхожу из цикла.")
            break

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

            driver = webdriver.Chrome()
            driver.get(flat_url)

            korpus = driver.find_element(
                By.XPATH,
                "//div[p[text()='Корпус']]/p[last()]"
            ).text

            driver.quit()







            if old_price == price:
                price = None

            print(
                f"{count}, {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, okrug,
                      district, '', '', korpus, '', '', '', srok_sdachi_old, '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', price, section, floor, flat_number]
            flats.append(result)

            count += 1

        print(offset)
        if page_number == 1:
            offset += 8
        else:
            offset += 9
        print(offset)
        print(page_number)
        page_number += 1
        print(page_number)
    except Exception as e:
        print(f"Ошибка обработки JSON: {e}")
        break

save_flats_to_excel(flats, 'all', developer)
