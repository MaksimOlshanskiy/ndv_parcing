from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near


def parse_lobanovo_apartments():
    url = "http://lobanovo.ru/vybrat-kvartiru/"

    # Настройка Selenium
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # если нужен headless режим
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Создаем сервис с правильным путем к ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Передаём путь через параметр service
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(5)  # Даем время для загрузки динамического контента

        # Ждём появления кнопки "открыть параметры"
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[span[text()='открыть параметры']]"))
            )
            button.click()
            time.sleep(2)  # подождать, пока панель откроется
        except Exception as e:
            print(f"[!] Не удалось нажать на кнопку 'открыть параметры': {e}")

        # Прокрутка страницы для загрузки всех элементов (опционально)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        apartment_items = soup.find_all('div', class_='room-item')

        apartments = []

        for item in apartment_items:
            try:
                date = datetime.date.today()
                section= item.find('div', class_='r-section').get_text(strip=True).replace('Секция ','')
                price= int(item.find('div', class_='r-price').get_text(strip=True).replace(' руб.','').replace(' ',''))
                area= float(item.find('div', class_='r-square').get_text(strip=True).replace(' м2',''))
                floor= int(item.find('div', class_='r-floar').get_text(strip=True))
                room_count= int(item.find('div', class_='r-room').get_text(strip=True).replace(' ком',''))
                finish_type= item.find('div', class_='r-otdelka').get_text(strip=True)

                if finish_type=='Да':
                    finish_type='С отделкой'
                else:
                    finish_type='Без отделки'

                result = [
                    date, 'Аврора', '', '', '', '', '', '', '', '', '', '', '', '',
                    'Продано', '', '', 'Инвестстрой', '', '', '', '', '1', '', '', '', '',
                    '', '', 'Квартиры', finish_type, room_count, area, '', price, '',
                    '', '', section, floor, ''
                ]
                apartments.append(result)
            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")
                continue

        # Сохранение результатов
        save_flats_to_excel(apartments,'Аврора','Инвестстрой')
        print(f"Найдено {len(apartments)} квартир. Данные сохранены")
        return apartments

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []
    finally:
        driver.quit()


if __name__ == "__main__":
    parse_lobanovo_apartments()
