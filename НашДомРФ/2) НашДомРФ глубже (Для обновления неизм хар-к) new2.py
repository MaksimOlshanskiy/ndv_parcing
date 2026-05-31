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

buildings_id = [71525, 71524, 69490, 69306, 69298, 69294, 69307, 69305, 69287,
       69288, 69300, 69303, 69289, 69302, 69290, 69293, 69308, 69292,
       69304, 69299, 69297, 69295, 69301, 69296, 69309, 54845, 50157,
       62679, 69993, 69261, 53594, 53593, 57497, 57498, 57495, 57499,
       57492, 57493, 69990, 70064, 66113, 15110, 71445, 64327, 58215,
       70592, 70593, 65400, 71282, 71283, 71280, 71281, 62090, 62045,
       55029, 68289, 58218, 62992, 64372, 64373, 64374, 71507, 71510,
       71509, 71508, 71386, 71385, 71387, 71392, 42477, 42475, 59954,
       70086, 70028, 70027, 60531, 58606, 58599, 58600, 58601, 58602,
       58603, 58604, 58605, 70392, 70393, 71246, 61304, 56213, 59618,
       61387, 46583, 67102, 67103, 67104, 67105, 67106, 67107, 67117,
       67118, 67119, 67120, 67121, 67122, 67123, 67124, 67125, 67126,
       67127, 67128, 67129, 67130, 44373, 67709, 67710, 67711, 67131,
       67132, 67133, 67134, 67108, 67109, 67110, 67111, 67112, 67113,
       67114, 67115, 42888, 42890, 42887, 42884, 42889, 42885, 42886,
       56451, 32335, 32336, 54531, 69713, 69712, 69711, 71492, 39402,
       39384, 39398, 39400, 39392, 39408, 39391, 39393, 39404, 39388,
       39411, 39395, 39403, 39409, 39389, 39390, 39407, 39385, 39405,
       39397, 39413, 39410, 39396, 39401, 39412, 39399, 39387, 39406,
       39386, 66038, 66037, 65993, 65994, 65495, 65494,  3229, 71441,
       65270, 65193, 65269, 65685, 65678, 65666, 65716, 65663, 65683,
       65676, 65656, 65710, 65709, 65690, 65700, 65652, 65672, 65661,
       65670, 65655, 65702, 65671, 65665, 65689, 65653, 65654, 65684,
       65693, 65651, 65658, 65680, 65697, 65714, 65713, 65679, 65707,
       65659, 65706, 65673, 65662, 65712, 65657, 65715, 65650, 65699,
       65708, 65682, 65705, 65669, 65677, 65688, 65694, 65664, 65667,
       65668, 65674, 65681, 65675, 65701, 65686, 65687, 65691, 65692,
       65696, 65698, 63361, 63357, 63360, 63355, 63356, 63362, 63358,
       63236, 62495, 69664, 69665, 63283, 70270, 71505, 70964, 70965,
       69989, 30686, 71667, 48118, 70975, 69373, 69371, 69370, 69372,
       23984, 23983, 54241, 50014, 49943, 70997, 65212, 65214, 65215,
       65213, 65118, 65120, 65123, 65119, 65121, 65122, 56656, 56657,
       56655, 56659, 56658, 56654, 55734, 55741, 55737, 55735, 55739,
       55738, 55736, 55740, 70512, 60181, 71745, 70111, 70110, 70116,
       70112, 70109, 70115, 70113, 70114, 69325, 69324, 69326, 43161,
       63764, 69316, 68175, 64626, 64624, 64623, 64625, 64174, 64071,
       66951, 58715, 71032, 71031, 66411, 31920, 31921, 31918, 31930,
       31934, 31932, 31926, 31917, 31928, 31925, 31929, 31923, 31914,
       31922, 31915, 31919, 31931, 31924, 31933, 31916, 31935, 31936,
       70898, 70899, 69944, 71296, 71297, 71292, 71294, 71291, 71295,
       71293, 71290, 71267, 71269, 71265, 71264, 71271, 71266, 71270,
       71268, 71263, 70288, 70294, 70291, 70292, 70290, 70293, 70289,
       70295, 69948, 69951, 69945, 69949, 69946, 69947, 69943, 71539,
       71540, 71541, 71444, 71443, 71442, 71398, 71365, 70181, 68965,
       68284, 68285, 68283, 68286, 68270, 68077, 68076, 68022, 68024,
       68023, 68026, 68025, 67734, 67727, 67729, 67564, 67585, 67573,
       67568, 67590, 67576, 67584, 67570, 67581, 67578, 67583, 67571,
       67577, 67562, 67569, 67572, 67586, 67567, 67563, 67574, 67591,
       67592, 67565, 67588, 67575, 67566, 67589, 67580, 67579, 67351,
       66004, 66001, 64523, 64522, 64172, 61438, 60715, 60559, 60558,
       58763, 58764, 58762, 56007, 56009, 56011, 56010, 56027, 56012,
       55954, 55953, 55952, 55876, 55391, 54873, 33422, 33421, 71592,
       57808, 62088, 29009, 26460, 26466, 40160, 66023, 65172, 71545,
       67696, 46311, 65422, 52006, 52227, 30004, 31074, 41581,  7531,
       71090, 68926, 69006, 52725, 66982, 66981, 66957, 67388, 67329,
       53802, 70960, 70961, 68728, 61344, 43701, 69377, 69374, 69375,
       30242, 65267, 71025, 70310, 70309, 71340, 32320, 32321, 32322,
       70718, 70968, 71425, 58135, 62589, 65337, 58749, 54732, 66447,
       66448, 66443, 71480, 71468, 69317, 70300, 70368, 45850, 45851,
       67699, 63647, 68426, 27252, 47512, 47509, 47510, 47511, 47508,
       67437, 27251, 27240, 27242, 26278, 60591, 69595, 54664, 53520,
       71428, 24954, 65478, 70374, 51622, 48805, 70547, 66744, 48777,
       48776, 48779, 70783, 55104, 55106, 55105, 56953, 42929, 54981,
       54917, 64748, 65125, 70684, 69378, 67859, 71477, 64004, 63823,
       47688, 70663, 49358, 69775, 69774, 56910, 44771, 50366, 51929,
       70442, 64168, 66802, 70590, 68659, 68660, 68658, 70118, 70117,
       70119, 66300, 71512, 71446, 71206, 71138, 70225, 69178, 68217,
       67173, 66285, 64850, 63865, 63875, 61290, 59864, 56719, 55992,
       54161, 52976, 52871, 52872, 52869, 52873, 52371, 52372, 52233,
       52235, 52236, 52234, 49702, 46468, 36579, 35845, 35847, 35850,
       35851, 35846, 35848, 35852, 35849, 24248]


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

        filename = f"НашДомРФ_глубже_190526_add.xlsx"

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