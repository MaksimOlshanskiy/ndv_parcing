"""

Обновляем куки в файле info, далее они подтягиваются в остальные проекты.
Также нужно обновлять строку 'ок'

"""


import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests
from info import cookies, headers, ok
from functions import save_flats_to_excel


data = {
    "price[min]": 12,
    "price[max]": 39.7,
    "price_range[min]": 12.0,
    "price_range[max]": 39.7,
    "last_delivery": 32,
    "obj[]": [207, 207],
    "area[min]": 21,
    "area[max]": 79,
    "area_range[min]": 21.0,
    "area_range[max]": 79.0,
    "floor[min]": 2,
    "floor[max]": 32,
    "floor_range[min]": 2,
    "floor_range[max]": 32,
    "ob[page]": 1,
    "ob[sort]": "price",
    "ob[order]": "asc",
    "group[t]": "false",
    "ob[id]": 207,
    "object": 207,
    "a": "types",
    "ok": ok
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
        project = "Дмитровское небо"

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
        listingCard = i.find('div', class_= 'listingCard__label').find_all(class_= 'label l3')

        korpus = listingCard[0].text
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        if len(all_tags) == 3:
            srok_sdachi = ''
            if all_tags[2].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[1].text.strip()} и доп опциями"
            else:
                finish_type = all_tags[1].text.strip()
        else:
            srok_sdachi = ''
            if all_tags[1].text.strip() == "С меблировкой":
                finish_type = f"{all_tags[0].text.strip()} и доп опциями"
            else:
                finish_type = all_tags[0].text.strip()

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'

        if i.find('span', class_="h4").text.strip().split()[0] == "Студия":
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
            floor = i.find('div', class_= 'listingCard__label').text.strip().split()[-3]
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