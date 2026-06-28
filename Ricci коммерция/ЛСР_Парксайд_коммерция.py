import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

from functions import save_flats_to_excel
from info import cookies, headers, ok
import requests

cookies = cookies
headers = headers

data = {
    "premiseType": "5",
    "ob[page]": "1",
    "ob[sort]": "price",
    "ob[order]": "asc",
    "group[t]": "false",
    "ob[id]": "152",
    "object": "152",
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
    flats_soup = soup.find_all('div', class_=["listingCard listingCard--isCommerce"])
    for i in flats_soup:

        url = ''

        date = datetime.date.today()
        project = "Парксайд"

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
        spans = soup.select("div.listingCard__label span.label.l3")
        korpus = spans[1].get_text(strip=True) if len(spans) > 1 else None
        if korpus == '(этап':
            korpus = '15'
        konstruktiv = ''
        klass = ''
        srok_sdachi = all_tags[0].text.strip()
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        finish_type = ''
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
        floor = spans[2].get_text(strip=True).split('/')[0].replace('эт. ', '').strip() if len(spans) > 1 else None
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
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)