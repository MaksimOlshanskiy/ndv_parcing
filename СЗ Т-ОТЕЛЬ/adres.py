import os
import time
import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near


def parse_adresdoma_ru():
    url = "https://adresdoma.ru/vybrat_po_paramentram"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service('C:/chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get(url)
        time.sleep(3)

        flats_data = []
        seen_numbers = set()  # Для отслеживания уникальных карточек
        page = 1
        max_pages = 20
        previous_card_count = 0

        while page <= max_pages:
            print(f"Обработка страницы {page}...")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            cards = driver.find_elements(By.CSS_SELECTOR, '#apartments_items .roomCard')
            current_card_count = len(cards)

            if current_card_count <= previous_card_count and page > 1:
                print("Новые карточки не загружаются, завершаю парсинг")
                break

            previous_card_count = current_card_count

            for card in cards:
                try:
                    number = card.get_attribute('data-number') or ''
                    if number in seen_numbers:
                        continue  # Пропускаем дубликат
                    seen_numbers.add(number)

                    price = card.find_element(By.CSS_SELECTOR, '.roomCard__price').text.strip().replace('\xa0', ' ').replace(' Р', '')
                    area = card.find_element(By.CSS_SELECTOR, '.roomCard__s').text.strip().replace('\xa0', ' ').replace(' м²', '').replace(' м2', '').replace('Площадь:','')
                    room_count=card.find_element(By.CSS_SELECTOR, '.roomCard__count').text.strip()

                    raw_type = card.find_element(By.CSS_SELECTOR, '.roomCard__title').text.strip().lower()
                    if 'студия' in raw_type:
                        room_count='студия'
                        room_type = 'Квартира'
                    elif 'евро' in raw_type:
                        import re
                        match = re.search(r'(\d+)\s*к\s*евро', raw_type)
                        room_count = f"{match.group(1)}Е" if match else raw_type
                        room_type = 'Квартира'
                    elif 'офис' in raw_type:
                        continue


                    flat_info = {
                        'Дата обновления': datetime.date.today(),
                        'Название проекта': 'Adres',
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
                        'Девелопер': 'СЗ Т-ОТЕЛЬ',
                        'Округ': '',
                        'Район': '',
                        'Адрес': '',
                        'Эскроу': '',
                        'Корпус': '1',
                        'Конструктив': '',
                        'Класс': '',
                        'Срок сдачи': '',
                        'Старый срок сдачи': '',
                        'Стадия строительной готовности': '',
                        'Договор': '',
                        'Тип помещения': room_type,
                        'Отделка': card.find_element(By.CSS_SELECTOR, '.roomCard__type').text.strip(),
                        'Кол-во комнат': room_count,
                        'Площадь, кв.м': float(area),
                        'Цена кв.м, руб.': '',
                        'Цена лота, руб.': price.replace('Цена:','').replace(' ',''),
                        'Скидка,%': '',
                        'Цена кв.м со ск, руб.': '',
                        'Цена лота со ск, руб.': '',
                        'секция': '',
                        'этаж': int(card.find_element(By.CSS_SELECTOR, '.roomCard__level').text.strip().replace(' этаж', '')),
                        'номер': ""
                    }

                    flats_data.append(flat_info)

                except Exception as e:
                    print(f"Ошибка при обработке карточки: {e}")
                    traceback.print_exc()
                    continue

            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, '.s-selector__footer .rvbtn--outline')
                if "disabled" not in load_more_button.get_attribute("class"):
                    driver.execute_script("arguments[0].click();", load_more_button)
                    time.sleep(3)
                else:
                    print("Кнопка 'Загрузить еще' неактивна, завершаю парсинг")
                    break
            except NoSuchElementException:
                print("Кнопка 'Загрузить еще' не найдена, завершаю парсинг")
                break

            page += 1

        return flats_data

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        driver.quit()


if __name__ == "__main__":
    flats_data = parse_adresdoma_ru()
    if flats_data:
        developer = "СЗ Т-ОТЕЛЬ"
        project = "Adres"
        save_flats_to_excel(flats_data, project,developer)
