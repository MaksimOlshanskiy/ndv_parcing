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
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    StaleElementReferenceException, NoSuchElementException


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


driver = webdriver.Chrome()
driver.get("https://kvartaly-otrada.ru/flats")

pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height




page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
elements = driver.find_elements(
    By.CSS_SELECTOR,
    "[class*='parameter-selection__flat']"
)
for i in elements:



    url = ''
    date = datetime.date.today()
    project = i.find_element(By.CSS_SELECTOR,"span.parameter-selection__item-complex").text
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
    developer = "Отрада Девелопмент"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    try:
        korpus = i.find_element(By.CSS_SELECTOR,"div.parameter-selection__item-property.phase").find_element(By.CSS_SELECTOR,"span:nth-of-type(2)").text
    except NoSuchElementException:
        korpus = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    finish_type = ''
    items = i.find_elements(
        By.CSS_SELECTOR,
        "div.parameter-selection__item-marker[class*='parameter-selection__item-finishing'] span"
    )
    if items:
        finish_type = items[0].get_attribute("textContent").strip()
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = 'Квартиры'
    room_count = i.find_element(By.CSS_SELECTOR,"div.parameter-selection__item-property.rooms").find_element(By.CSS_SELECTOR,"span:nth-of-type(2)").text
    area = i.find_element(By.CSS_SELECTOR,"div.parameter-selection__item-property.area").text.replace('Площадь', '').split('м')[0].strip()
    price_per_metr = ''
    try:
        old_price = i.find_element(By.CSS_SELECTOR,"span.parameter-selection__old-cost").text.replace('от', '').replace('₽', '').replace(' ', '').strip()
        price = i.find_element(By.CSS_SELECTOR,"span.parameter-selection__item-cost").text.replace('от', '').replace('₽', '').replace(' ', '').strip()
    except:
        old_price = i.find_element(By.CSS_SELECTOR,"span.parameter-selection__item-cost").text.replace('от', '').replace('₽', '').replace(' ', '').strip()
        price = ''
    discount = ''
    price_per_metr_new = ''
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

driver.quit()







save_flats_to_excel(flats, project, developer)