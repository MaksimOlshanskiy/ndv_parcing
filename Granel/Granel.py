# текущий код выгружает все квартиры из всех ЖК одним запросом

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os


cookies = {
    'csrftoken': 'cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1',
    '_ym_uid': '1741701518760793495',
    '_ym_d': '1741701518',
    '_ym_isad': '2',
    '_ga': 'GA1.2.2019530414.1741701518',
    '_gid': 'GA1.2.119258665.1741701518',
    '_ym_visorc': 'w',
    '_dc_gtm_UA-68221887-1': '1',
    'OAuth': '1295255121',
    'wr_visit_id': '1295255121',
    'mars': '571cea60c1064eddb514b03f938bcb9a',
    'sessionid': 'wk6174yimlq6hn0dhjlkqahnsdwa596u',
    'dbl': '4e6bc89260dc4d5fbf8bdec6e0fe8670',
    'cted': 'modId%3Dfc97be79%3Bclient_id%3D2019530414.1741701518%3Bya_client_id%3D1741701518760793495',
    '_ct_ids': 'fc97be79%3A17380%3A4794763832',
    '_ct_session_id': '4794763832',
    '_ct_site_id': '17380',
    'call_s': '___fc97be79.1741703320.4794763832.49394:1248368|2___',
    '_ct': '3100000002820627262',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_gali': 'header',
    '_ga_FR9TMQETHP': 'GS1.1.1741701517.1.1.1741701532.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'priority': 'u=1, i',
    'referer': 'https://granelle.ru/flats?is_released=0&view=grid',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-csrftoken': 'cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1',
    # 'cookie': 'csrftoken=cCd0FF01972c4bfac14c71F910B20a7c0f2b336dcBfef8e010F5f982206649C1; _ym_uid=1741701518760793495; _ym_d=1741701518; _ym_isad=2; _ga=GA1.2.2019530414.1741701518; _gid=GA1.2.119258665.1741701518; _ym_visorc=w; _dc_gtm_UA-68221887-1=1; OAuth=1295255121; wr_visit_id=1295255121; mars=571cea60c1064eddb514b03f938bcb9a; sessionid=wk6174yimlq6hn0dhjlkqahnsdwa596u; dbl=4e6bc89260dc4d5fbf8bdec6e0fe8670; cted=modId%3Dfc97be79%3Bclient_id%3D2019530414.1741701518%3Bya_client_id%3D1741701518760793495; _ct_ids=fc97be79%3A17380%3A4794763832; _ct_session_id=4794763832; _ct_site_id=17380; call_s=___fc97be79.1741703320.4794763832.49394:1248368|2___; _ct=3100000002820627262; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _gali=header; _ga_FR9TMQETHP=GS1.1.1741701517.1.1.1741701532.0.0.0',
}

params = {
    'area_max': '',
    'area_min': '',
    'city': '',
    'floor_number_max': '',
    'floor_number_min': '',
    'is_apartments': '',
    'is_black_friday': '',
    'is_business': '',
    'is_coming': '',
    'is_cyber_monday': '',
    'is_profit': '',
    'is_property_of_the_day': '',
    'is_released': '0',
    'is_with_keys': '',
    'limit': '3000',
    'offset': '0',
    'order': '',
    'price_max': '',
    'price_min': '',
    'search': '',
    'withLayouts': 'false',
}

response = requests.get('https://granelle.ru/api/flats/', params=params, cookies=cookies, headers=headers)

flats = []
counter = 1
offset = 0

def extract_digits_or_original(s):
    if s == "Тихий дом":
        return s
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


url = 'https://granelle.ru/api/flats/'
response = requests.get(url, params=params, cookies=cookies, headers=headers)

items = response.json()["results"]

for i in items:
    developer = "Гранель"
    project = i["project"]
    url = f"https://granelle.ru/flats/{i["id"]}"
    oplata = ""
    date = datetime.date.today()
    room_count = i["rooms"]
    area = i["area"]
    price = i["price_discounted"]
    old_price = i["price"]
    if i["finish_type"] == "whitebox":
        finish_type = "Предчистовая отделка"
    elif i["finish_type"] == "finish":
        finish_type = "С отделкой"
    elif i["finish_type"] == "without_finish":
        finish_type = "Без отделки"
    else:
        finish_type = i["finish_type"]
    korpus = i["building"]
    floor = i["floor"]
    floor_count = i["floor_count"]
    completion_till = f"{i["completion_quarter"]} кв {i["completion_year"]} года"
    print(
        f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price},  отделка: {finish_type}, корпус: {korpus}, этаж: {floor}, срок сдачи {completion_till}")
    result = [developer, project, oplata, date, room_count, area, price, old_price, finish_type, korpus, floor, floor_count, completion_till, url]
    flats.append(result)


df = pd.DataFrame(flats, columns=["Застройщик", "Проект", "Способ оплаты", "Дата", "Число комнат", "Площадь", "Актуальная цена", "Старая цена", "Отделка", "Корпус", "Этаж", "Всего этажей", "Заселение до", "URL"])
df.insert(0, 'Row Number', range(1, len(df) + 1))
print(df)

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Granel"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Granel_{current_date}.xlsx"
df.to_excel(filename, index=False)

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
