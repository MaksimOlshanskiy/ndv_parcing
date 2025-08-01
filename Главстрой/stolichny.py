import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    StaleElementReferenceException
from bs4 import BeautifulSoup
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка Selenium
service = Service('C:/chromedriver/chromedriver.exe')
chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# Загружаем страницу
url = 'https://100lichny.ru/realty/flats/'
driver.get(url)

driver.execute_script("""
    const removePopups = () => {
        let popups = document.querySelectorAll('[class*="popup"], [class*="modal"], [class*="overlay"]');
        popups.forEach(p => p.remove());
    };
    removePopups();
    setInterval(removePopups, 100);  // удалять каждые 2 секунды
""")

# Даем странице прогрузиться
time.sleep(15)

while True:
    try:
        load_more = driver.find_element(By.ID, 'load-more')

        # Проверим, отображается ли кнопка
        if not load_more.is_displayed():
            break

        driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
        time.sleep(7)
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(7)

    except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):
        break


# Получаем HTML
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

apartments = soup.find_all('div', class_='apartments__item')

apartment_data = []

for apt in apartments:
    try:
        price_raw = apt.get('data-price')
        area_raw = apt.get('data-area')
        href = apt.get('data-href')
        full_link = f"https://100lichny.ru{href}" if href else None

        # Заголовок с типом и площадью
        title = apt.find('div', class_='apartments__item__title')
        title_text = title.text.strip() if title else ''
        if 'Студия' in title_text:
            rooms = "студия"
            area = float(title_text.split()[1].replace(',', '.'))
        else:
            rooms = int(title_text.strip()[0])
            area = float(area_raw) if area_raw else None
        description = 'Квартира'

        floor_block = apt.find('div', class_='apartments__features__label', string='Этаж')
        floor = int(floor_block.find_next_sibling().text.strip()) if floor_block else None

        building_block = apt.find('div', class_='apartments__features__label', string='Корпус')
        building = int(building_block.find_next_sibling().text.strip()) if building_block else None

        location_block = apt.find('div', class_='apartments__features__item--wide')
        location = location_block.text.strip() if location_block else None

        price = int(price_raw) if price_raw else None

        apartment_data.append({
            'Дата обновления': datetime.date.today(),
            'Название проекта': 'Столичный',
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
            'Девелопер': "Главстрой",
            'Округ': None,
            'Район': None,
            'Адрес': None,
            'Эскроу': None,
            'Корпус': building,
            'Конструктив': None,
            'Класс': None,
            'Срок сдачи': None,
            'Старый срок сдачи': None,
            'Стадия строительной готовности': None,
            'Договор': None,
            'Тип помещения': description,
            'Отделка': "С отделкой",
            'Кол-во комнат': rooms,
            'Площадь, кв.м': area,
            'Цена кв.м, руб.': None,
            'Цена лота, руб.': price,
            'Скидка,%': None,
            'Цена кв.м со ск, руб.': None,
            'Цена лота со ск, руб.': price,
            'секция': None,
            'этаж': floor,
            'номер': None,
        })
    except Exception as e:
        print(f"Ошибка при обработке элемента: {e}")

if apartment_data:
    save_flats_to_excel_middle(apartment_data,'Столичный','Главстрой')
else:
    print("Не удалось извлечь данные с сайта.")

driver.quit()
