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

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

url = 'https://pirogovo-riviera.ru/catalog/?min_price=5&max_price=18&rooms_amount='

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # если хочешь без окна браузера
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

wait = WebDriverWait(driver, 10)

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
    title_tag = item.select_one('.woocommerce-loop-product__title a')
    if not title_tag:
        continue

    flat_name = title_tag.text.strip()
    flat_url = title_tag['href']

    korpus = item.select_one('.product-title')
    korpus = korpus.text.strip().replace('Корпус №', '') if korpus else ''

    price_tags = item.select('bdi')
    prices = []
    for tag in price_tags:
        txt = tag.text.strip().replace('от', '').replace('р', '').replace(' ', '')
        if txt.isdigit():
            prices.append(int(txt))

    price_lot = price_discounted = ''
    if prices:
        max_price = max(prices)
        min_price = min(prices)
        price_lot = str(max_price)
        price_discounted = str(min_price)

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

    if price_lot == price_discounted:
        price_discounted = None

    flats_data.append({
        'Дата обновления': datetime.date.today(),
        'Название проекта': 'Пироговская Ривьера',
        'на англ': None,
        'промзона': None,
        'Местоположение': None,
        'Метро': None,
        'Расстояние до метро, км': None,
        'Время до метро, мин': None,
        'МЦК/МЦД/БКЛ': None,
        'Расстояние до МЦК/МЦД, км': None,
        'Время до МЦК/МЦД, мин': None,
        'БКЛ': None,
        'Расстояние до БКЛ, км': None,
        'Время до БКЛ, мин': None,
        'статус': None,
        'старт': None,
        'Комментарий': None,
        'Девелопер': "Эс Ди Ай",
        'Округ': None,
        'Район': None,
        'Адрес': None,
        'Эскроу': None,
        'Корпус': korpus,
        'Конструктив': None,
        'Класс': None,
        'Срок сдачи': None,
        'Старый срок сдачи': None,
        'Стадия строительной готовности': None,
        'Договор': None,
        'Тип помещения': "Квартира",
        'Отделка': finishing,
        'Кол-во комнат': flat_type.split(' ')[0],
        'Площадь, кв.м': float(area) if area else None,
        'Цена кв.м, руб.': None,
        'Цена лота, руб.': int(price_lot) if price_lot else None,
        'Скидка,%': None,
        'Цена кв.м со ск, руб.': None,
        'Цена лота со ск, руб.': int(price_discounted) if price_discounted else None,
        'секция': '',
        'этаж': floor,
        'номер': None
    })

# Сохраняем в Excel
developer = 'Эс Ди Ай'
project = 'Пироговская Ривьера'
save_flats_to_excel(flats_data, project, developer)
