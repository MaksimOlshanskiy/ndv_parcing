import re
import time
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Настройки Selenium
options = Options()
# options.add_argument('--headless')  # Можно убрать, если хочешь видеть окно
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Укажи путь до chromedriver, если нужно
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Открываем страницу
url = 'https://shkolny-nf.ru/prices/flats'
driver.get(url)

# Ждём, пока появится кнопка
try:
    while True:
        # Ждём, пока кнопка станет доступной
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'products__show-more'))
        )
        show_more = driver.find_element(By.ID, 'products__show-more')
        if not show_more.is_displayed():
            break

        # Пробуем кликнуть
        try:
            show_more.click()
            time.sleep(2)  # даём время подгрузиться
        except:
            break  # если клик не проходит — выходим
except:
    pass  # кнопки может уже не быть

# Получаем HTML после всех подгрузок
html = driver.page_source
driver.quit()

# Парсим как раньше
soup = BeautifulSoup(html, 'html.parser')
flats = soup.find_all('tr', class_='flat-item')
data = []

for flat in flats:
    room_title = flat.find('td', class_='room-title')
    title = room_title.text.strip()
    if 'Студия' in title:
        rooms = 'Студия'
    else:
        room_count = re.findall(r'\d+', title)
        rooms = int(room_count[0]) if room_count else 'Не указано'
    title = 'Квартира'

    area = room_title.find('span')
    area_value = float(
        area.text.strip().replace('м²', '').replace(',', '.').replace('м2', '')) if area else 'Не указано'

    price = flat.find('span', class_='price')
    if price:
        # Ищем все вложенные <span> в .price
        price_spans = price.find_all('span')
        price_text = ''
        for span in reversed(price_spans):
            text = span.get_text(strip=True).replace('\xa0', '').replace(' ', '')
            if re.fullmatch(r'\d+₽?', text) or re.search(r'\d', text):
                price_text = text
                break

        # Извлекаем число
        match = re.search(r'\d+', price_text)
        price_value = int(match.group()) if match else 'Не указано'
    else:
        price_value = 'Не указано'

    floor = flat.find_all('td', class_='hide-on-m')
    if floor and len(floor) > 1:
        floor_text = floor[1].text.strip()
        if 'из' in floor_text:
            current_floor = int(floor_text.split(' из ')[0])
        else:
            current_floor = 'Не указано'
    else:
        current_floor = 'Не указано'

    data.append({
        'Дата обновления': datetime.date.today(),
        'Название проекта': 'Школьный',
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
        'Девелопер': "СМУ 29",
        'Округ': None,
        'Район': None,
        'Адрес': None,
        'Эскроу': None,
        'Корпус': 1,
        'Конструктив': None,
        'Класс': None,
        'Срок сдачи': None,
        'Старый срок сдачи': None,
        'Стадия строительной готовности': None,
        'Договор': None,
        'Тип помещения': title,
        'Отделка': 'без отделки',
        'Кол-во комнат': rooms,
        'Площадь, кв.м': area_value,
        'Цена кв.м, руб.': None,
        'Цена лота, руб.': price_value,
        'Скидка,%': None,
        'Цена кв.м со ск, руб.': None,
        'Цена лота со ск, руб.': None,
        'секция': None,
        'этаж': current_floor,
        'номер': None
    })

developer = 'СМУ 29'
project = 'Школьный'
save_flats_to_excel(data, project, developer)
