import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far

cookies = {
    '_ym_uid': '1744366056493324114',
    '_ym_d': '1758885660',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'laravel_session': 'eyJpdiI6IjhlUWxtZVVoVDJXVEx5VERoVVB6T2c9PSIsInZhbHVlIjoiTVA5NzgzN2xmcjBYN2VtUXEvb3p6REdhREl5MlNyRnJVVVRXSHRHQkJHVk5VcDhCOWQzUUlMWjZEQitIZVRwdG9hdHZJU2NxYkNMUjZ2a0Z2aW1MU0pnSUtTMGM1bGNaQ3RYSkJvdmQwRFZ2UUNCT1ZGemdaSS92bkFhMkFpWlQiLCJtYWMiOiI1Mjk1YjU5OTg1OTE0ZDM2ZWU0YTA2Zjg4NzQxMGU4ZDEzM2JkNDU5OGEzZTBmZTRjYjcxYWM3NWIyNmQ4OWMxIiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://rk-gazsetservis.ru/catalog/1',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744366056493324114; _ym_d=1758885660; _ym_isad=2; _ym_visorc=w; laravel_session=eyJpdiI6IjhlUWxtZVVoVDJXVEx5VERoVVB6T2c9PSIsInZhbHVlIjoiTVA5NzgzN2xmcjBYN2VtUXEvb3p6REdhREl5MlNyRnJVVVRXSHRHQkJHVk5VcDhCOWQzUUlMWjZEQitIZVRwdG9hdHZJU2NxYkNMUjZ2a0Z2aW1MU0pnSUtTMGM1bGNaQ3RYSkJvdmQwRFZ2UUNCT1ZGemdaSS92bkFhMkFpWlQiLCJtYWMiOiI1Mjk1YjU5OTg1OTE0ZDM2ZWU0YTA2Zjg4NzQxMGU4ZDEzM2JkNDU5OGEzZTBmZTRjYjcxYWM3NWIyNmQ4OWMxIiwidGFnIjoiIn0%3D',
}

url = 'https://rk-gazsetservis.ru/catalog/api/catalog_free/?complexId[]=1&price[]=6214000&price[]=9196000&turnId[]=0&tab[]=filter'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



response = requests.get(
    'https://rk-gazsetservis.ru/api/catalog/list?viewId[]=1&statusId[]=1&complexId[]=5',
    cookies=cookies,
    headers=headers,
)
print(response.status_code)

if response.status_code == 200:
    items = response.json()['list']

    for i in items:
        count += 1
        date = datetime.date.today()
        project = 'Донской (Коломна)'
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
        developer = "РК-Газсетьсервис"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = i['_type']['title']
        finish_type = 'Предчистовая'
        room_count = int(i["room"]['title'])
        area = float(i["area"])
        price_per_metr = ''
        if i['price'][0]['valueOld']:
            old_price = i['price'][0]['valueOld']
            price = i['price'][0]['value']
        else:
            price = i['price'][0]['value']
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        floor = i['floor']['title']
        flat_number = ''
        section = ''
        korpus = i['turn']['title'].replace('Позиция ', '')

        print(
            f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area},  корпус: {korpus}, секция: {section}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                  mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, '', section, floor, flat_number]
        flats.append(result)

save_flats_to_excel(flats, project, developer)
