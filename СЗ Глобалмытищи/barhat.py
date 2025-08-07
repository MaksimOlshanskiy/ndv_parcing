import time
import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near


def parse_barhatdom():
    # Настройка Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service('C:/chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    url = "https://barhatdom.ru/apartments/"
    driver.get(url)

    apartments_data = []

    try:
        # Прокрутка страницы для загрузки всех объявлений
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Парсинг данных
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apartment_cards = soup.find_all('div', class_='product-list__col')

        for card in apartment_cards:
            try:
                # Основная информация
                img_tag = card.find('a', class_='item-product__img').find('img')
                title = img_tag.get('alt', '').strip() if img_tag else 'Не указано'
                link = "https://barhatdom.ru" + card.find('a', class_='item-product__img')['href']

                # Детали квартиры
                details = {
                    'Жилая площадь': '',
                    'Этаж': '',
                    'Комнат': '',
                    'Цена ₽': ''
                }

                items = card.find_all('div', class_='item-product__item')
                for item in items:
                    name = item.find('div', class_='item-product__item-name')
                    value = item.find('div', class_='item-product__item-value')
                    if name and value:
                        name_text = name.get_text(strip=True)
                        value_text = value.get_text(strip=True)
                        if name_text in details:
                            details[name_text] = value_text

                rooms_raw = details.get('Комнат', '').strip()

                if rooms_raw == '0' or rooms_raw == '0 комнат' or rooms_raw == '0 комнат.':
                    rooms = "студия"
                else:
                    try:
                        rooms = int(rooms_raw)
                    except:
                        rooms = rooms_raw

                # Формирование записи
                apartment = {
                    'Дата обновления': datetime.date.today(),
                    'Название проекта': 'Бархат',
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
                    'Девелопер': 'СЗ Глобалмытищи',
                    'Округ': '',
                    'Район': '',
                    'Адрес': '',
                    'Эскроу': '',
                    'Корпус': '',
                    'Конструктив': '',
                    'Класс': '',
                    'Срок сдачи': '',
                    'Старый срок сдачи': '',
                    'Стадия строительной готовности': '',
                    'Договор': '',
                    'Тип помещения': "Квартира",
                    'Отделка': 'Без отделки',
                    'Кол-во комнат': rooms,
                    'Площадь, кв.м': float(details.get('Жилая площадь', '').replace('м²', '').replace('м<sup>2</sup>',
                                                                                                      '').replace('м2',
                                                                                                                  '').strip()),
                    'Цена кв.м, руб.': '',
                    'Цена лота, руб.': int(details.get('Цена ₽', '').replace(' ', '')),
                    'Скидка,%': '',
                    'Цена кв.м со ск, руб.': '',
                    'Цена лота со ск, руб.': '',
                    'секция': '',
                    'этаж': int(details.get('Этаж', '')),
                    'номер': ''
                }

                apartments_data.append(apartment)

            except Exception as e:
                print(f"Ошибка при парсинге карточки: {e}")
                continue

    finally:
        driver.quit()

    return apartments_data


if __name__ == "__main__":
    flats_data = parse_barhatdom()
    if flats_data:
        developer = "СЗ Глобалмытищи"
        project = "Бархат"
        save_flats_to_excel(flats_data,project, developer)
