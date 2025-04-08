import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


cookies = {
    'mland_csi_user_id': 'b9dde91d-b7af-48fd-986e-b89ea703c3f3',
    'ns_session': '5011a2ce-40b7-4307-9dff-9fed60e19442',
    '_ym_uid': '1740562161474500875',
    '_ym_d': '1740562161',
    'RETENTION_COOKIES_NAME': 'da71a744b8a7424f8bc56bdf51b4ba8b:TYqJKjhpqh_akDpD7vt-jDOjHx8',
    'sessionId': '1dfe9bca45c844398634e16da44fce02:dBF_qU58ldZE_dfocSYyoxczPX0',
    'UNIQ_SESSION_ID': 'a68756276f814777aa088db760c38ad9:ss86e0wOaMs90EdCxwTUV6aO8RY',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'adtech_uid': '922aa77e-5a11-4674-bbc7-c1d747a45432%3Adomclick.ru',
    'top100_id': 't1.7711713.1593066985.1740562160961',
    'logoSuffix': '',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    '_sv': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'tmr_lvid': 'be20669b799d3b0c2f1ca532743794d3',
    'tmr_lvidTS': '1740562162078',
    'canary-bind-id-985': 'next',
    'favoriteHintShowed': 'true',
    'regionAlert': '1',
    'currentRegionGuid': '9930cc20-32c6-4f6f-a55e-cd67086c5171',
    'currentLocalityGuid': 'ac7f923e-9a06-46c3-8f21-c72ae4ea9cac',
    'regionName': 'ac7f923e-9a06-46c3-8f21-c72ae4ea9cac:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'cookieAlert': '1',
    'qrator_ssid2': 'v2.0.1742560890.331.023ba284zbW14vn4|CEicd1NamYaB7qlW|MJARO8jFNZb0BZxYWcZ1aTvQY0Lm4raFCzRFwq42frVfKEZSdtxJJKI/BJsdskr/gTWHVFcMBxjrdY2BVfNJuw==-Mrz2k1PuoSWP8D8QwJ+GtkSgzpk=',
    'qrator_jsr': 'v2.0.1742560890.331.023ba284zbW14vn4|xlvIBrv4CY2OHgzn|35oCXdG2ka9KvnbY6fkHUopRiTmI4mYhuq1FmSvS0txbUlNha/gDX7NyXnAsoGrQKUyB7O03V1WplUyGTezCxA==-vaDjaw4bAkwoCEIgAdoHhav29iA=-00',
    'qrator_jsid2': 'v2.0.1742560890.331.023ba284zbW14vn4|vLe2Iq2c7diFQiJ8|oUV6JyZNZ18gtFyQBQcjPByCxI2cUGADFrqtMUTNUG8AHX33s9rISk0ucj5lXNPu09zdYYLe7VOLZDFEepEv1gf7TBFBayR2La6Gl8QF7n/p/pmvxLLGGvgdf5MrL9qHX6txDP9F6UILLfequeR6Jw==-Y8sDZmTqEzTiVritpVJrgYLPNxo=',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1742566539',
    '_ym_isad': '2',
    '_visitId': '633d6202-6db4-4d42-a1b1-ea00afdb42cd-f4f0dcc432ac8ba6',
    'adrdel': '1742566539730',
    '_sas': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1742566541',
    't3_sid_7711713': 's1.395297629.1742566539457.1742566634245.4.19.3.1',
    'tmr_reqNum': '52',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'mland_csi_user_id=b9dde91d-b7af-48fd-986e-b89ea703c3f3; ns_session=5011a2ce-40b7-4307-9dff-9fed60e19442; _ym_uid=1740562161474500875; _ym_d=1740562161; RETENTION_COOKIES_NAME=da71a744b8a7424f8bc56bdf51b4ba8b:TYqJKjhpqh_akDpD7vt-jDOjHx8; sessionId=1dfe9bca45c844398634e16da44fce02:dBF_qU58ldZE_dfocSYyoxczPX0; UNIQ_SESSION_ID=a68756276f814777aa088db760c38ad9:ss86e0wOaMs90EdCxwTUV6aO8RY; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; adtech_uid=922aa77e-5a11-4674-bbc7-c1d747a45432%3Adomclick.ru; top100_id=t1.7711713.1593066985.1740562160961; logoSuffix=; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; _sv=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688; adrcid=A0r9KB4fc8duMUv2jPsp-tg; tmr_lvid=be20669b799d3b0c2f1ca532743794d3; tmr_lvidTS=1740562162078; canary-bind-id-985=next; favoriteHintShowed=true; regionAlert=1; currentRegionGuid=9930cc20-32c6-4f6f-a55e-cd67086c5171; currentLocalityGuid=ac7f923e-9a06-46c3-8f21-c72ae4ea9cac; regionName=ac7f923e-9a06-46c3-8f21-c72ae4ea9cac:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; cookieAlert=1; qrator_ssid2=v2.0.1742560890.331.023ba284zbW14vn4|CEicd1NamYaB7qlW|MJARO8jFNZb0BZxYWcZ1aTvQY0Lm4raFCzRFwq42frVfKEZSdtxJJKI/BJsdskr/gTWHVFcMBxjrdY2BVfNJuw==-Mrz2k1PuoSWP8D8QwJ+GtkSgzpk=; qrator_jsr=v2.0.1742560890.331.023ba284zbW14vn4|xlvIBrv4CY2OHgzn|35oCXdG2ka9KvnbY6fkHUopRiTmI4mYhuq1FmSvS0txbUlNha/gDX7NyXnAsoGrQKUyB7O03V1WplUyGTezCxA==-vaDjaw4bAkwoCEIgAdoHhav29iA=-00; qrator_jsid2=v2.0.1742560890.331.023ba284zbW14vn4|vLe2Iq2c7diFQiJ8|oUV6JyZNZ18gtFyQBQcjPByCxI2cUGADFrqtMUTNUG8AHX33s9rISk0ucj5lXNPu09zdYYLe7VOLZDFEepEv1gf7TBFBayR2La6Gl8QF7n/p/pmvxLLGGvgdf5MrL9qHX6txDP9F6UILLfequeR6Jw==-Y8sDZmTqEzTiVritpVJrgYLPNxo=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1742566539; _ym_isad=2; _visitId=633d6202-6db4-4d42-a1b1-ea00afdb42cd-f4f0dcc432ac8ba6; adrdel=1742566539730; _sas=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1742566541; t3_sid_7711713=s1.395297629.1742566539457.1742566634245.4.19.3.1; tmr_reqNum=52',
}



params = {
    'address': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'offset': '20',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'layout',
    'complex_ids': '3195',
    'complex_name': 'ЖК Времена года',
    'from_developer': '1',
    'sort_by_tariff_date': '1'
}

response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies, headers=headers)



flats = []
options = uc.ChromeOptions()
# Дополнительные настройки (опционально)
options.add_argument("--start-maximized")  # Открыть браузер на весь экран
# options.add_argument("--headless")       # Режим без графического интерфейса (может детектиться)
driver = uc.Chrome(options=options)



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
        developer = i["developerName"]
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
        finish_type = ""
        room_count = i['generalInfo']['rooms']
        area = i['generalInfo']['area']
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        old_price = ''

        section = ''
        floor = i['generalInfo']['floors']
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

        if i['developerOffersCount'] > 1:
            more_flats = i['path']
            driver.get(more_flats)
            page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
            soup = BeautifulSoup(page_content, 'html.parser')
            print(soup)
            time.sleep(2)

    params["offset"] = str(int(params["offset"]) + 20)
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
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
base_path = r"/"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Оптима_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
