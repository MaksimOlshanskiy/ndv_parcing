import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random


cookies = {
    'ma_cid': '4056384301741529079',
    '_ym_uid': '1741529079657008183',
    '_ym_d': '1741529079',
    'ma_id': '2449120181727944913463',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'tmr_lvid': '3c7be473357935db09f70107466955c5',
    'tmr_lvidTS': '1741529080285',
    '_pk_id.6528.26a3': 'ded68cab7079fc01.1741529081.',
    'cookies-accepted': 'true',
    'sessionid': 'j44xe7i90o4v2ynq2ckmu16i26d23l18',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742569373606%2C%22sl%22%3A%7B%22224%22%3A1742482973606%2C%221228%22%3A1742482973606%7D%7D',
    'adrdel': '1742482973747',
    '_ym_visorc': 'w',
    '_ym_isad': '1',
    'domain_sid': 'M3dKBsVK_O6q7BxuLMInj%3A1742482976464',
    '_pk_ref.6528.26a3': '%5B%22%22%2C%22%22%2C1742482977%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D',
    '_pk_ses.6528.26a3': '1',
    'tmr_detect': '0%7C1742482978237',
    '_cmg_csstexsNi': '1742482979',
    '_comagic_idexsNi': '10447800279.14566365434.1742482978',
    'flats_filter': '%7B%22standard%22%3A%5B%5D%2C%22complex%22%3A%5B%5D%2C%22building%22%3A%5B%5D%2C%22construction_queue%22%3A%5B%5D%2C%22rooms%22%3A%5B%5D%2C%22basic_kitchen_set%22%3A%22%22%2C%22smart_home%22%3A%22%22%2C%22finish%22%3A%5B%5D%2C%22price_min%22%3A%22%22%2C%22price_max%22%3A%22%22%2C%22discount%22%3A%22%22%2C%22area_min%22%3A%22%22%2C%22area_max%22%3A%22%22%2C%22completion_year%22%3A%5B%5D%2C%22finishing%22%3A%22%22%2C%22features%22%3A%5B%5D%2C%22layout%22%3A%5B%5D%2C%22window_view%22%3A%5B%5D%2C%22purchase%22%3A%5B%5D%2C%22booked%22%3A%22%22%2C%22viewed%22%3A%22%22%2C%22floor_min%22%3A%22%22%2C%22floor_max%22%3A%22%22%2C%22section_number%22%3A%22%22%7D',
    'ma_ss_0ad81644-92d8-17a2-8192-d8c7a20d0000': '5425822211742482974.3.1742482992.7',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://sbercity.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'ma_cid=4056384301741529079; _ym_uid=1741529079657008183; _ym_d=1741529079; ma_id=2449120181727944913463; adrcid=A0r9KB4fc8duMUv2jPsp-tg; tmr_lvid=3c7be473357935db09f70107466955c5; tmr_lvidTS=1741529080285; _pk_id.6528.26a3=ded68cab7079fc01.1741529081.; cookies-accepted=true; sessionid=j44xe7i90o4v2ynq2ckmu16i26d23l18; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1742569373606%2C%22sl%22%3A%7B%22224%22%3A1742482973606%2C%221228%22%3A1742482973606%7D%7D; adrdel=1742482973747; _ym_visorc=w; _ym_isad=1; domain_sid=M3dKBsVK_O6q7BxuLMInj%3A1742482976464; _pk_ref.6528.26a3=%5B%22%22%2C%22%22%2C1742482977%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.6528.26a3=1; tmr_detect=0%7C1742482978237; _cmg_csstexsNi=1742482979; _comagic_idexsNi=10447800279.14566365434.1742482978; flats_filter=%7B%22standard%22%3A%5B%5D%2C%22complex%22%3A%5B%5D%2C%22building%22%3A%5B%5D%2C%22construction_queue%22%3A%5B%5D%2C%22rooms%22%3A%5B%5D%2C%22basic_kitchen_set%22%3A%22%22%2C%22smart_home%22%3A%22%22%2C%22finish%22%3A%5B%5D%2C%22price_min%22%3A%22%22%2C%22price_max%22%3A%22%22%2C%22discount%22%3A%22%22%2C%22area_min%22%3A%22%22%2C%22area_max%22%3A%22%22%2C%22completion_year%22%3A%5B%5D%2C%22finishing%22%3A%22%22%2C%22features%22%3A%5B%5D%2C%22layout%22%3A%5B%5D%2C%22window_view%22%3A%5B%5D%2C%22purchase%22%3A%5B%5D%2C%22booked%22%3A%22%22%2C%22viewed%22%3A%22%22%2C%22floor_min%22%3A%22%22%2C%22floor_max%22%3A%22%22%2C%22section_number%22%3A%22%22%7D; ma_ss_0ad81644-92d8-17a2-8192-d8c7a20d0000=5425822211742482974.3.1742482992.7',
}

params = {
    'limit': '12',
    'offset': '12',
}



today = '2025-03-20'


flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://sbercity.ru/api/v1/api/flats/', params=params, cookies=cookies, headers=headers)

    items = response.json()["results"]

    for i in items:

        if i['status'] == 2:    # отфильтровываем забронированные квартиры
            continue

        url = ""

        date = today
        project = 'Сберсити'
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
        developer = "СЗ Рублево-Архангельское"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = f"Квартал {i['complex_name']}, {i['standard']}, корпус {i['building_number']}"
        konstruktiv = ''
        klass = ''
        srok_sdachi = f'{i["complex_finish_quarter"]} кв, {i["complex_finish_year"]} года'
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['type'] == "flat":
            type = 'Квартира'
        else:
            type = ''
        if i["finish"]:
            finish_type = "С отделкой"
        else:
            finish_type = "Без отделки"
        if i["euro"]:
            room_count = f'E-{i["rooms"]}'
        else:
            room_count = int(i["rooms"])
        area = i["area"]
        price_per_metr = ''
        price = i['original_price']
        old_price = ""
        discount = ''
        price_per_metr_new = ''

        section = int(i['section_number'])
        floor = i["floor_number"]
        flat_number = int(i['number'])

        print(
            f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params["offset"] = str(int(params["offset"]) + 12)
    sleep_time = random.uniform(5, 15)
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

current_date = today

# Базовый путь для сохранения
base_path = r"C:\PycharmProjects\SeleniumParcer\СЗ Рублево-Архангельское"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

