from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome()


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

cookies = {
    'spid': '1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3',
    '_ym_uid': '1741679472430329696',
    'tmr_lvid': '21dd9990a0516763e1af5efdddfe2ece',
    'tmr_lvidTS': '1741679492626',
    '___dmpkit___': 'a4186694-8f1a-4c72-a444-15171df726ff',
    '_ym_d': '1757920713',
    'spjs': '1763471574517_02f93493_013501e8_8f0b3b874fce18ec51ebb135a76ec58b_c0R5YGTsV2e6g14u40DmpDQR7osRwjR1mPDcOv/WHyNWLqoqb0YQbeXseXh81RjQpSuHJ2rJbs+S2tY0cMEcTRGI1YQowApmn9ZzcnbfFapfJYEhZMe4eZzU0D56W4ZHa4LPI/JrNbU5kNM8oejE5CmFWzpfF5LzOV7Zi71nklITH0ub7xIJyeD9RGWJRLhIFG/m01pXD2+D7mdAodmKa24sgrL2TzvvjrYio5e/zi4aZcm5QGhFlTmB3b732uZGD2PfqlYuAGI9f2mITk7iczd8Wct9F7LjN89+FJig/OxweUDlHHGOfrKfBiLL04oPs1TVwEQpTImextIg9c47ai6ShvMnD5H07cDJbeT55QVJUpu+Ilpngp6jOn2cwYDnFQ3s6Q3VgnKG/kq+z1fmBhdo1NQIwHiNxJxlRp+X/htXbASkegQO664vcxJ+vtvMytMmB+OL3vpP1rMt8U7h8d1EKdlATvCnupJfz/N6kRKu7LjozUCRgfQcXj76w1c0Q1r8HusG7LyA+bQVmMAa2rdNAWe7R9p6BtpQVaH5LZmtAuQlULjPu06WEgIXzntq3wHamWUtAcAocQ0egyqmBxlAXC1wirMDN54LKvbFY7I2DdmrfUYwtcIauxTYYd/PZC2Ec18TPbqW24ABqeDKOtLTp4JXaD27ntAEwyCYqEkbUjSgcO8HZ7qjKlhkLNCRTTB9KUfOMhJuFwr6XxPllcF4HPh6cJbHQ1sIiEgiZyXAGdOAXVX4q5LK1jT5lD1NsS7UotkzKPjslEAxtY25KS1W8oJWDlv7n6dDPNTLkMSroukt8Ss1xtrDXS5Qy7QRTpk97YgwIULVncjK/yaVQdYfm4qfRvyc8MgVxemhqu43qaHjLnerqkeAdDNDuW2dScCApuCoKwE9lngA5EwXxzTL//5wQTb2sCJPDXT4tUW5Efzs8FkT8jZNWyh+xLVSlj3JqXxI8MKV7EgX6+Off3NKxrZqUh3Nkcl1BNjDbF6RZ9Ozd38K6r62YhHF/ZlpDQTgoHR8J+Sas9//8ksWtDqDfT4CaofHmwPfuIxnU7M3Dt6rLkYZ4kQNTQi608cmwCuRQY2lSs70nQFjDeHbi8fuhgYYy/vKP4VzEubemMr+hdChdM0a6L4EUy/wy5THe4LfrnZKEWW8gW4JUGpU5WkP+ittRkBjhY55qfnFleEwDN0IK2NNOpbdVyB6xZ5ps1HVtXHBDOWwmGUuJ+26q5/ShfVQuR+7SVOmFsI76UgbJI4PAGnAoCz0yW99Bnqaxv8jU4+4AEcnLqui/jeZ4reF2Vt1xZJBokpOwbz1qXg1WAGhXNTL+pYYdERwwG1nIHYDoXmrWLq6gJZjfc1qYb2FcBD1zRZma4NXLQDKhGsaJfaNUGh0RN5nOr25UYJDNq69rGlwJ/d3rVuo/WxAcLQq9uMNteiYdNhSsx/zf2+17bAwPNQJehqzR8aCCshouuC1NTHZCiq4YTS7t1+FY01WuFlUfEfhzMNeP/P7lma7CFiofEQR9vWNSLv5gwZHYzubnD9XDejUvqRzCcCZaQf6gFZ7gxivhMtHMWXvXh1pImQ1NEtvv5nxk4CRus5MipScp3tLBWe+jbHdw+uTQ2pT799WG1CQNMx4vM3FseRgPkr6/hMj5qcKCzHdkI3kMzl2JmpSDf2hmUUw3VA/zbAP26NvRxryv45TIbtN6cm8BdAA9IQf5/RMoNECspZOOiFVpXlBFGVQgV3rd8eLazcm2iJ+wh4eRbx5CXzFMTAkG8e3e1MO/rKKRiX5wZ1tMQjUpHpAD02/BUID9kaSZTH1IK9vVmk5MpqvPlLql+8zDdFeg0Sq78vA1FIauXXE+IMQNuLt0qO/FfIY/0CSQVWMyahtxAvkQ55Y1u9iPu4zCdQle0EebLao9P39d+8qbDXjFlDCFn3ojqqaO/DrXewP2hs1SWBGvaNYs77ZdDE0s+to1Xtk/1YOU=',
    'domain_sid': 'p9NEOoC7wfYKTfSohYE69%3A1763471581292',
    'spsc': '1763538114091_0df2f6bc4e2b6141bff199e3478158b0_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3745525d5f4f58455e445a4a423660',
    'tmr_detect': '0%7C1763539348930',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic MTpxd2U=',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8/?place=0',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; ___dmpkit___=a4186694-8f1a-4c72-a444-15171df726ff; _ym_d=1757920713; spjs=1763471574517_02f93493_013501e8_8f0b3b874fce18ec51ebb135a76ec58b_c0R5YGTsV2e6g14u40DmpDQR7osRwjR1mPDcOv/WHyNWLqoqb0YQbeXseXh81RjQpSuHJ2rJbs+S2tY0cMEcTRGI1YQowApmn9ZzcnbfFapfJYEhZMe4eZzU0D56W4ZHa4LPI/JrNbU5kNM8oejE5CmFWzpfF5LzOV7Zi71nklITH0ub7xIJyeD9RGWJRLhIFG/m01pXD2+D7mdAodmKa24sgrL2TzvvjrYio5e/zi4aZcm5QGhFlTmB3b732uZGD2PfqlYuAGI9f2mITk7iczd8Wct9F7LjN89+FJig/OxweUDlHHGOfrKfBiLL04oPs1TVwEQpTImextIg9c47ai6ShvMnD5H07cDJbeT55QVJUpu+Ilpngp6jOn2cwYDnFQ3s6Q3VgnKG/kq+z1fmBhdo1NQIwHiNxJxlRp+X/htXbASkegQO664vcxJ+vtvMytMmB+OL3vpP1rMt8U7h8d1EKdlATvCnupJfz/N6kRKu7LjozUCRgfQcXj76w1c0Q1r8HusG7LyA+bQVmMAa2rdNAWe7R9p6BtpQVaH5LZmtAuQlULjPu06WEgIXzntq3wHamWUtAcAocQ0egyqmBxlAXC1wirMDN54LKvbFY7I2DdmrfUYwtcIauxTYYd/PZC2Ec18TPbqW24ABqeDKOtLTp4JXaD27ntAEwyCYqEkbUjSgcO8HZ7qjKlhkLNCRTTB9KUfOMhJuFwr6XxPllcF4HPh6cJbHQ1sIiEgiZyXAGdOAXVX4q5LK1jT5lD1NsS7UotkzKPjslEAxtY25KS1W8oJWDlv7n6dDPNTLkMSroukt8Ss1xtrDXS5Qy7QRTpk97YgwIULVncjK/yaVQdYfm4qfRvyc8MgVxemhqu43qaHjLnerqkeAdDNDuW2dScCApuCoKwE9lngA5EwXxzTL//5wQTb2sCJPDXT4tUW5Efzs8FkT8jZNWyh+xLVSlj3JqXxI8MKV7EgX6+Off3NKxrZqUh3Nkcl1BNjDbF6RZ9Ozd38K6r62YhHF/ZlpDQTgoHR8J+Sas9//8ksWtDqDfT4CaofHmwPfuIxnU7M3Dt6rLkYZ4kQNTQi608cmwCuRQY2lSs70nQFjDeHbi8fuhgYYy/vKP4VzEubemMr+hdChdM0a6L4EUy/wy5THe4LfrnZKEWW8gW4JUGpU5WkP+ittRkBjhY55qfnFleEwDN0IK2NNOpbdVyB6xZ5ps1HVtXHBDOWwmGUuJ+26q5/ShfVQuR+7SVOmFsI76UgbJI4PAGnAoCz0yW99Bnqaxv8jU4+4AEcnLqui/jeZ4reF2Vt1xZJBokpOwbz1qXg1WAGhXNTL+pYYdERwwG1nIHYDoXmrWLq6gJZjfc1qYb2FcBD1zRZma4NXLQDKhGsaJfaNUGh0RN5nOr25UYJDNq69rGlwJ/d3rVuo/WxAcLQq9uMNteiYdNhSsx/zf2+17bAwPNQJehqzR8aCCshouuC1NTHZCiq4YTS7t1+FY01WuFlUfEfhzMNeP/P7lma7CFiofEQR9vWNSLv5gwZHYzubnD9XDejUvqRzCcCZaQf6gFZ7gxivhMtHMWXvXh1pImQ1NEtvv5nxk4CRus5MipScp3tLBWe+jbHdw+uTQ2pT799WG1CQNMx4vM3FseRgPkr6/hMj5qcKCzHdkI3kMzl2JmpSDf2hmUUw3VA/zbAP26NvRxryv45TIbtN6cm8BdAA9IQf5/RMoNECspZOOiFVpXlBFGVQgV3rd8eLazcm2iJ+wh4eRbx5CXzFMTAkG8e3e1MO/rKKRiX5wZ1tMQjUpHpAD02/BUID9kaSZTH1IK9vVmk5MpqvPlLql+8zDdFeg0Sq78vA1FIauXXE+IMQNuLt0qO/FfIY/0CSQVWMyahtxAvkQ55Y1u9iPu4zCdQle0EebLao9P39d+8qbDXjFlDCFn3ojqqaO/DrXewP2hs1SWBGvaNYs77ZdDE0s+to1Xtk/1YOU=; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1763471581292; spsc=1763538114091_0df2f6bc4e2b6141bff199e3478158b0_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ; _ym_isad=2; _ym_visorc=b; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3745525d5f4f58455e445a4a423660; tmr_detect=0%7C1763539348930',
}

