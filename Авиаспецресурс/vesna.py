import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Настройки браузера
options = Options()
options.add_argument('--headless')  # Без графического окна
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Запуск драйвера
driver = webdriver.Chrome(options=options)

# Открытие страницы
url = "https://an-50.ru/vesna/filter/clear/apply/"
driver.get(url)

# Ждём загрузку JS
time.sleep(3)

html = driver.page_source
driver.quit()

# Парсим через BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
flats = soup.find_all('div', class_='apartment-block')

data = []
for flat in flats:
    name_tag = flat.find('a', class_='apartment-name')
    corpus_tag = flat.find('a', class_='apartment-corpus')
    price_tag = flat.find('div', class_='apartment-price')
    announce = flat.find('div', class_='apartment-announce')
    announce_items = announce.find_all('p') if announce else []

    floor_tag = flat.find('div', class_='apartment-floor')
    floors = []
    status = ''
    if floor_tag:
        floor_text = floor_tag.get_text(strip=True)
        parts = floor_text.replace('Этаж:', '').replace('дом сдан', '').split(',')

        floors = [f.strip() for f in parts if f.strip().isdigit()]

        span = floor_tag.find('span')
        status = span.get_text(strip=True) if span else ''

    for floor in floors:
        flat_data = {
            'Дата обновления': datetime.date.today(),
            'Название проекта': 'Весна',
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
            'Девелопер': "АСРесурс",
            'Округ': None,
            'Район': None,
            'Адрес': None,
            'Эскроу': None,
            'Корпус': corpus_tag.get_text(strip=True).replace('Дом ', '') if corpus_tag else '',
            'Конструктив': None,
            'Класс': None,
            'Срок сдачи': None,
            'Старый срок сдачи': None,
            'Стадия строительной готовности': None,
            'Договор': None,
            'Тип помещения': 'Квартира',
            'Отделка': "С отделкой",
            'Кол-во комнат': int(name_tag.get_text(strip=True)[0]) if name_tag else '',
            'Площадь, кв.м': '',
            'Цена кв.м, руб.': None,
            'Цена лота, руб.': int(price_tag.find('strong').get_text(strip=True).replace(' ₽', '').replace('\xa0',
                                                                                                           '')) if price_tag and price_tag.find(
                'strong') else '',
            'Скидка,%': None,
            'Цена кв.м со ск, руб.': None,
            'Цена лота со ск, руб.': None,
            'секция': None,
            'этаж': int(floor),
            'номер': None,
        }

        for p in announce_items:
            text = p.get_text(strip=True)
            if text.startswith('Общая площадь'):
                flat_data['Площадь, кв.м'] = float(
                    text.split(':')[-1].strip().replace(' м²', '').replace(',', '.').strip())

        data.append(flat_data)

# Сохраняем
if data:
    save_flats_to_excel(data, 'Весна', 'Авиаспецресурс')
else:
    print('Нет данных для записи')
