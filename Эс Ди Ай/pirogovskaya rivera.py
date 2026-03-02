import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

url = 'https://pirogovo-riviera.ru/catalog/?min_price=5&max_price=99&rooms_amount='

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # если хочешь без окна браузера
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

wait = WebDriverWait(driver, 6)
date = datetime.date.today()

# Цикл клика по кнопке "Показать еще"
while True:
    # 1️⃣ Проверяем, появился ли блок "Больше нет доступных квартир"
    try:
        end_block = driver.find_element(By.CSS_SELECTOR, "div.filter-message")

        if "Больше нет доступных квартир" in end_block.text:
            print("Все квартиры загружены")
            break

    except NoSuchElementException:
        pass  # блока ещё нет — продолжаем

    # 2️⃣ Кликаем кнопку
    try:
        load_more_btn = driver.find_element(By.CSS_SELECTOR, "a.load-more-all")

        driver.execute_script("arguments[0].scrollIntoView();", load_more_btn)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", load_more_btn)
        time.sleep(2)

    except NoSuchElementException:
        print("Кнопка не найдена")
        break

# Теперь парсим все квартиры
page_source = driver.page_source
driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')
elements = soup.find_all('div', class_="product-info")

flats_data = []

for item in elements:


    area = item.find('a').text.split(',')[1].replace('м²', '').strip()
    room_count = item.find('a').text.split(',')[0].replace('м²', '').strip()
    korpus = item.find('p', class_="product-title").text.strip().replace('Корпус ', '').replace('№', '')
    prices = item.find_all('span', class_=["woocommerce-Price-amount", "amount"])
    if len(prices) == 2:
        old_price = int(prices[1].text.replace(' ', '').replace('от', '').replace('р', '').strip())
        price = int(prices[0].text.replace(' ', '').replace('от', '').replace('р', '').strip())
    else:
        old_price = int(prices[0].text.replace(' ', '').replace('от', '').replace('р', '').strip())
        price = int(prices[0].text.replace(' ', '').replace('от', '').replace('р', '').strip())


    area_tag = item.select_one('.product-footage')
    area = area_tag.text.replace('кв. м', '').strip() if area_tag else ''

    tags = item.select('.product-tags span')
    flat_type, floor, finishing = '', '', ''
    if tags:
        flat_type = tags[0].text.strip()
        if len(tags) > 1:
            floor = tags[1].text.replace('этаж ', '').split(' ')[0]
        if len(tags) > 2:
            finishing = tags[2].text.strip()

    project = 'Пироговская Ривьера'
    english = ''
    promzona = ''
    mestopolozhenie = ''
    subway = ''
    distance_to_subway = ''
    time_to_subway = ''
    mck = ''
    distance_to_mck = ''
    time_to_mck = ''
    distance_to_bkl = ''
    time_to_bkl = ''
    bkl = ''
    status = ''
    start = ''
    comment = ''
    developer = 'Эс Ди Ай'
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    konstruktiv = ''
    klass= ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = "Квартира"
    tags = item.find_all('div', class_= 'product-tags')
    for finish in tags:

        if 'без отделки' in finish.text.replace('\n', '').strip():
            finish_type = 'Без отделки'
            break
        elif 'С отделкой' in finish.text.replace('\n', '').strip():
            finish_type = 'С отделкой'
            break
        else:
            finish_type = ''
    area = area
    price_per_metr = ''
    discount = ''
    price_per_metr_new = ''
    section = ''
    floor = floor
    flat_number = ''


    print(
        f"{project}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
              klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]

    flats_data.append(result)

# Сохраняем в Excel

save_flats_to_excel(flats_data, project, developer)
