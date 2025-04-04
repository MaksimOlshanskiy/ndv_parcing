import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'nvs': 'eyJpdiI6ImZpYkg3MjMrSVA1RGRnNGlKZ0lURlE9PSIsInZhbHVlIjoiZ3AzYytZckM3MVdIT2pIQlpFZE5JUjlkb1dzaWxlT0ZMNDV6Q0N4Q3hBd3dJNUlkM2ROSW9rQ3F1VkZXYU44ZiIsIm1hYyI6IjY5NTBlYTcyYWM3YWU4OTI3NjE3ZTI2NDAzOWJlNDRlMGU3MmUxZTcxY2ZkZTdiMjZlMmM4YTk3YjQ4MThhYTIiLCJ0YWciOiIifQ%3D%3D',
    'tmr_lvid': '3f51c4a387d0b10a119be4828321b6d7',
    'tmr_lvidTS': '1743585772981',
    '_ym_uid': '1743585773110474590',
    '_ym_d': '1743585773',
    '_ym_visorc': 'w',
    'cted': 'modId%3D0xaodku7%3Bya_client_id%3D1743585773110474590',
    '_ym_isad': '2',
    '_ct_ids': '0xaodku7%3A72830%3A50946372',
    '_ct_session_id': '50946372',
    '_ct_site_id': '72830',
    '_ct': '3000000000036739589',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'domain_sid': 'qR1JSEXdynT2Ef7w2hCSV%3A1743585774756',
    'call_s': '___0xaodku7.1743589349.50946372.454194:1283573|2___',
    'tmr_detect': '0%7C1743587551854',
    'XSRF-TOKEN': 'eyJpdiI6IjBrd3B3Y3FhSm5INzYyeStYZXYxRGc9PSIsInZhbHVlIjoiRDMrSVNudCtlT0FNL0tGM1NabWVvSHFjYlNObndJSWFhcjFUTUJDU05OMDlpaUVQOXNYSnZ0Q2pDR2JKeHE1WHV1WGU5WExBc0tsOWNmMnh5ZmFFcFcvRUMyOGQ4WEY2dWJ6VW0vMWFHZGNFdEcwNG1lTDM4V1p6aVdZQ256djAiLCJtYWMiOiI2M2QwNjhhNTg3YTY0YWQ1ZDlmMTFlYWE4NWI5MzQzN2JmNTBlNzdmYWRmZDgxMWM0MjEwZWI4NzZjMWZiODZjIiwidGFnIjoiIn0%3D',
    'iakovlevo_session': 'eyJpdiI6InRoclV0d3YrVXk1a3V2SjVUY2pWbFE9PSIsInZhbHVlIjoiVkdCVXB5d3VBQVhETmltbnZQdkE1QWZ5RlZIaWZqRlJCMTFNUDBGM1RNVVNDTTI2eGF4OFRBSWdkZ1dOTGRxNVZ1VFlOK2oxNVRsbDk1NWtFRnlZaWx0UGFqMFdWak9OeS9WbWFYaEUxQjd5TTBac3hkWTZlZTJhd2tDQ3lGdG0iLCJtYWMiOiIwOGYyYmU5YjljYzBjZjBjYmZkYWJkNzRkODM3Yzg1ZDEyODVhOTJjNjA0ZmY4NmUwMmQ0ZDBhN2NiNjZkMjhlIiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary5hTkXHXEhMheqW5C',
    'origin': 'https://xn----dtbalcybjze4p.xn--p1ai',
    'priority': 'u=1, i',
    'referer': 'https://xn----dtbalcybjze4p.xn--p1ai/kvartiry?page=4',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': 'eyJpdiI6IjBrd3B3Y3FhSm5INzYyeStYZXYxRGc9PSIsInZhbHVlIjoiRDMrSVNudCtlT0FNL0tGM1NabWVvSHFjYlNObndJSWFhcjFUTUJDU05OMDlpaUVQOXNYSnZ0Q2pDR2JKeHE1WHV1WGU5WExBc0tsOWNmMnh5ZmFFcFcvRUMyOGQ4WEY2dWJ6VW0vMWFHZGNFdEcwNG1lTDM4V1p6aVdZQ256djAiLCJtYWMiOiI2M2QwNjhhNTg3YTY0YWQ1ZDlmMTFlYWE4NWI5MzQzN2JmNTBlNzdmYWRmZDgxMWM0MjEwZWI4NzZjMWZiODZjIiwidGFnIjoiIn0=',
    # 'cookie': 'nvs=eyJpdiI6ImZpYkg3MjMrSVA1RGRnNGlKZ0lURlE9PSIsInZhbHVlIjoiZ3AzYytZckM3MVdIT2pIQlpFZE5JUjlkb1dzaWxlT0ZMNDV6Q0N4Q3hBd3dJNUlkM2ROSW9rQ3F1VkZXYU44ZiIsIm1hYyI6IjY5NTBlYTcyYWM3YWU4OTI3NjE3ZTI2NDAzOWJlNDRlMGU3MmUxZTcxY2ZkZTdiMjZlMmM4YTk3YjQ4MThhYTIiLCJ0YWciOiIifQ%3D%3D; tmr_lvid=3f51c4a387d0b10a119be4828321b6d7; tmr_lvidTS=1743585772981; _ym_uid=1743585773110474590; _ym_d=1743585773; _ym_visorc=w; cted=modId%3D0xaodku7%3Bya_client_id%3D1743585773110474590; _ym_isad=2; _ct_ids=0xaodku7%3A72830%3A50946372; _ct_session_id=50946372; _ct_site_id=72830; _ct=3000000000036739589; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; domain_sid=qR1JSEXdynT2Ef7w2hCSV%3A1743585774756; call_s=___0xaodku7.1743589349.50946372.454194:1283573|2___; tmr_detect=0%7C1743587551854; XSRF-TOKEN=eyJpdiI6IjBrd3B3Y3FhSm5INzYyeStYZXYxRGc9PSIsInZhbHVlIjoiRDMrSVNudCtlT0FNL0tGM1NabWVvSHFjYlNObndJSWFhcjFUTUJDU05OMDlpaUVQOXNYSnZ0Q2pDR2JKeHE1WHV1WGU5WExBc0tsOWNmMnh5ZmFFcFcvRUMyOGQ4WEY2dWJ6VW0vMWFHZGNFdEcwNG1lTDM4V1p6aVdZQ256djAiLCJtYWMiOiI2M2QwNjhhNTg3YTY0YWQ1ZDlmMTFlYWE4NWI5MzQzN2JmNTBlNzdmYWRmZDgxMWM0MjEwZWI4NzZjMWZiODZjIiwidGFnIjoiIn0%3D; iakovlevo_session=eyJpdiI6InRoclV0d3YrVXk1a3V2SjVUY2pWbFE9PSIsInZhbHVlIjoiVkdCVXB5d3VBQVhETmltbnZQdkE1QWZ5RlZIaWZqRlJCMTFNUDBGM1RNVVNDTTI2eGF4OFRBSWdkZ1dOTGRxNVZ1VFlOK2oxNVRsbDk1NWtFRnlZaWx0UGFqMFdWak9OeS9WbWFYaEUxQjd5TTBac3hkWTZlZTJhd2tDQ3lGdG0iLCJtYWMiOiIwOGYyYmU5YjljYzBjZjBjYmZkYWJkNzRkODM3Yzg1ZDEyODVhOTJjNjA0ZmY4NmUwMmQ0ZDBhN2NiNjZkMjhlIiwidGFnIjoiIn0%3D',
}

params = {

    'page': '1',

}


session = requests.Session()


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:
    response = session.post('https://xn----dtbalcybjze4p.xn--p1ai/api', cookies=cookies, headers=headers, params=params)

    print(response.status_code)  # Код ответа (200, 404, 500 и т. д.)
    print(response.headers.get('Content-Type'))  # Тип содержимого ответа
    print(response.text)  # Первые 1000 символов ответа
    items = response.json()['data']

    for i in items:

        url = i['link']

        date = datetime.date.today()
        project = "Яковлево"
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
        developer = "Монарх"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = extract_digits_or_original(i['corpus'])
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартира'
        finish_type = 'С отделкой'
        if i['name'] == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i['name'])
        area = i["area"]
        price_per_metr = ''
        try:
            old_price = int(i['old_price'])
        except:
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        price = i["price"]
        section = ''
        floor = extract_digits_or_original(i["floor"])
        flat_number = i['number']

        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    params['page'] = str(int(params['page']) + 1)
    if not items:
        break
    print('------------------------------------------------------')


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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Монарх"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)
