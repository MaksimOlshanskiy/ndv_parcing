import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка драйвера для Selenium
service = Service('C:/chromedriver/chromedriver.exe')
chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL страницы с объявлениями
url = 'https://kvartal-geroev.ru/realty/flats/'

# Загружаем страницу
driver.get(url)

driver.execute_script("""
    const removePopups = () => {
        let popups = document.querySelectorAll('[class*="popup"], [class*="modal"], [class*="overlay"]');
        popups.forEach(p => p.remove());
    };
    removePopups();
    setInterval(removePopups, 100);  // удалять каждые 2 секунды
""")

# Даем время для загрузки динамического контента (можно подкорректировать время в зависимости от скорости сайта)
time.sleep(10)

# Пытаемся кликнуть на кнопку "Показать еще"
try:
    load_more_button = driver.find_element(By.ID, "load-more")
    while load_more_button.is_displayed():
        # Кликаем на кнопку "Показать еще"
        load_more_button.click()
        time.sleep(3)  # Даем время для подгрузки новых данных
        load_more_button = driver.find_element(By.ID, "load-more")
except Exception as e:
    print(f"Ошибка при попытке нажать кнопку 'Показать еще': {e}")

# Получаем HTML-контент страницы после загрузки всех данных
html = driver.page_source

# Парсим HTML с помощью BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Находим все элементы, содержащие информацию о квартирах
apartments = soup.find_all('a', class_='apartments__item')

apartment_data = []

for apartment in apartments:
    try:
        # Извлекаем данные
        price = apartment.get('data-price')  # Цена
        description = apartment.find('span', itemprop='description').text.strip().split()[0]  # Тип квартиры

        if 'Студия' in description:
            rooms = 'студия'

        area = apartment.find('span', itemprop='description').text.strip().split()[1]

        if 'евро' in area:
            rooms = apartment.find('span', itemprop='description').text.strip()[0] + 'Е'
            description = 'Квартира'
            area = float(apartment.find('span', itemprop='description').text.strip().split()[2])
        else:
            area = float(apartment.find('span', itemprop='description').text.strip().split()[1])

        floor = int(apartment.find('div', class_='apartments__features__item').find('div',
                                                                                    class_='apartments__features__value').text.strip())

        building = int(apartment.find_all('div', class_='apartments__features__item')[1].find('div',
                                                                                              class_='apartments__features__value').text.strip())

        apartment_data.append({
            'Дата обновления': datetime.date.today(),
            'Название проекта': 'Квартал Героев',
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
            'Тип помещения': "Квартира",
            'Отделка': "С отделкой",
            'Кол-во комнат': rooms,
            'Площадь, кв.м': area,
            'Цена кв.м, руб.': None,
            'Цена лота, руб.': int(price.replace(' ', '')),
            'Скидка,%': None,
            'Цена кв.м со ск, руб.': None,
            'Цена лота со ск, руб.': None,
            'секция': None,
            'этаж': floor,
            'номер': None,
        })
    except AttributeError as e:
        print(f"Ошибка при извлечении данных из элемента: {e}")

if apartment_data:
    save_flats_to_excel(apartment_data, 'Квартал героев', 'Главстрой')
else:
    print("Не удалось извлечь данные с сайта.")

# Закрываем драйвер
driver.quit()
