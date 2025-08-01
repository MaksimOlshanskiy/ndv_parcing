import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

from functions import save_flats_to_excel
from ЖК_WAVE import cookies, headers
import requests

cookies = cookies
headers = headers

data = {
    'last_delivery': '30',
    'price[min]': '1',
    'price[max]': '99',
    'price_range[min]': '1',
    'price_range[max]': '99',
    'obj[]': ['52', '52'],
    'area[min]': '1',
    'area[max]': '999',
    'area_range[min]': '1',
    'area_range[max]': '999',
    'floor[min]': '1',
    'floor[max]': '99',
    'floor_range[min]': '1',
    'floor_range[max]': '99',
    'ob[page]': '1',
    'ob[sort]': 'price',
    'ob[order]': 'asc',
    'group[t]': 'false',
    'ob[id]': '52',
    'object': '52',
    'a': 'types',
    'ok': 'AOh62eYGcl8tIk4c4IknAX6vrqvI106z'
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://www.lsr.ru/ajax/search/msk/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['html']
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('div', class_=["listingCard listingCard--isFlat", "listingCard--isPromotion"])
    for i in flats_soup:

        url = ''

        date = datetime.date.today()
        project = "Лучи"

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
        developer = "ЛСР"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        all_tags = i.find_all('div', class_='tag tag--isSmall')
        korpus = i.find('div', class_= 'listingCard__label').text.strip().split()[1]
        if korpus == '(этап':
            korpus = '15'
        konstruktiv = ''
        klass = ''
        srok_sdachi = all_tags[0].text.strip()
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'

        if all_tags[2].text.strip() == "С меблировкой":
            finish_type = f"{all_tags[1].text.strip()} и доп опциями"
        else:
            finish_type = all_tags[1].text.strip()
        if i.find('span', class_= "h4").text.strip().split()[0] == "Студия":
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('span', class_= "h4").text.strip().split()[0])
        area = float(i.find('span', class_='h4 isColorSilverChalice isTextNoWrap').text.strip().split(' ')[0])
        price_per_metr = ''
        old_price = extract_digits_or_original(i.find('span', class_= 'h4 isHiddenInGrid').text)
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        try:
            floor = int(i.find('div', class_= 'listingCard__label').text.strip().split()[5])
        except:
            floor = i.find('div', class_='listingCard__label').text.strip().split()[5]
        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

    data['ob[page]'] = str(int(data['ob[page]']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)