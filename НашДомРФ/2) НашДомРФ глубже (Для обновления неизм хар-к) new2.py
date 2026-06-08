from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re

options = Options()

driver = webdriver.Chrome(
    options=options,
)

driver.get("https://api.ipify.org")
time.sleep(5)
print(driver.find_element("tag name", "body").text)

'''
e0gdcKM8OS:8C0r1I3U7R
'''

def convert_quarter(text: str) -> str:
    roman_to_int = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4
    }

    for roman, arabic in roman_to_int.items():
        if text.startswith(roman):
            # удаляем " кв." или " кв. "
            rest = text.replace(f"{roman} кв.", "").replace(f"{roman} кв. ", "")
            return f"{arabic} кв {rest.strip()}"

    return text  # если формат не совпал

buildings_id = ['68831', '71592', '58854', '71392', '66807', '71445', '71031', '71505', '71440', '57752', '71032', '50764', '66931', '62677', '71525', '63966', '50516', '71828', '51572', '47112', '50517', '70084']



print(len(buildings_id))
flats = []
problem_id = []
current_date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

for building_id in buildings_id:

    try:
        url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/{building_id}'

        driver.get(url)
        print(driver.title)
        print(driver.current_url)

        wait = WebDriverWait(driver, 10)

        # ждем появления нужных элементов
        element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[text()='Все характеристики']")
            )
        )

        driver.execute_script("arguments[0].click();", element)

        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')

        title = soup.find('h1')

        project_name = title.get_text(strip=True)
        print(project_name)

        status_tag = soup.select_one('label[class*="HouseStatus"]')
        status = status_tag.get_text(strip=True) if status_tag else None
        print(status)


        address = soup.select_one('div.Address__AddressWrapper-sc-1x6nurk-2 h5')

        if address:
            address = address.get_text(strip=True)

        print(address)

        developer_info_text = soup.find('div', class_='DeveloperBlock__TextBlock-sc-xwde49-1').get_text(separator=' | ', strip=True).split("|")

        if len(developer_info_text) == 2:

            developer = developer_info_text[1].strip()
            developer_group = developer_info_text[0].strip()

        else:

            developer = developer_info_text[0].strip()
            developer_group = ''



        print(developer)
        print(developer_group)

        data = {}

        rows = soup.select('div.CharacteristicsBlock__Row-sc-1fyyfia-3')

        for row in rows:
            name = row.select_one('p').get_text(strip=True).replace('\n', ' ')
            value = row.select_one('h5').get_text(strip=True)
            data[name] = value

        print(data)

        add_data = {}

        add_rows = soup.select('div.CharacteristicsBlock__Info-sc-1fyyfia-7')


        for row in add_rows:
            ps = row.find_all('p')
            if len(ps) >= 2:
                key = ps[0].get_text(strip=True).replace('\xa0', ' ')
                value = ps[1].get_text(strip=True).replace('\xa0', ' ')
                add_data[key] = value

        print(add_data)

        for p in soup.find_all('p'):
            if 'Дата публикации проекта' in p.get_text():
                publication_date = re.search(r'\d{2}\.\d{2}\.\d{4}', p.get_text()).group()
                break
        print(publication_date)

        klass = data.get('Класс недвижимости', '')
        explotation_start_date = data.get('Сдача дома', '')
        keys_date = data.get('Выдача ключей', '')
        material = data.get('Материал стен', '')
        floors_count = data.get('Количество этажей', '')
        flats_sales_perc = data.get('Распроданность квартир', '')
        if flats_sales_perc:
            flats_sales_perc = int(flats_sales_perc.replace('%', '').strip())/100
        parking_availability = data.get('Обеспеченность машиноместами', '')
        energy_efficiency_class = add_data.get('Класс энергоэффективности', '')
        first_floor = add_data.get('Первый этаж', '')
        entrances_count = add_data.get('Количество подъездов', '')
        flats_count = add_data.get('Количество квартир', '')
        if flats_count:
            flats_count = int(flats_count.strip())
        flats_count_on_the_floor = add_data.get('Среднее количество квартир на этаже', '')
        living_area = add_data.get('Жилая площадь, м²', '').replace(' ', '')
        if living_area:
            living_area = int(living_area.strip())
        passenger_elevators_count = add_data.get('Количество пассажирских лифтов', '')
        freight_and_passenger_elevators_count = add_data.get('Количество грузовых и грузопассажирских лифтов', '')
        parking_place_count = add_data.get('Количество мест в паркинге', '')
        guest_places_inside = add_data.get('Гостевые места на придомовой территории', '')
        guest_places_outside = add_data.get('Гостевые места вне придомовой территории', '')
        finish_type = add_data.get('Тип отделки', '').replace('\xa0', ' ')
        is_free_plan = add_data.get('Свободная планировка', '')
        average_flat_area = add_data.get('Средняя площадь квартир', '')
        roofs_height = add_data.get('Высота потолков, м', '')
        playgrounds_count = add_data.get('Детские площадки', '')
        sports_grounds_count = add_data.get('Спортивные площадки', '')
        bike_paths = add_data.get('Велосипедные дорожки', '')
        garbage_collection_sites_count = add_data.get('Количество площадок для сбора мусора', '')
        pandus = add_data.get('Наличие пандуса', '')
        low_places = add_data.get('Понижающие площадки', '')
        wheelchair_lifts_count = add_data.get('Инвалидные подъемники', '')
        try:
            flats_left = round(flats_count - (flats_count * flats_sales_perc))
        except:
            flats_left = ''




        res = [int(building_id), project_name, developer, developer_group, status, publication_date, explotation_start_date.replace('IV', '4').replace('III', '3').replace('II', '2').replace('I', '1').replace('.', ''), keys_date, flats_sales_perc, flats_left, klass, material,
               finish_type, is_free_plan, floors_count, flats_count, living_area, roofs_height, bike_paths, playgrounds_count, sports_grounds_count, garbage_collection_sites_count, parking_availability, parking_place_count, guest_places_inside,
               guest_places_outside, pandus, low_places, wheelchair_lifts_count, entrances_count, passenger_elevators_count, freight_and_passenger_elevators_count]
        print(res)
        flats.append(res)

        sleep_time = random.uniform(2, 7)
        time.sleep(sleep_time)




        # Базовый путь для сохранения
        base_path = r""

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = f"НашДомРФ_глубже_080626_add.xlsx"

        # Полный путь к файлу
        file_path = os.path.join(folder_path, filename)

        df = pd.DataFrame(flats, columns=['ID дом.рф',
                                          'Название проекта',
                                          'Застройщик',
                                          'Группа компаний',
                                          'Статус',
                                          'Дата публикации проекта',
                                          'Ввод в эксплуатацию',
                                          'Выдача ключей',
                                          'Распроданность квартир',
                                          'Остаток квартир',
                                          'Класс недвижимости',
                                          'Материал стен',
                                          'Тип отделки',
                                          'Свободная планировка',
                                          'Количество этажей',
                                          'Количество квартир',
                                          'Жилая площадь, м²',
                                          'Высота потолков, м',
                                          'Велосипедные дорожки',
                                          'Количество детских площадок',
                                          'Количество спортивных площадок',
                                          'Количество площадок для сбора мусора',
                                          'Обеспеченность машиноместами',
                                          'Количество мест в паркинге',
                                          'Гостевые места на придомовой территории',
                                          'Гостевые места вне придомовой территории',
                                          'Наличие пандуса',
                                          'Наличие понижающих площадок',
                                          'Количество инвалидных подъемников',
                                          'Количество подъездов',
                                          'Количество пассажирских лифтов',
                                          'Количество грузовых и грузопассажирских лифтов'
                                          ])

        # Сохранение файла в папку
        df.to_excel(file_path, index=False)
    except:
        print(f'Проблема с id {building_id}')
        problem_id.append(building_id)


print(f"Проблемные ID: {problem_id}")