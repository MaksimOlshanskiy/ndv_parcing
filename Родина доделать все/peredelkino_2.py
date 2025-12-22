# импорт функции сохранения из другого файла
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
from functions import save_flats_to_excel


def get_full_catalog_html(url):
    options = Options()
    options.add_argument('--headless')  # убрать, чтобы видеть браузер
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    while True:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button-more')))
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
        except:
            break

    html = driver.page_source
    driver.quit()
    return html


def parse_apartments(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.select('a.card')
    results = []

    for card in cards:
        flat = {}

        flat['Дата обновления'] = datetime.date.today().strftime("%Y-%m-%d")
        flat['Название проекта'] = "Переделкино"
        flat['на англ'] = ''
        flat['промзона'] = ''
        flat['Местоположение'] = ''
        flat['Метро'] = ''
        flat['Расстояние до метро, км'] = ''
        flat['Время до метро, мин'] = ''
        flat['МЦК/МЦД/БКЛ'] = ''
        flat['Расстояние до МЦК/МЦД, км'] = ''
        flat['Время до МЦК/МЦД, мин'] = ''
        flat['БКЛ'] = ''
        flat['Расстояние до БКЛ, км'] = ''
        flat['Время до БКЛ, мин'] = ''
        flat['статус'] = ''
        flat['старт'] = ''
        flat['Комментарий'] = ''
        flat['Девелопер'] = "Родина Групп"
        flat['Округ'] = ''
        flat['Район'] = ''
        flat['Адрес'] = ''
        flat['Эскроу'] = ''
        flat['Конструктив'] = ''
        flat['Класс'] = ''
        flat['Старый срок сдачи'] = ''
        flat['Стадия строительной готовности'] = ''
        flat['Договор'] = ''
        flat['Тип помещения'] = 'квартира'
        flat['Отделка'] = 'Без отделки'
        flat['Цена кв.м, руб.'] = ''
        flat['Скидка,%'] = ''
        flat['Цена кв.м со ск, руб.'] = ''
        flat['секция'] = ''

        # Собираем данные из парсинга
        buttons = card.select('.buttons-card')
        flat['Корпус'] = buttons[0].get_text(strip=True).replace('Корпус ', '') if len(buttons) > 0 else ''
        flat['этаж'] = int(buttons[1].get_text(strip=True).replace(' этаж','')) if len(buttons) > 1 else ''

        flat['Срок сдачи'] = ''

        flat['номер'] = ''

        rooms = card.select_one('.card-footer-text')
        flat['Кол-во комнат'] = rooms.get_text(strip=True) if rooms else ''

        if flat['Кол-во комнат']=='Студия':
            flat['Кол-во комнат']='Студия'
        else:
            flat['Кол-во комнат']=rooms.get_text(strip=True).replace(' комнаты','')


        area = card.select_one('.card-footer-accent')
        flat['Площадь, кв.м'] = float(area.get_text(strip=True).replace(' м²','')) if area else ''

        price = card.select_one('.card-row-price')
        flat['Цена лота, руб.'] = int(price.get_text(strip=True).replace('₽','').replace(' ','')) if price else ''
        flat['Цена лота со ск, руб.'] = int(price.get_text(strip=True).replace('₽','').replace(' ','')) if price else ''

        if flat['Цена лота со ск, руб.']==flat['Цена лота, руб.']:
            flat['Цена лота со ск, руб.']=None

        results.append(flat)

    return results


def remove_duplicates(flats):
    seen = set()
    unique_flats = []
    for flat in flats:
        flat_tuple = tuple(sorted(flat.items()))
        if flat_tuple not in seen:
            seen.add(flat_tuple)
            unique_flats.append(flat)
    return unique_flats


def main():
    url = "https://rodina-peredelkino.ru/catalog/"
    html = get_full_catalog_html(url)
    flats = parse_apartments(html)
    flats = remove_duplicates(flats)

    print(f"Всего уникальных квартир: {len(flats)}")

    # вызываем функцию из другого файла
    save_flats_to_excel(flats, project="Переделкино", developer="Родина Групп")


if __name__ == '__main__':
    main()
