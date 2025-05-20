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
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'is-lotto-banner-hidden': 'true',
    'is-ddd-banner-hidden': 'true',
    'iosAppLink': '',
    'favoriteHintShowed': 'true',
    'qrator_jsr': 'v2.0.1747748922.389.5b6ce31fbmxP4vdH|2o3etwVES0XzOcKC|O+IuYWPeJP6uNrd+OmzpezBVOZyVL2/wO7/LMvi3xaRY+dFAwLzYaHDYLZCy07filvMxqJ89rlTfbi5l0KN0aQ==-jtjL44oJ1+8wDlwVR5wuxbfoaSU=-00',
    'qrator_jsid2': 'v2.0.1747748922.389.5b6ce31fbmxP4vdH|bT7dlgSFk8zgLdc4|yJ4pHZR2X19erbWUGJDaPhc5cpRtKBt4bMbCURgSD57CN3TAqh2ZQaBnMjpkAEs5U0n39eNRC/wZbt5mU26Nx2vvSBywmOEwyQCQ/PlGXYdeorGEMu1L9fl3QkyYcr8NMDdMAaimpH2i5S+vTKIiLQ==-cb5hwMjZNmE1Rv7s2QxM+H+TxJ4=',
    '_ym_isad': '2',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1747748926',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1747748927',
    '_visitId': 'e8f1e9f7-e3a9-4a67-a2d8-e787f42d6bb8-fdf0b4f3aa3cdbac',
    'adrdel': '1747748927840',
    'currentRegionGuid': '435a7bbb-ed9d-45f4-a70f-0fdebcfe9173',
    'currentLocalityGuid': '87950264-09e9-442e-8586-e33d06bb3eec',
    'regionName': '87950264-09e9-442e-8586-e33d06bb3eec:%D0%A1%D0%B8%D0%BC%D1%84%D0%B5%D1%80%D0%BE%D0%BF%D0%BE%D0%BB%D1%8C',
    'tmr_reqNum': '297',
    't3_sid_7711713': 's1.1804275365.1747748926801.1747748949091.36.10.2.1',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; logoSuffix=; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; iosAppAvailable=true; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; _ym_d=1743518289; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; is-lotto-banner-hidden=true; is-ddd-banner-hidden=true; iosAppLink=; favoriteHintShowed=true; qrator_ssid2=v2.0.1747644624.450.59bc7836w5a20kWw|z7NPiMxITvWZpAzA|j5S3t7zqIFhCUYIt8z8QAhapO8JVqv2fDocyN91TsbzK67jFAgDFve0BC1hxb98B7EQ0jw1GM4oLtTgXhtzbgg==-/kRg09h86KSAlbk6sGf6WGxS4bs=; qrator_jsid2=v2.0.1747644621.934.59bc7836PCX0vSY2|m2CZWGda6C8iOJPi|2gkSIXAIsCulDoq3vu1sHJj/07Z9S3zvUkdM5uAAVRc6WN4w1xj2v/sABEDD0VB7KlEhSelyR/D2mR/bBFnV2zqxafrEsJQK5YshKd8T2tDxhWeOJB1x1BhYvdbbgpCa8FhjAPX2jFR9d5GavGeGmg==-W+oYJHyKq9xo1Jr1fRiuLZczhRY=; _ym_isad=2; adrdel=1747644627114; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1747644627; autoDefinedRegion=1d1463ae-c80f-4d19-9331-a1b68a85b553:1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0:; _visitId=e4955cc1-5c3c-436e-96a8-7192a21037ff-f4f0dcc432ac8ba6; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1747644627; t3_sid_7711713=s1.1956016705.1747644627075.1747645541888.33.21.2.1; tmr_reqNum=286',
}

