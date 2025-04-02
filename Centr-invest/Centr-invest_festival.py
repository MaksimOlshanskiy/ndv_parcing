# запрос к сайту housing....

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'PHPSESSID': 'B2vQ0NUWk8CGWjY3jMdg3AgICTTdKuVl',
    'PRIVACY': '1',
    'tmr_lvid': 'cb890e29ef43e5554ad57ee3ec8401a8',
    'tmr_lvidTS': '1741874377965',
    '_gcl_au': '1.1.1924344410.1741874378',
    '_ym_uid': '1741874378282494327',
    '_ym_d': '1741874378',
    '_ga': 'GA1.2.96155142.1741874378',
    '_gid': 'GA1.2.229136922.1741874378',
    'scbsid_old': '2746015342',
    '_cmg_csstBndh0': '1741874378',
    '_comagic_idBndh0': '10032876911.14206768976.1741874378',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    'domain_sid': 'kzYlcNarj1UsChOHJm6LG%3A1741874378307',
    '_ga_PJJPRF5JJB': 'GS1.2.1741874378.1.1.1741874382.56.0.0',
    'tmr_detect': '0%7C1741874384807',
    'sma_session_id': '2222106647',
    'SCBfrom': 'https%3A%2F%2Fjk-festivalpark.ru%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D',
    'SCBstart': '1741874418952',
    'SCBporogAct': '5000',
    'sma_index_activity': '7279',
    'SCBindexAct': '79',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://jk-festivalpark.ru/flats/parametrical/?page=1&by=price&order=asc&building=24.3,25,27.1,27.2,26,24.2,24.1&price=65%20%D0%BC%D0%BB%D0%BD%20%E2%82%BD&price_from=13&price_to=65&area=131%20%D0%BC2&area_from=22&area_to=131&floor=35%20&floor_from=1&floor_to=35',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'PHPSESSID=B2vQ0NUWk8CGWjY3jMdg3AgICTTdKuVl; PRIVACY=1; tmr_lvid=cb890e29ef43e5554ad57ee3ec8401a8; tmr_lvidTS=1741874377965; _gcl_au=1.1.1924344410.1741874378; _ym_uid=1741874378282494327; _ym_d=1741874378; _ga=GA1.2.96155142.1741874378; _gid=GA1.2.229136922.1741874378; scbsid_old=2746015342; _cmg_csstBndh0=1741874378; _comagic_idBndh0=10032876911.14206768976.1741874378; _ym_visorc=w; _ym_isad=2; domain_sid=kzYlcNarj1UsChOHJm6LG%3A1741874378307; _ga_PJJPRF5JJB=GS1.2.1741874378.1.1.1741874382.56.0.0; tmr_detect=0%7C1741874384807; sma_session_id=2222106647; SCBfrom=https%3A%2F%2Fjk-festivalpark.ru%2F; SCBnotShow=-1; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%5D; SCBstart=1741874418952; SCBporogAct=5000; sma_index_activity=7279; SCBindexAct=79',
}

params = { "page": 1

}

session = requests.Session()



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = session.get(
        'https://jk-festivalpark.ru/local/components/bs-soft/search.apartments/templates/.default/ajax/housingParameter.php?by=price&order=asc&building=24.3,25,27.1,27.2,26,24.2,24.1&price=65%20%D0%BC%D0%BB%D0%BD%20%E2%82%BD&price_from=13&price_to=65&area=131%20%D0%BC2&area_from=22&area_to=131&floor=35%20&floor_from=1&floor_to=35',
        cookies=cookies,
        headers=headers,
        params=params
    )
    print(response.status_code)

    try:
        items = response.json()["list"]
    except:
        break

    for i in items:

        url = f"https://jk-festivalpark.ru{i["url"]}"

        date = datetime.date.today()
        project = "Фестиваль парк"
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
        developer = "Центр-Инвест"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i["parameters"][0]["description"]
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = "Без отделки"
        try:
            room_count = int(i["roominess"])
        except:
            room_count = i["roominess"]
        area = float(i["parameters"][2]["description"].replace(' м2', ''))
        price_per_metr = ''
        try:
            old_price = int(extract_digits_or_original(i["price"]["old"].replace(" ", "")))
        except:
            old_price = 0
        discount = ''
        price_per_metr_new = ''
        try:
            price = int(extract_digits_or_original(i["price"]["new"].replace(" ", "")))
        except:
            price = int(extract_digits_or_original(i["price"]["price"].replace(" ", "")))
        try:
            section = i["sectionTitle"].split()[1].strip().replace(',', '')
        except:
            section = i["sectionTitle"]
        try:
            floor = int(i["parameters"][1]["description"].split()[0])
        except:
            floor = i["parameters"][1]["description"]
        try:
            flat_number = int(i['num'])
        except:
            flat_number = i['title']

        print(
            f"{project}, {url}, {section}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["page"] = int(params["page"]) + 1
    sleep_time = random.uniform(1, 3)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Centr-invest"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)