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

buildings_id = ['66527', '56266', '70900', '62998', '54220', '47690', '6636999', '63646', '35468', '51091', '69377', '51928', '64073', '70357', '31913', '64808', '59212', '68806', '68618', '59628', '61422', '69549', '66234', '53988', '54616', '58524', '45192', '66240', '67498', '52082', '69508', '64768', '56305', '50448', '69718', '62732', '55215', '65944', '52455', '64622', '27248', '68901', '58281', '54897', '68181', '68198', '57478', '67099', '59391', '45298', '49777', '45184', '65639', '66869', '72616', '60622', '71505', '63685', '54218', '59686', '64430', '65642', '46648', '53464', '63732', '67735', '55028', '65114', '71031', '65825', '54725', '65561', '58775', '62138', '60425', '53713', '35467', '57805', '60548', '63354', '67723', '51437', '63924', '65833', '70778', '59753', '61562', '72615', '51395', '32274', '57752', '70846', '61046', '63054', '59598', '53748', '62557', '56363', '24535', '72374', '50975', '66008', '72816', '71138', '61654', '65641', '62793', '68245', '62840', '69431', '64983', '56234', '72781', '68965', '63966', '58802', '56265', '69275', '64072', '42557', '63450', '63822', '67384', '50200', '50409', '63052', '69374', '51949', '66399', '52870', '56224', '58644', '56715', '60247', '66131', '72298', '69251', '65460', '62556', '59756', '71282', '61610', '70278', '60564', '59237', '71066', '66328', '70095', '57838', '63049', '71828', '44768', '58714', '57448', '69153', '50237', '27250', '58776', '67972', '53661', '69675', '72766', '55760', '54394', '72621', '64621', '68269', '54038', '64921', '54583', '54281', '45519', '66547', '62839', '60421', '72702', '66746', '54579', '53581', '72619', '43199', '69433', '56157', '65370', '70395', '53790', '67728', '64065', '68275', '63754', '68144', '62494', '54039', '67094', '53521', '60526', '61674', '57885', '50364', '63603', '60790', '48694', '65525', '51440', '70084', '65513', '56842', '71891', '73047', '50976', '44769', '58187', '51567', '30640', '70548', '44596', '64494', '61312', '70179', '46646', '50363', '59595', '64003', '47486', '50407', '65638', '66363', '64126', '58217', '53542', '61521', '57881', '58132', '47431', '53523', '54984', '61675', '66793', '62841', '59150', '45826', '68503', '56264', '72620', '60177', '58133', '48352', '56270', '44648', '54723', '60896', '67708', '65371', '59036', '70594', '63789', '56932', '66132', '51560', '62843', '52453', '56071', '64219', '49356', '63222', '71579', '63056', '48260', '70382', '55633', '69386', '31912', '72622', '72225', '54578', '56753', '47511', '66052', '58201', '61714', '56899', '64340', '69352', '67732', '71525', '69179', '50408', '58243', '54449', '55796', '72885', '64566', '58803', '71428', '67615', '61251', '63015', '67205', '64324', '50365', '63925', '64029', '62789', '71440', '57884', '27247', '69950', '65338', '59507', '63787', '72704', '55422', '67396', '68276', '69252', '65834', '59759', '55103', '67620', '71592', '60011', '59887', '61323', '51394', '72701', '53412', '54315', '62266', '55387', '72273', '19620', '70050', '60872', '55102', '70409', '54454', '56514', '56951', '54313', '70027', '56062', '63030', '56306', '62125', '55594', '66400', '62547', '56394', '63053', '62265', '48767', '59146', '46647', '64933', '37859', '59506', '64627', '58300', '61311', '55420', '58232', '62590', '54980', '71062', '61303', '52712', '54314', '59327', '64936', '53411', '44125', '54724', '56672', '62896', '56674', '72161', '59540', '49532', '54450', '61676', '54299', '64805', '59897', '64620', '65182', '62087', '40634', '54293', '68291', '70939', '53522', '50893', '65141', '68887', '63948', '58312', '39716', '61088', '66801', '56687', '65023', '56502', '36234', '68513', '63900', '66710', '31911', '56102', '64082', '70938', '67209', '56673', '45970', '57179', '53541', '57008', '53635', '58298', '59144', '39827', '68196', '61842', '62498', '59934', '63895', '56341', '72055', '68174', '67700', '63755', '56214']



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