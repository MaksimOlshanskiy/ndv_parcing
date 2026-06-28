import datetime
import time
import random
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://forma.ru',
    'priority': 'u=1, i',
    'referer': 'https://forma.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

json_data = {
    'price': {},
    'area': {},
    'floor': {},
    'attributes': [],
    'page': 1,
    'limit': 750,
    'order': {
        'key': 'price',
        'type': 'asc',
    },
    'type': 4,
    'objectType': 'flat',
    'ceilingHeight': {},
}

flats = []

response = requests.post('https://manager.forma.ru/api/v2/marketplace', headers=headers, json=json_data)


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


items = response.json().get("flats", [])

count = 0
for i in items:
    count += 1
    date = datetime.date.today()
    project = i["ProjectName"]
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
    developer = "Форма"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    korpus = str(i["bulk"]["number"]).replace(',', '.')
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = f'{i['bulk']['settlement_quarter']} кв {i["bulk"]["settlement_year"]}'
    stadia = ''
    dogovor = ''
    type = 'Квартира'
    finish_type = ''
    if isinstance(i.get("rooms"), int):
        room_count = i["rooms"]
    else:
        room_count = 'студия'
    area = i["area"]
    price_per_metr = ''
    old_price = i["real_price"]
    discount = ''
    price_per_metr_new = ''
    price = i["currentPrice"]
    section = i["bulk"]["settlement_quarter"]
    floor = i["section"]["number"]
    flat_number = ''

    if old_price == price:
        price = None

    print(
        f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, срок сдачи: {srok_sdachi_old}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
              distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
              konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
              price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)

sleep_time = random.uniform(3, 15)
time.sleep(sleep_time)

save_flats_to_excel(flats, 'all', developer)
