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

url = 'https://pirogovo-riviera.ru/catalog/?min_price=5&max_price=18&rooms_amount='

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # если хочешь без окна браузера
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

wait = WebDriverWait(driver, 4)
date = datetime.date.today()

# Цикл клика по кнопке "Показать еще"
while True:
    flats = driver.find_elements(By.CSS_SELECTOR, 'li.product')
    count_before = len(flats)

    try:
        load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.load-more-all')))
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", load_more_button)
        print("Нажали кнопку 'Показать еще'")
        time.sleep(4)
    except (TimeoutException, NoSuchElementException):
        print("Кнопка 'Показать еще' не найдена или недоступна, выходим из цикла")
        break

    flats = driver.find_elements(By.CSS_SELECTOR, 'li.product')
    count_after = len(flats)

    if count_after == count_before:
        print("Новых квартир после нажатия не появилось, выходим из цикла")
        break

print(f"Всего квартир загружено: {count_after}")

# Теперь парсим все квартиры
page_source = driver.page_source
driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')

flats_data = []

for item in soup.select('li.product'):
    try:
        title_tag = item.select_one('.woocommerce-loop-product__title a')
        if not title_tag:
            continue

        flat_name = title_tag.text.strip()
        flat_url = title_tag['href']

        korpus = item.select_one('.product-title')
        korpus = korpus.text.strip().replace('Корпус №', '') if korpus else ''


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
        price_lots = item.find_all('span', class_= ['woocommerce-Price-amount', 'amount'])

        try:
            price_lot = price_lots[1].text.strip().replace('от', '').replace(' ', '').replace('р', '')
            price_discounted = price_lots[0].text.strip().replace('от', '').replace(' ', '').replace('р', '')

        except IndexError:

            price_lot = price_lots[0].text.strip().replace('от', '').replace(' ', '').replace('р', '')
            price_discounted = ''


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
        korpus = item.find('p', class_='product-title').text.strip().replace('Корпус №', '')
        konstruktiv = ''
        klass= ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = "Квартира"
        finish_type = finishing
        room_count = flat_type.split(' ')[0]
        area = area
        price_per_metr = ''
        old_price = int(price_lot)
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(price_discounted)
        except:
            price = ''
        section = ''
        floor = floor
        flat_number = ''
    except:
        continue

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
