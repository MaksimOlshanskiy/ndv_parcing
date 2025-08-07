import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle


url = f'https://mfz-sunterra.ru/units/suites'

driver = webdriver.Chrome()
driver.get(url=url)
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')




def parse_html_to_excel(html: str, file_path: str = None):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')
    data = []

    if not rows:
        print("HTML не содержит строк таблицы.")
        return

    for idx, row in enumerate(rows):
        cols = row.find_all('td')
        if len(cols) >= 8:
            try:
                floor = int(cols[3].text.strip())
                rooms = int(cols[4].text.strip())
                area = float(re.search(r'\d+\.?\d*', cols[5].text).group())
                price_text = cols[7].text.strip().replace('\xa0', '').replace(' ', '')
                price = int(price_text) if price_text.isdigit() else None
                if price == None:
                    continue

                item = {
                    'Дата обновления': datetime.datetime.today().date(),
                    'Название проекта': "Сантерра",
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
                    'Девелопер': "СЗ Сантерра",
                    'Округ': None,
                    'Район': None,
                    'Адрес': None,
                    'Эскроу': None,
                    'Корпус': '1',
                    'Конструктив': None,
                    'Класс': None,
                    'Срок сдачи': None,
                    'Старый срок сдачи': None,
                    'Стадия строительной готовности': None,
                    'Договор': None,
                    'Тип помещения': 'апартаменты',
                    'Отделка': 'Без отделки',
                    'Кол-во комнат': rooms,
                    'Площадь, кв.м': area,
                    'Цена кв.м, руб.': None,
                    'Цена лота, руб.': price,
                    'Скидка,% ': None,
                    'Цена кв.м со ск, руб.': None,
                    'Цена лота со ск, руб.': None,
                    'секция': None,
                    'этаж': floor,
                    'номер': None
                }

                data.append(item)

            except Exception as e:
                print(f"Ошибка при обработке строки #{idx}: {e}")

    if not data:
        print("Нет данных для сохранения.")
        return

    developer = 'СЗ Сантерра'
    project = 'Сантерра'
    save_flats_to_excel(data, project, developer)


parse_html_to_excel(page_content)