params = {
    'address': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'offset': '0',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'layout',
    'complex_ids': '121959',
    'complex_name': 'ЖК Солнечный город',
    'from_developer': '1',
    'sort_by_tariff_date': '1',
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.json()['result']['items']

    for i in items:

        url = ""
        date = datetime.date.today()
        project = i['complex']['name']
        english = ''
        promzona = ''
        mestopolozhenie = ''
        subway = ''
        distance_to_subway = ''
        time_to_subway = ''
        mck = ''
        distance_to_mck = ''
        time_to_mck = ''
        bkl = ''
        distance_to_bkl = ''
        time_to_bkl = ''
        status = ''
        start = ''
        comment = ''
        developer = 'ООО СЗ "СТРОЙСОЮЗ"'
        okrug = ''
        district = ''
        adress = i['address']['displayName']
        eskrou = ''
        korpus = ''
        konstruktiv = ''
        klass = ''
        quarter = i['complex']['building']['endBuildQuarter']
        year = i['complex']['building']['endBuildYear']
        srok_sdachi = f"{quarter} квартал {year} года"
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['generalInfo']['isApartment'] == False:
            type = 'Квартира'
        else:
            type = "Апартаменты"
        room_count = i['generalInfo']['rooms']
        area = i['generalInfo']['area']
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        price = int(i["price"])
        old_price = ''
        section = ''
        floor = int(i['generalInfo']['maxFloor'])
        flat_number = ''



        if i['developerOffersCount'] > 1:

            web_url = i['path']
            print(web_url)

            driver.get(web_url)
            for name, value in cookies.items():
                cookie_dict = {
                    'name': name,
                    'value': value
                }
                driver.add_cookie(cookie_dict)

            driver.get(web_url)
            time.sleep(4)
            while True:

                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')
                items2 = soup.find_all(class_='tHj6o')
                for item in range(1,len(items2)):

                    y = items2[item]

                    url2 = ""
                    date2 = datetime.date.today()
                    project2 = project
                    english2 = ''
                    promzona2 = ''
                    mestopolozhenie2 = ''
                    subway2 = ''
                    distance_to_subway2 = ''
                    time_to_subway2 = ''
                    mck2 = ''
                    distance_to_mck2 = ''
                    time_to_mck2 = ''
                    bkl2 = ''
                    distance_to_bkl2 = ''
                    time_to_bkl2 = ''
                    status2 = ''
                    start2 = ''
                    comment2 = ''
                    developer2 = developer
                    okrug2 = ''
                    district2 = ''
                    adress2 = adress
                    eskrou2 = ''
                    korpus2 = ''
                    konstruktiv2 = ''
                    klass2 = ''
                    quarter2 = ''
                    year2 = ''
                    srok_sdachi2 = srok_sdachi
                    srok_sdachi_old2 = ''
                    stadia2 = ''
                    dogovor2 = ''
                    type2 = type
                    finish_type2 = y.get_text(separator='!').split('!')[4]
                    room_count2 = room_count
                    area2 = area
                    price_per_metr2 = ''
                    discount2 = ''
                    price_per_metr_new2 = ''
                    price2 = int(y.find(class_= 'VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', ''))
                    old_price2 = ''
                    section2 = ''
                    floor2 = int(y.get_text(separator='!').split('!')[1])
                    flat_number2 = '' # y.find(class_= 'T8vBE').get_text(strip=True)

                    print(
                        f"{project2}, {url2}, дата: {date2}, комнаты: {room_count2}, площадь: {area2}, цена: {price2}, старая цена: {old_price2}, корпус: {korpus2}, этаж: {floor2}")
                    result2 = [date2, project2, english2, promzona2, mestopolozhenie2, subway2, distance_to_subway2, time_to_subway2,
                              mck2,
                              distance_to_mck2, time_to_mck2, distance_to_bkl2,
                              time_to_bkl2, bkl2, status2, start2, comment2, developer2, okrug2, district2, adress2, eskrou2, korpus2,
                              konstruktiv2, klass2, srok_sdachi2, srok_sdachi_old2,
                              stadia2, dogovor2, type2, finish_type2, room_count2, area2, price_per_metr2, old_price2, discount2,
                              price_per_metr_new2, price2, section2, floor2, flat_number2]
                    flats.append(result2)

                try:
                    # Получаем все кнопки с нужным классом
                    buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-3-0-8")
                    next_button = None

                    for btn in buttons:
                        try:
                            # Проверяем, есть ли у кнопки div с нужным вложенным классом
                            btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-3-0-8")
                            next_button = btn
                            break  # нашли нужную кнопку — дальше не ищем
                        except NoSuchElementException:
                            continue

                    if not next_button:
                        print("Кнопка 'вперёд' не найдена")
                        break

                    # Проверяем, не отключена ли она
                    if "pgnt-disabled-835-3-0-8" in next_button.get_attribute("class"):
                        print("Кнопка 'вперёд' неактивна, выходим из цикла")
                        break

                    ActionChains(driver).move_to_element(next_button).perform()
                    next_button.click()
                    print("Переход на следующую страницу")
                    time.sleep(2)

                except Exception as e:
                    print(f"Ошибка при переходе на следующую страницу: {e}")
                    break

        try:
            finish_type = finish_type2
        except:
            finish_type = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)








    params["offset"] = str(int(params["offset"]) + 20)
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        driver.quit()
        break



df = pd.DataFrame(flats, columns=['Дата обновления',
                                  'Название проекта',
                                  'на англ',
                                  'промзона',
                                  'Местоположение',
                                  'Метро',
                                  'Расстояние до метро, км',
                                  'Время до метро, мин',
                                  'МЦК/МЦД/БКЛ',
                                  'Расстояние до МЦК/МЦД, км',
                                  'Время до МЦК/МЦД, мин',
                                  'БКЛ',
                                  'Расстояние до БКЛ, км',
                                  'Время до БКЛ, мин',
                                  'статус',
                                  'старт',
                                  'Комментарий',
                                  'Девелопер',
                                  'Округ',
                                  'Район',
                                  'Адрес',
                                  'Эскроу',
                                  'Корпус',
                                  'Конструктив',
                                  'Класс',
                                  'Срок сдачи',
                                  'Старый срок сдачи',
                                  'Стадия строительной готовности',
                                  'Договор',
                                  'Тип помещения',
                                  'Отделка',
                                  'Кол-во комнат',
                                  'Площадь, кв.м',
                                  'Цена кв.м, руб.',
                                  'Цена лота, руб.',
                                  'Скидка,%',
                                  'Цена кв.м со ск, руб.',
                                  'Цена лота со ск, руб.',
                                  'секция',
                                  'этаж',
                                  'номер'])

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Дом клик"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Стройсоюз_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
