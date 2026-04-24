from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from functions import save_flats_to_excel

flats_data = []


options = webdriver.ChromeOptions()
# Убери или добавь нужные тебе флаги, например:
# options.add_argument("--headless")  # если нужно без GUI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://pp.moscow/flats/catalog/?stage[]=1")  # вставь свой URL

wait = WebDriverWait(driver, 10)


while True:
    try:
        # скроллим вниз страницы
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(2)

        # ищем кнопку
        button = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a.btn.green.reverse.more-btn")
            )
        )

        # дополнительный скрол именно до кнопки
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        time.sleep(1)

        # клик
        driver.execute_script("arguments[0].click();", button)

        print("Нажали 'Показать ещё'")
        time.sleep(3)  # ждём подгрузку новых объявлений

    except TimeoutException:
        print("Кнопка больше не появилась — объявления закончились")
        break

print("Все объявления загружены")


def get_text_safe(parent, selector_name):
    if parent is None:
        return None
    el = parent.find('span', {'data-name': selector_name})
    if el and el.text:
        return el.text.strip()
    return None

# WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, "div.list.data-table"))
# )
# time.sleep(3)

# HTML после всех кликов
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# ищем контейнер
flats_container = soup.find("div", class_="list data-table")

if flats_container:
    flats = flats_container.find_all("div", class_="item")

    if flats:
        print(f"Найдено квартир: {len(flats)}")

        for flat in flats:
            title = flat.find("div", class_="title")
            price = flat.find("div", class_="price")

            print(
                title.text.strip() if title else "Нет названия",
                price.text.strip() if price else "Нет цены"
            )
    else:
        print("Квартиры не найдены в контейнере")
else:
    print("Контейнер с объявлениями не найден")

print(f"Найдено {len(flats)} квартир для обработки")
parsed_flats = []

for flat in flats:
    try:
        info1 = flat.find('div', class_='info1')
        rooms_text = get_text_safe(info1, 'rooms')
        square_text = get_text_safe(info1, 'square')
        flat_num = get_text_safe(info1, 'num')
        stage = get_text_safe(info1, 'stage')

        try:
            rooms = int(re.search(r'\d+', rooms_text).group()) if rooms_text else None
        except:
            rooms = None

        info4 = flat.find('div', class_='info4')

        # Цена
        price_tag = info4.find('span', {'data-name': 'price'}) if info4 else None
        price = price_tag.text.strip() if price_tag else None
        price_num = int(re.sub(r'[^\d]', '', price)) if price else None

        # Скидка
        discount = None
        discount_el = info4.find('span', {'data-name': 'discount'}) if info4 else None
        if discount_el:
            discount_text = discount_el.text.strip()
            discount = re.sub(r'[^\d]', '', discount_text)

        # Старая цена
        old_price = None
        old_price_el = info4.find('span', {'data-name': 'price_old'}) if info4 else None
        if old_price_el:
            old_price = re.sub(r'[^\d]', '', old_price_el.text.strip())

        info3 = flat.find('div', class_='info3')
        corpus_text = get_text_safe(info3, 'corpus')
        section_text = get_text_safe(info3, 'section')
        floor_text = get_text_safe(info3, 'floor')  # если такой есть, иначе по-другому

        try:
            corpus = int(re.search(r'\d+', corpus_text).group()) if corpus_text else None
        except:
            corpus = None

        try:
            section = int(re.search(r'\d+', section_text).group()) if section_text else None
        except:
            section = None

        # Разбираем этажи
        current_floor = None
        if floor_text:
            floors_found = re.findall(r'\d+', floor_text)
            if floors_found:
                current_floor = int(floors_found[0])

        # Площадь - безопасное преобразование
        try:
            square = float(square_text.split()[0]) if square_text else None
        except:
            square = None

        if old_price==None:
            old_price=price_num

        if old_price==price_num:
            price_num=None

        flat_data = {
            'Дата обновления': datetime.date.today(),
            'Название проекта': 'Преображенская площадь',
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
            'Девелопер': 'Регионы',
            'Округ': '',
            'Район': '',
            'Адрес': '',
            'Эскроу': '',
            'Корпус': corpus,
            'Конструктив': '',
            'Класс': '',
            'Срок сдачи': '',
            'Старый срок сдачи': '',
            'Стадия строительной готовности': '',
            'Договор': '',
            'Тип помещения': 'Квартира',
            'Отделка': 'Без отделки',
            'Кол-во комнат': rooms,
            'Площадь, кв.м': square,
            'Цена кв.м, руб.': '',
            'Цена лота, руб.': int(old_price) if old_price else None,
            'Скидка,%':'',
            'Цена кв.м со ск, руб.': '',
            'Цена лота со ск, руб.': price_num,
            'секция': section,
            'этаж': current_floor,
            'номер': '',
        }

        parsed_flats.append(flat_data)

    except Exception as e:
        print(f"Ошибка обработки квартиры: {e}")
        continue


driver.quit()


save_flats_to_excel(flats_data,'Преображенская площадь 1 очередь', 'Регионы')

