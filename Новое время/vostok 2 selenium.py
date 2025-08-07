from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import datetime

from functions import save_flats_to_excel


def parse_vostok_all_pages():
    apartments_data = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = 'https://www.gkvostok2.ru/search?price=5.04494&price=43.74&floor=2&floor=17&square=24.49&square=108&ordering=price&pagination[page]=1&pagination[pageSize]=10'
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flat-card')))

    last_count = 0
    scroll_pause_time = 2
    max_no_change = 3  # Максимальное количество итераций без новых карточек
    no_change_counter = 0

    while True:
        # Прокручиваем вниз страницы
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        cards = driver.find_elements(By.CSS_SELECTOR, '.flat-card')
        current_count = len(cards)

        if current_count == last_count:
            no_change_counter += 1
            if no_change_counter >= max_no_change:
                # Новых квартир больше не подгружается
                break
        else:
            no_change_counter = 0
            last_count = current_count

    # Парсим все собранные карточки
    for card in cards:
        try:
            title = card.find_element(By.CSS_SELECTOR, '.flat-card__header-title').text.strip()
            subtitle = card.find_element(By.CSS_SELECTOR, '.flat-card__header-subtitle').text.strip()
            price_text = card.find_element(By.CSS_SELECTOR, '.flat-card__price').text.strip()

            match_title = re.search(r'(\d+)\s+комнат[аы]?,?\s*(\d+\.?\d*)', title)
            rooms = int(match_title.group(1)) if match_title else ''
            square = float(match_title.group(2)) if match_title else ''

            match_sub = re.search(r'Литер\s+(\d+),\s*Секция\s+(\d+),\s*Этаж\s+(\d+)', subtitle)
            liter = match_sub.group(1) if match_sub else ''
            section = match_sub.group(2) if match_sub else ''
            floor = int(match_sub.group(3)) if match_sub else ''

            price_clean = re.sub(r'\D', '', price_text)
            price_int = int(price_clean) if price_clean else ''

            apartment = {
                'Дата обновления': datetime.date.today(),
                'Название проекта': 'Восток 2',
                'на англ': '',
                'промзона': '',
                'Местоположение': '',
                'Метро': '',
                'Расстояние до метро, км': '',
                'Время до метро, мин': '',
                'МЦК/МЦД/БКЛ': '',
                'Расстояние до МЦК/МЦД, км': '',
                'Время до МЦК/МЦД, мин': '',
                'БКЛ': '',
                'Расстояние до БКЛ, км': '',
                'Время до БКЛ, мин': '',
                'статус': '',
                'старт': '',
                'Комментарий': '',
                'Девелопер': 'Новое время',
                'Округ': '',
                'Район': '',
                'Адрес': '',
                'Эскроу': '',
                'Корпус': liter,
                'Конструктив': '',
                'Класс': '',
                'Срок сдачи': '',
                'Старый срок сдачи': '',
                'Стадия строительной готовности': '',
                'Договор': '',
                'Тип помещения': "Квартира",
                'Отделка': 'Без отделки',
                'Кол-во комнат': rooms,
                'Площадь, кв.м': square,
                'Цена кв.м, руб.': '',
                'Цена лота, руб.': price_int,
                'Скидка,%': '',
                'Цена кв.м со ск, руб.': '',
                'Цена лота со ск, руб.': '',
                'секция': section,
                'этаж': floor,
                'номер': ''
            }

            apartments_data.append(apartment)

        except Exception as e:
            print(f"Ошибка при парсинге карточки: {e}")
            continue

    driver.quit()
    return apartments_data


if __name__ == "__main__":
    flats_data = parse_vostok_all_pages()
    if flats_data:
        project = 'Восток 2'
        developer = 'Новое время'
        from save_to_excel import save_flats_to_excel_near
        save_flats_to_excel(flats_data, project, developer)
