import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

URL = 'https://balashiha28.ru/prices/kvartiryi/params'
BASE_URL = 'https://balashiha28.ru/'


def parse_flat_item(flat_tag):
    info = flat_tag.select_one('.flat-item__info')

    name_tag = info.select_one('.flat-item__number')
    name_parts = name_tag.get_text(strip=True).split('№')
    room_count = int(name_parts[0].strip()[0])
    area = float(name_tag.find('span').get_text(strip=True).replace(' м2', ''))

    loc_items = info.select('.flat-item__location li')
    corpus = loc_items[0].find_all('span')[1].text.strip()
    section = int(loc_items[1].find_all('span')[1].text.strip())
    floor = int(loc_items[2].find_all('span')[1].text.strip())

    price = int(info.select_one('.flat-item__buy span').get_text(strip=True).replace(' ₽', '').replace(' ', ''))

    return {
        'Дата обновления': datetime.date.today(),
        'Название проекта': 'Преображенский квартал',
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
        'Девелопер': 'Ди Эм Холдинг',
        'Округ': None,
        'Район': None,
        'Адрес': None,
        'Эскроу': None,
        'Корпус': corpus,
        'Конструктив': None,
        'Класс': None,
        'Срок сдачи': None,
        'Старый срок сдачи': None,
        'Стадия строительной готовности': None,
        'Договор': None,
        'Тип помещения': 'Квартира',
        'Отделка': 'Без отделки',
        'Кол-во комнат': room_count,
        'Площадь, кв.м': area,
        'Цена кв.м, руб.': None,
        'Цена лота, руб.': price,
        'Скидка,%': None,
        'Цена кв.м со ск, руб.': None,
        'Цена лота со ск, руб.': None,
        'секция': section,
        'этаж': floor,
        'номер': None,
    }


def main():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)

    wait = WebDriverWait(driver, 10)

    # Жмём на кнопку "Показать ещё", пока она есть
    while True:
        try:
            show_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.params__more')))
            driver.execute_script("arguments[0].click();", show_more)
            time.sleep(1)  # даем время контенту подгрузиться
        except:
            break  # кнопки больше нет

    # Забираем HTML после всех подгрузок
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    flats = []
    for tag in soup.select('a[href*="prices/kvartiryi/korpus"]'):
        try:
            flats.append(parse_flat_item(tag))
        except Exception as e:
            print(f'Ошибка при разборе квартиры: {e}')


    developer = 'Ди Эм Холдинг'
    project = 'Преображенский квартал'
    save_flats_to_excel(flats, project, developer)


if __name__ == '__main__':
    main()
