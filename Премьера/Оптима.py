import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1742567659625481482',
    '_ym_d': '1742567659',
    'user_id': '1742567659625481482',
    'utm_source': 'null',
    'utm_medium': 'null',
    'utm_campaign': 'null',
    'utm_content': 'null',
    'utm_term': 'null',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cookie-accepted': 'yes',
    'october_session': 'eyJpdiI6IlZXakwyUy9zT0g4bjVIWjhPckp1UHc9PSIsInZhbHVlIjoiajVnUzdOVHZZVlBleTZWZUx6cVd6b3NoN1lQWTBtWk1Jd3pJMVQwcVBEVmpxNk1uUFJoTG5DaEprY2FVUXJFakM1UmNmbm9zRnV1TUtTYVhJVUtNWDdEZG92SVJBVjgvdkwwOE9sTnFwQWpJL3NBUkluVndMYWtDbFVpK2lpTWMiLCJtYWMiOiI3NDJmNjgwYTE3ODA3ZjYwMWIzOTVjYzcwNWJjMWFkY2VjOTVhMmVhNGZjNWMxYjZkZWYzN2E4ZjNkNDI1Mjg5IiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://optima-dom.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://optima-dom.ru/realty?type=residential',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-october-request-handler': 'onPaginate',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ym_uid=1742567659625481482; _ym_d=1742567659; user_id=1742567659625481482; utm_source=null; utm_medium=null; utm_campaign=null; utm_content=null; utm_term=null; _ym_isad=2; _ym_visorc=w; cookie-accepted=yes; october_session=eyJpdiI6IlZXakwyUy9zT0g4bjVIWjhPckp1UHc9PSIsInZhbHVlIjoiajVnUzdOVHZZVlBleTZWZUx6cVd6b3NoN1lQWTBtWk1Jd3pJMVQwcVBEVmpxNk1uUFJoTG5DaEprY2FVUXJFakM1UmNmbm9zRnV1TUtTYVhJVUtNWDdEZG92SVJBVjgvdkwwOE9sTnFwQWpJL3NBUkluVndMYWtDbFVpK2lpTWMiLCJtYWMiOiI3NDJmNjgwYTE3ODA3ZjYwMWIzOTVjYzcwNWJjMWFkY2VjOTVhMmVhNGZjNWMxYjZkZWYzN2E4ZjNkNDI1Mjg5IiwidGFnIjoiIn0%3D',
}

params = {
    'type': 'residential',
}

data = {
    'page': '1',
    'sort_column': 'price',
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://optima-dom.ru/realty', params=params, cookies=cookies, headers=headers, data=data)
    items = response.json()['dv_spaces']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_='realty-card-body')

    for i in flats_soup:
        print(f"Номер страницы: {data['page']}")
        if i.find(class_='realty-card__price-bottom-price').get_text() == 'Зарезервировано':
            continue
        url = ''
        developer = "Премьера"
        project = 'Оптима'
        korpus = i.find(class_='realty-card__subtitle').get_text().strip().replace('Дом ', '')
        section = ''
        type = 'Квартиры'
        finish_type = 'Без отделки'
        if i.find(class_='realty-card__title').get_text().split()[0] == 'Студия':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find(class_='realty-card__title').get_text().split()[0])
        flat_number = ''
        try:
            area = float(i.find(class_='realty-card__title').get_text().split()[1])
        except:
            area = ''
        try:
            old_price = i.find(class_='realty-card__price-bottom-price').get_text().replace(' ₽', '').replace(' ', '')
        except:
            old_price = ''
        try:
            price = ''
        except:
            price = ''
        try:
            floor = i.find(class_='realty-card__title').get_text().split()[2].replace('м2', '')
        except:
            floor = ''


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
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not flats_soup:
        break
    data['page'] = str(int(data['page']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

