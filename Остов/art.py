from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)

url = "https://ostov-art.ru/prices/flats#&orderby=price&orderto=asc&page=1&perpage=20&return_type=prices%2Fflats&slider_update=false&price_from=0.5&price_to=33.2&square_from=5&square_to=199&floor_from=1&floor_to=7&sort-flats=on&is_filter=yes&ac=1"

driver.get(url)
time.sleep(2)

flats = []
processed_urls = set()

while True:
    try:
        # Ожидаем загрузки элементов
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.flat-item"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "tr.flat-item")
        print(f"Найдено {len(rows)} квартир на текущей странице")

        new_flats_added = 0

        for row in rows:
            try:
                href = row.find_element(By.CSS_SELECTOR, ".room-title").get_attribute("data-href")
                detail_url = f"https://ostov-art.ru/{href}"

                # Проверяем, не обрабатывали ли мы уже эту квартиру
                if detail_url not in processed_urls:
                    room = row.find_element(By.CSS_SELECTOR, ".room-title").text.strip()
                    area = row.find_elements(By.CSS_SELECTOR, ".hide-on-m")[3].text.strip()
                    section = row.find_elements(By.CSS_SELECTOR, ".hide-on-m")[1].text.strip()
                    floor_text = row.find_elements(By.CSS_SELECTOR, ".hide-on-m")[2].text.strip()
                    floor = int(floor_text.split(' из ')[0])
                    price = row.find_element(By.CSS_SELECTOR, ".price").text.strip().replace("₽", "").replace(" ", "")

                    flats.append({
                        'Дата обновления': datetime.date.today(),
                        'Название проекта': 'АРТ',
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
                        'Девелопер': "Остов",
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
                        'Тип помещения': "Квартира",
                        'Отделка': 'без отделки',
                        'Кол-во комнат': int(room.replace("-комнатная", "")),
                        'Площадь, кв.м': float(area),
                        'Цена кв.м, руб.': None,
                        'Цена лота, руб.': int(price),
                        'Скидка,%': None,
                        'Цена кв.м со ск, руб.': None,
                        'Цена лота со ск, руб.': None,
                        'секция': section,
                        'этаж': floor,
                        'номер': None
                    })
                    processed_urls.add(detail_url)
                    new_flats_added += 1
            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")

        print(f"Добавлено {new_flats_added} новых квартир")

        # Проверяем кнопку "Показать еще"
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#products__show-more .btn.btn-default"))
            )

            if "Показать еще" in button.text:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(0.5)
                driver.execute_script("arguments[0].click();", button)

                WebDriverWait(driver, 10).until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, "tr.flat-item")) > len(rows)
                )
                time.sleep(1)
            else:
                print("Все квартиры загружены")
                break
        except:
            print("Кнопка 'Показать еще' не найдена или недоступна")
            break

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        break

driver.quit()

developer = 'Остов'
project = 'Арт'
save_flats_to_excel(flats, project, developer)
