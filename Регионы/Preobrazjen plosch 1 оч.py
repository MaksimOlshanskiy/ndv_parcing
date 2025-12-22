from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import datetime
import re

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

"""
Нужно посчитать количество необходимых кликов и вписать это число в переменную max_clicks
А в идеале переделать
"""

# Настройки для Selenium
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Укажите путь к вашему chromedriver
service = Service('C:/chromedriver/chromedriver.exe')


def setup_driver():
    """Настройка и запуск веб-драйвера"""
    options = webdriver.ChromeOptions()
    # Убери или добавь нужные тебе флаги, например:
    # options.add_argument("--headless")  # если нужно без GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def click_show_more(driver, max_clicks=23):
    from selenium.common.exceptions import (
        NoSuchElementException, StaleElementReferenceException,
        TimeoutException, ElementClickInterceptedException
    )

    clicks = 0
    last_count = len(driver.find_elements(By.CSS_SELECTOR, "div.list.data-table div.item"))

    while clicks < max_clicks:
        try:
            # Ждём появления кнопки "Показать ещё"
            more_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.buttons a.more-btn"))
            )

            # Прокручиваем страницу к кнопке
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)  # Даем время на прокрутку

            # Прокручиваем немного вниз, чтобы убрать возможное перекрытие
            driver.execute_script("window.scrollBy(0, 100);")
            time.sleep(1)

            # Пробуем кликнуть по кнопке обычным способом
            try:
                more_button.click()
            except Exception:
                # Если не получилось, кликаем через JavaScript
                driver.execute_script("arguments[0].click();", more_button)

            print(f"Клик №{clicks + 1} выполнен")
            time.sleep(5)  # Ждем загрузку новых элементов

            # Проверяем, появилось ли больше квартир
            current_count = len(driver.find_elements(By.CSS_SELECTOR, "div.list.data-table div.item"))
            if current_count <= last_count:
                print("Больше новых квартир не появилось")
                break

            last_count = current_count
            clicks += 1

        except TimeoutException:
            print("Кнопка не найдена или не кликабельна")
            break
        except StaleElementReferenceException:
            print("Элемент устарел, перезапрашиваем")
            time.sleep(2)
            continue
        except ElementClickInterceptedException:
            print("Кнопка перекрыта, прокручиваем немного вверх")
            driver.execute_script("window.scrollBy(0, -150);")
            time.sleep(2)
            continue
        except Exception as e:
            print(f"Ошибка: {e}")
            break

    return clicks


def get_text_safe(parent, selector_name):
    if parent is None:
        return None
    el = parent.find('span', {'data-name': selector_name})
    if el and el.text:
        return el.text.strip()
    return None

def parse_pp_moscow_flats():
    driver = setup_driver()
    url = "https://pp.moscow/flats/catalog/"

    try:
        print("Открываем страницу...")
        driver.get(url)

        # Ожидаем загрузки контейнера с квартирами
        print("Ожидаем загрузки данных...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.list.data-table"))
        )
        time.sleep(3)

        # Нажимаем кнопку "Показать ещё" несколько раз
        total_clicks = click_show_more(driver)
        print(f"Всего выполнено нажатий: {total_clicks}")

        # Получаем HTML после полной загрузки
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        flats_container = soup.find('div', class_='list data-table')
        if not flats_container:
            print("Контейнер с квартирами не найден в загруженном HTML")
            return []

        flats = flats_container.find_all('div', class_='item')
        if not flats:
            print("Квартиры не найдены в контейнере")
            return []

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

        return parsed_flats

    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return []

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Запуск парсера Преображенская площадь...")
    start_time = time.time()

    flats_data = parse_pp_moscow_flats()

    if flats_data:
        print(f"Успешно обработано {len(flats_data)} квартир")
        save_flats_to_excel(flats_data,'Преображенская площадь 1 очередь', 'Регионы')
    else:
        print("Не удалось получить данные о квартирах")

    print(f"Общее время выполнения: {time.time() - start_time:.2f} сек")