params = {
    'offset': '0',
    'limit': '20',
    'sortField': 'obj_publ_dt',
    'sortType': 'desc',
    'searchValue': 'москва',
    'residentialBuildings': '1',
    'place': '77',
    'objStatus': '0',
}



buildings_id = ['3025', '3395', '3882', '8637', '22344', '33295', '33296', '38074', '42436', '42437', '44480', '45019', '53850', '55727', '55728', '56378', '57464', '57765', '57833', '57911', '57912', '58179', '58180', '58912', '59950', '60694', '61154', '62048', '62967', '62968', '63664', '63874', '64171', '64236', '65027', '65042', '65271', '65567', '66029', '66184', '66384', '66614', '66615', '66795', '66796', '66817', '67259', '67322', '67372', '67403', '67823', '67824', '67872', '67873', '68028', '68054', '68055', '68056', '68404', '68406', '68407', '68408', '68409', '68410', '68859', '68944', '69169', '69171', '69392', '69662']


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


        driver.get(url=url)
        page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
        soup = BeautifulSoup(page_content, 'html.parser')
        info = soup.find_all('div', class_=["Row__Value-sc-13pfgqd-2 dySlPJ", 'Row__Value-sc-13pfgqd-2 ClvkY'])
        i = []
        for inf in info:

            i.append(inf.text)


        if len(i) == 3:  # сданный проект
            developer = i[0]
            developer_group = 'Сдан'
            project_declaration = i[1]
            publication_date = 'Сдан'
            explotation_start_date = i[2]
            keys_date = 'Сдан'
            avg_metr_price = 'Сдан'
            flats_sales_perc = 'Сдан'
        if len(i) == 4:  # сданный проект
            developer = i[0]
            developer_group = i[1]
            project_declaration = i[2]
            publication_date = 'Сдан'
            explotation_start_date = i[3]
            keys_date = 'Сдан'
            avg_metr_price = 'Сдан'
            flats_sales_perc = 'Сдан'
        if len(i) == 5:   # сданный проект
            developer = i[0]
            developer_group = i[1]
            project_declaration = i[2]
            publication_date = 'Сдан'
            explotation_start_date = i[4]
            keys_date = 'Сдан'
            avg_metr_price = 'Сдан'
            flats_sales_perc = 'Сдан'
        if len(i) == 8:
            developer = i[0]
            developer_group = i[1]
            project_declaration = i[2]
            publication_date = i[3]
            explotation_start_date = i[4]
            keys_date = i[5]
            avg_metr_price = i[6]
            flats_sales_perc = i[7]
        if len(i) == 9:
            developer = i[0]
            developer_group = i[1]
            project_declaration = i[3]
            publication_date = i[4]
            explotation_start_date = i[5]
            keys_date = i[6]
            avg_metr_price = i[7]
            flats_sales_perc = i[8]
        if len(i) == 7:
            developer = i[0]
            developer_group = '-'
            project_declaration = i[1]
            publication_date = i[2]
            explotation_start_date = i[3]
            keys_date = i[4]
            avg_metr_price = i[5]
            flats_sales_perc = i[6]
        if soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY') and len(i) == 6:
            developer = i[0]
            developer_group = '-'
            project_declaration = i[1]
            publication_date = i[2]
            explotation_start_date = soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY').text
            keys_date = i[3]
            avg_metr_price = i[4]
            flats_sales_perc = i[5]
        if soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY') and len(i) == 7:
            developer = i[0]
            developer_group = i[1]
            project_declaration = i[2]
            publication_date = i[3]
            explotation_start_date = soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY').text
            keys_date = i[4]
            avg_metr_price = i[5]
            flats_sales_perc = i[6]



        dop_info = soup.find_all('span', class_="CharacteristicsBlock__RowSpan-sc-1fyyfia-4 eCBXEE")
        i = []
        for inf in dop_info:

            i.append(inf.text)

        klass = i[1]
        material = i[3]
        finish_type = i[5].replace('\xa0', ' ')
        is_free_plan = i[7]
        floors_count = i[9]
        flats_count = i[11]
        living_area = i[13].replace(' ', '')
        roofs_height = i[15]
        bike_paths = i[17]
        playgrounds_count = i[19]
        sports_grounds_count = i[21]
        garbage_collection_sites_count = i[23]
        parking_place_count = i[25]
        guest_places_inside = i[27]
        guest_places_outside = i[29]
        pandus = i[31]
        low_places = i[33]
        wheelchair_lifts_count = i[35]
        entrances_count = i[37]
        passenger_elevators_count = i[39]
        freight_and_passenger_elevators_count = i[41]

        res = [int(building_id), developer, developer_group, project_declaration, publication_date, explotation_start_date.replace('IV', '4').replace('III', '3').replace('II', '2').replace('I', '1').replace('.', ''), keys_date, avg_metr_price, flats_sales_perc, klass, material,
               finish_type, is_free_plan, floors_count, flats_count, living_area, roofs_height, bike_paths, playgrounds_count, sports_grounds_count, garbage_collection_sites_count, parking_place_count, guest_places_inside,
               guest_places_outside, pandus, low_places, wheelchair_lifts_count, entrances_count, passenger_elevators_count, freight_and_passenger_elevators_count]
        print(res)
        flats.append(res)

        sleep_time = random.uniform(2, 7)
        time.sleep(sleep_time)
    except:
        print('Ошибка, пропускаем id')
        problem_id.append(building_id)
        continue

    params = {
        'type': 'apartments',
    }

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{building_id}/sale_graph?type=apartments'
    print(url)

    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
    salesGraphs = json.loads(json_text)['data']
    print(salesGraphs)

    salesGraph = pd.DataFrame(salesGraphs)


    # переводим дату в формат MM.YY
    salesGraph["month"] = pd.to_datetime(salesGraph["reportMonthDt"], dayfirst=True).dt.strftime("%m.%y")

    # убираем столбец даты
    salesGraph = salesGraph.drop(columns="reportMonthDt")

    # превращаем в "длинный" формат
    salesGraph_long = salesGraph.melt(id_vars="month", var_name="metric", value_name="value")

    # формируем имена колонок
    salesGraph_long["column"] = salesGraph_long["month"] + "-" + salesGraph_long["metric"]

    # собираем в одну строку
    salesGraph_result = salesGraph_long.set_index("column")["value"].to_frame().T

    print(salesGraph_result)

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"НашДомРФ_глубже_МО.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['ID дом.рф',
                                  'Застройщик',
                                  'Группа компаний',
                                  'Проектная декларация',
                                  'Дата публикации проекта',
                                  'Ввод в эксплуатацию',
                                  'Выдача ключей',
                                  'Средняя цена за 1 м²',
                                  'Распроданность квартир',
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
print(f"Проблемные ID: {problem_id}")