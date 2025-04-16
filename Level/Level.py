# не нашёл откуда вытягивать данные об отделке!!!
# запрос filter...

import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'tmr_lvid': 'a5ef860db478f984f83e34d01161b4e1',
    'tmr_lvidTS': '1741763429108',
    'scbsid_old': '2746015342',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    'carrotquest_device_guid': 'e03ae51f-71b5-443a-8be5-2630839609a7',
    'carrotquest_uid': '1926489373600121724',
    'carrotquest_auth_token': 'user.1926489373600121724.50549-b9906febe2aaab4d349cf1594e.bde0e2e8c1b1a0654e7af2596a1945c70880d0e976ef2c72',
    '_gcl_au': '1.1.2022743371.1741763438',
    '_ym_uid': '1741763438149410509',
    '_ym_d': '1741763438',
    '_ga_M5QHFCMEFC': 'deleted',
    'csrftoken': '4VUAWu4g0lSylFlbhfSZgLMAcRjK2c9V',
    '_ga': 'GA1.1.1912290618.1741763428',
    'booking-blocking': 'false',
    'ya_visit_init': '1744105834033',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstvg3wT': '1744105836',
    '_comagic_idvg3wT': '10587514839.14723874639.1744105835',
    'carrotquest_realtime_services_transport': 'wss',
    'domain_sid': 'V3PUXqAC4mgB-tKYkvsR_%3A1744105836263',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDQxMDk0MzYsImlhdCI6MTc0NDEwNTgzNiwianRpIjoiYTI4YmNmMTZmYWUyNDJlMzlhMWU4YzNkOWNiMjVjNzQiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0NDEwNTgzNiwicm9sZXMiOlsidXNlci4kYXBwX2lkOjUwNTQ5LiR1c2VyX2lkOjE5MjY0ODkzNzM2MDAxMjE3MjQiXSwiYXBwX2lkIjo1MDU0OSwidXNlcl9pZCI6MTkyNjQ4OTM3MzYwMDEyMTcyNH0.BjzrSEEc9CXigohijDzegEhXQ7u4h3RRWmd2mtxWXvE',
    'sma_session_id': '2254152602',
    'SCBfrom': '',
    'smFpId_old_values': '%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1744105837533',
    'menu': '%7B%22isFavorite%22%3Afalse%7D',
    'activity': '0|-1',
    'ya_visit_total': '14',
    'carrotquest_closed_part_id': '1946139066638533621',
    'qrator_jsid2': 'v2.0.1744105830.556.5b6ce31fJsLefv4s|QagWL7bnTNcPqrhb|HSqsBA4UJxUypv3X2fhXnmW/yt+hiO3hzq2zvZg7BS9gqxtehCjnMCKeRauNln4OwqgwfNlHDAEZuBaTOX6BBPPC5Vc1CYW1TVAfLh34XIquUneUlJsm1uInvnWm4Nvrp8LXTs7nWP36KMdn/QSoo7GcSJnVPnHLSFdHPeC8jmk=-SfAnMkFee13da649vtdrjorso9Q=',
    'carrotquest_session': 'bz3a0f5r356lcsrpt1x5b7u9vwc9lgna',
    'carrotquest_session_started': '1',
    'pageCount': '11',
    'tmr_detect': '0%7C1744106012106',
    'ya_visit_finished': 'done',
    'ya_visit_total_session': '15',
    'ya_visit_page': '%2Ffilter',
    '_ga_M5QHFCMEFC': 'GS1.1.1744105832.5.1.1744106527.29.0.0',
    'sma_index_activity': '18176',
    'SCBindexAct': '110',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'baggage': 'sentry-environment=production,sentry-public_key=d431fc4e116909199fba6f7f1ecd0f0a,sentry-trace_id=8675b1c9148a46e994c8e5b188cffc14',
    'priority': 'u=1, i',
    'qrator-timestamp': '2025-04-08T10:02:07.202Z',
    'qrator-token': 'c2ee923cec4758cf7fcb18ce84b8740d',
    'qrator-version': '1.0',
    'referer': 'https://level.ru/filter?renovation=0&cardType=vertical',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '8675b1c9148a46e994c8e5b188cffc14-8c5b6cf7dde57e4f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-csrftoken': '4VUAWu4g0lSylFlbhfSZgLMAcRjK2c9V',
    'x-forwarded-host': '',
    # 'cookie': 'tmr_lvid=a5ef860db478f984f83e34d01161b4e1; tmr_lvidTS=1741763429108; scbsid_old=2746015342; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; carrotquest_device_guid=e03ae51f-71b5-443a-8be5-2630839609a7; carrotquest_uid=1926489373600121724; carrotquest_auth_token=user.1926489373600121724.50549-b9906febe2aaab4d349cf1594e.bde0e2e8c1b1a0654e7af2596a1945c70880d0e976ef2c72; _gcl_au=1.1.2022743371.1741763438; _ym_uid=1741763438149410509; _ym_d=1741763438; _ga_M5QHFCMEFC=deleted; csrftoken=4VUAWu4g0lSylFlbhfSZgLMAcRjK2c9V; _ga=GA1.1.1912290618.1741763428; booking-blocking=false; ya_visit_init=1744105834033; _ym_isad=2; _ym_visorc=w; _cmg_csstvg3wT=1744105836; _comagic_idvg3wT=10587514839.14723874639.1744105835; carrotquest_realtime_services_transport=wss; domain_sid=V3PUXqAC4mgB-tKYkvsR_%3A1744105836263; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDQxMDk0MzYsImlhdCI6MTc0NDEwNTgzNiwianRpIjoiYTI4YmNmMTZmYWUyNDJlMzlhMWU4YzNkOWNiMjVjNzQiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0NDEwNTgzNiwicm9sZXMiOlsidXNlci4kYXBwX2lkOjUwNTQ5LiR1c2VyX2lkOjE5MjY0ODkzNzM2MDAxMjE3MjQiXSwiYXBwX2lkIjo1MDU0OSwidXNlcl9pZCI6MTkyNjQ4OTM3MzYwMDEyMTcyNH0.BjzrSEEc9CXigohijDzegEhXQ7u4h3RRWmd2mtxWXvE; sma_session_id=2254152602; SCBfrom=; smFpId_old_values=%5B%22d3885f11f554d9bfaaad76858b685aaa%22%2C%22b0d44eece823d71c253568fc397e79de%22%5D; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1744105837533; menu=%7B%22isFavorite%22%3Afalse%7D; activity=0|-1; ya_visit_total=14; carrotquest_closed_part_id=1946139066638533621; qrator_jsid2=v2.0.1744105830.556.5b6ce31fJsLefv4s|QagWL7bnTNcPqrhb|HSqsBA4UJxUypv3X2fhXnmW/yt+hiO3hzq2zvZg7BS9gqxtehCjnMCKeRauNln4OwqgwfNlHDAEZuBaTOX6BBPPC5Vc1CYW1TVAfLh34XIquUneUlJsm1uInvnWm4Nvrp8LXTs7nWP36KMdn/QSoo7GcSJnVPnHLSFdHPeC8jmk=-SfAnMkFee13da649vtdrjorso9Q=; carrotquest_session=bz3a0f5r356lcsrpt1x5b7u9vwc9lgna; carrotquest_session_started=1; pageCount=11; tmr_detect=0%7C1744106012106; ya_visit_finished=done; ya_visit_total_session=15; ya_visit_page=%2Ffilter; _ga_M5QHFCMEFC=GS1.1.1744105832.5.1.1744106527.29.0.0; sma_index_activity=18176; SCBindexAct=110',
}

params = {
    'project': '',
    'limit': '1000',
    'offset': "0",
}

flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://level.ru/api/filter/', params=params, cookies=cookies, headers=headers)
    items = response.json()["results"]

    for i in items:

        url = f"https://level.ru{i["url"]}"
        date = datetime.date.today()
        project = i["project"]
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
        developer = "Level"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = extract_digits_or_original(i["building_name"])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = ''
        if i['renovation'] == 2:
            finish_type = "Предчистовая"
        elif i['renovation'] == 0:
            finish_type = "Без отделки"
        room_count = int(i["room"])
        area = i["area"]
        price_per_metr = ''
        old_price = i["old_price"]
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        section = int(i["section_title"])
        floor = i["floor"]
        flat_number = ''

        print(
            f"{project}, {url}, дата: {date}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["offset"] = str(int(params["offset"]) + 1000)
    sleep_time = random.uniform(1, 4)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Level"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

