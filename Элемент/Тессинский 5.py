import datetime
import random
from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

'''
Запустить и ничего не трогать
'''

flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


web_site = f'https://tessinskiy5.ru/select-parameters/'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()   # <<< разворачивает окно
driver.get(url=web_site)
time.sleep(9)

page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript

soup = BeautifulSoup(page_content, 'html.parser')
items = soup.find_all('div', class_=['property-line', 'property-line-show'])

print(len(items))

for i in items:

    url = ''
    developer = "Элемент"
    project = 'Тессинский 5'
    info = i.find_all('div', class_='col--info')

    korpus = info[0].text.strip()
    section = ''
    type = 'Квартиры'
    finish_type = 'Без отделки'
    room_count_finding = i.find_all('div', class_=['cards-item__info-item', 'cards-item__rooms'])
    room_count = i.find('div', class_='flat--info').text.split()[0]
    flat_number = ''
    try:
        area = float(i.find('div', class_='flat--info').text.split()[-2].replace(',', '.'))
    except:
        area = ''

    price = int(i.find('div', class_='flat--price').text.strip().replace(' ', '').replace(' ', '').replace('₽', ''))
    old_price = price

    floor = info[1].text.strip().split(' из ')[0]




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
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    price_per_metr = ''
    discount = ''
    price_per_metr_new = ''


    print(
        f"{project}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)



save_flats_to_excel(flats, project, developer)



