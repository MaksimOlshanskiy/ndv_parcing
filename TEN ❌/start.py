import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from save_to_excel import save_flats_to_excel_middle

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)

try:
    driver.get(
        "https://ten-stroy.ru/parametric/?tab=flats&type_form=flats&joinBuilding%5B362%5D=362&price%5Bmin%5D=3%C2%A0326%C2%A0000&price%5Bmax%5D=72%C2%A0087%C2%A0000&area%5Bmin%5D=19&area%5Bmax%5D=160&floor%5Bmin%5D=1&floor%5Bmax%5D=31&type_req=show&group=1&AB_TEST_CLASS=a-test&sort=price&sort_turn=asc")

    try:
        toggle_button = driver.find_element(By.CLASS_NAME, "j-parametric-complex-toggle")
        if toggle_button.is_displayed():
            driver.execute_script("arguments[0].click();", toggle_button)
            time.sleep(2)
    except NoSuchElementException:
        print("Кнопка раскрытия списка квартир не найдена")

    while True:
        try:
            button = driver.find_element(By.CLASS_NAME, "j-parametric-result-flats-more")
            if button.is_displayed():
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
            else:
                break
        except NoSuchElementException:
            # Кнопка больше не найдена — завершаем
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    flats = soup.find_all('div', class_='parametric-result__flat')

    data = []
    for flat in flats:
        try:
            title = flat.find('div', class_='flat-cart__title')
            type_ = title.get_text(strip=True) if title else None

            if 'Студия' in type_:
                room_count = 0
            else:
                room_count=int(str(title.get_text(strip=True))[0])

            place = flat.find('div', class_='flat-cart__place')
            place = place.get_text(strip=True) if place else ''

            props = flat.find_all('div', class_='flat-cart__prop')
            props_dict = {}
            for prop in props:
                key = prop.find(class_='flat-cart__prop-ttl').get_text(strip=True)
                val = prop.find(class_='flat-cart__prop-val').get_text(strip=True)
                props_dict[key] = val

            area_raw = props_dict.get('Площадь', '')
            area = float(area_raw.replace(' ', '').replace('м²', '').strip())

            floor_raw = props_dict.get('Этаж', '')
            floor = int(floor_raw.split('/')[0].strip())

            price_tag = flat.find('div', class_='flat-cart__price')
            price = int(price_tag.get_text(strip=True).replace(' ', '').replace('i', '')) if price_tag else None

            old_price_tag = flat.find('div', class_='flat-cart__price-old')
            old_price = int(
                old_price_tag.get_text(strip=True).replace(' ', '').replace('i', '')) if old_price_tag else None

            data.append({
                'Дата обновления': datetime.date.today(),
                'Название проекта': 'Старт',
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
                'Девелопер': 'СК Межрегионстрой',
                'Округ': None,
                'Район': None,
                'Адрес': None,
                'Эскроу': None,
                'Корпус': props_dict.get('Дом', '').replace('Дом ', ''),
                'Конструктив': None,
                'Класс': None,
                'Срок сдачи': None,
                'Старый срок сдачи': None,
                'Стадия строительной готовности': None,
                'Договор': None,
                'Тип помещения': 'Квартира',
                'Отделка': 'С отделкой',
                'Кол-во комнат': room_count,
                'Площадь, кв.м': area,
                'Цена кв.м, руб.': None,
                'Цена лота, руб.': old_price,
                'Скидка,%': None,
                'Цена кв.м со ск, руб.': None,
                'Цена лота со ск, руб.': price,
                'секция': None,
                'этаж': floor,
                'номер': None,
            })

        except Exception as e:
            print('Ошибка при обработке квартиры:', e)


    developer = 'СК Межрегионстрой'
    project = 'Старт'
    save_flats_to_excel_middle(data, project, developer)

finally:
    driver.quit()  # ← гарантированное закрытие
