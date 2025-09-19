"""
Сначала обновляем куки
Затем меняем в params - complex_ids на нужный
Его можно найти в адресной строке нужного ЖК

Обращать внимание на код кнопки вперёд. Он иногда меняется.
"""

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from functions import save_flats_to_excel

developer = ''
project = ''
area = ''

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

cookies = {
    'ns_session': '5210b38b-2a77-4df9-a428-6405b3065d3d',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'logoSuffix': '',
    'RETENTION_COOKIES_NAME': 'd7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI',
    'sessionId': 'be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE',
    'UNIQ_SESSION_ID': '01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs',
    'iosAppAvailable': 'true',
    'adtech_uid': '5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru',
    'top100_id': 't1.7711713.1405137252.1743518288740',
    '_ym_uid': '1743518289666663600',
    '_ym_d': '1743518289',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '6b6b440680155a4ac17ccaf6a462f603',
    'tmr_lvidTS': '1743518291170',
    'regionAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING': 'true',
    'cookieAlert': '1',
    'iosAppLink': '',
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'qrator_jsr': 'v2.0.1758096935.091.5b6ce31fmozKfdpC|eq1K3nf8f1KDeEey|rMXQ52CLYvp4dI7CCqF8kJ+ReE1/hf79cRVCko8mNWgJB724btPqk7VC3YL/ktNsKfx0ks2h8EjJyBBfhK85qA==-O/qNqne4JwL6PPJgyi18xGEgm3s=-00',
    'qrator_jsid2': 'v2.0.1758096935.091.5b6ce31fmozKfdpC|J3sgK0znYf9AIwBi|X/W+md/IC5VKj3jhf3KezOuUB33/BBQU5k2jfYYqmqjEKIfRss99jcE4RX3l9b0PvnF9jSk0U9hdY9GXX3033VB41n6NKwf7ZHIT811MiXolVkb8MfoDBRr9HNiBsBZv+SUuBKWoHFGQ3UjFlhCkqA==-mZY3EkDNWXGMLqAG4/GRaJas1bM=',
    'currentRegionGuid': '962c3758-8514-4c8f-91fe-aa465d78e56f',
    'currentLocalityGuid': '0d475b79-88de-4054-818c-37d8f9d0d440',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1758096939',
    '_ym_isad': '2',
    'regionName': '0d475b79-88de-4054-818c-37d8f9d0d440:%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3',
    'adrdel': '1758096941145',
    '_visitId': 'dde8c4b7-c6a1-4edc-b751-f8b5872bf6c3-887c3e444c005759',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1758096943',
    't3_sid_7711713': 's1.349673235.1758096940223.1758096955236.6.5.1.1..',
    'tmr_reqNum': '292',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://ekaterinburg.domclick.ru',
    'Referer': 'https://ekaterinburg.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; logoSuffix=; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; iosAppAvailable=true; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; _ym_d=1743518289; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; iosAppLink=; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; qrator_jsr=v2.0.1758096935.091.5b6ce31fmozKfdpC|eq1K3nf8f1KDeEey|rMXQ52CLYvp4dI7CCqF8kJ+ReE1/hf79cRVCko8mNWgJB724btPqk7VC3YL/ktNsKfx0ks2h8EjJyBBfhK85qA==-O/qNqne4JwL6PPJgyi18xGEgm3s=-00; qrator_jsid2=v2.0.1758096935.091.5b6ce31fmozKfdpC|J3sgK0znYf9AIwBi|X/W+md/IC5VKj3jhf3KezOuUB33/BBQU5k2jfYYqmqjEKIfRss99jcE4RX3l9b0PvnF9jSk0U9hdY9GXX3033VB41n6NKwf7ZHIT811MiXolVkb8MfoDBRr9HNiBsBZv+SUuBKWoHFGQ3UjFlhCkqA==-mZY3EkDNWXGMLqAG4/GRaJas1bM=; currentRegionGuid=962c3758-8514-4c8f-91fe-aa465d78e56f; currentLocalityGuid=0d475b79-88de-4054-818c-37d8f9d0d440; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1758096939; _ym_isad=2; regionName=0d475b79-88de-4054-818c-37d8f9d0d440:%D0%95%D0%BA%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D0%B1%D1%83%D1%80%D0%B3; adrdel=1758096941145; _visitId=dde8c4b7-c6a1-4edc-b751-f8b5872bf6c3-887c3e444c005759; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1758096943; t3_sid_7711713=s1.349673235.1758096940223.1758096955236.6.5.1.1..; tmr_reqNum=292',
}

params = {
    'address': '9930cc20-32c6-4f6f-a55e-cd67086c5171',
    'offset': '0',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'townhouse',
    'village_uuids': '1d395017-4e64-4a56-9aa9-45825ef9d2ca',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:

    response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies,
                            headers=headers)
    print(response.status_code)
    items = response.json()['result']['items']

    for i in items:
        try:
            region = i['seoInfo']['displayNameParts'][0]['title']
        except:
            region = i['offerRegionName']

        try:
            house_area = float(i['objectInfo']['area'])
        except:
            house_area = ''
        try:
            uchastok_area = float(i['land']['area'])
        except:
            uchastok_area = ''
        try:
            price = i['price']
        except:
            price = ''
        try:
            poselok = i['village']['name']
        except:
            poselok = ''
        try:
            kp = ''
        except:
            kp = ''
        try:
            property_from = "От застройщика"
        except:
            property_from = ''

        url = ''
        try:
            flours = i['house']['floors']
        except:
            flours = ''

        print(
            f"{region}, {url}, Участок: {uchastok_area}, дом: {house_area}, цена: {price}, посёлок {poselok}, кп: {kp}, объявление {property_from}")
        result = [region, uchastok_area, house_area, price, poselok, kp, property_from, flours, url]
        flats.append(result)

    params["offset"] = str(int(params["offset"]) + 20)
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        driver.quit()
        break

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{region}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['Регион',
                                  'Размер участка',
                                  'Размер дома',
                                  'Цена',
                                  'Посёлок',
                                  'Коттеджный посёлок',
                                  'Объявление от',
                                  'Этажность',
                                  'Ссылка'
                                  ])

# Сохранение файла в папку
df.to_excel(file_path, index=False)
