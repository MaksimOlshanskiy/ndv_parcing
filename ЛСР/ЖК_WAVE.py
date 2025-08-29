import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests
from functions import save_flats_to_excel
from info import cookies, headers, ok

cookies = cookies
headers = headers


if __name__ == "__main__":

    data = {
  'price[min]': '1',
  'price[max]': '99.1',
  'price_range[min]': '1.7',
  'price_range[max]': '99.1',
  'last_delivery': '32',
  'obj[]': ['202', '202'],
  'area[min]': '1',
  'area[max]': '1089',
  'area_range[min]': '1.0',
  'area_range[max]': '1089.0',
  'floor[min]': '1',
  'floor[max]': '99',
  'floor_range[min]': '1',
  'floor_range[max]': '99',
  'ob[page]': '2',
  'ob[sort]': 'price',
  'ob[order]': 'asc',
  'group[t]': 'false',
  'ob[id]': '202',
  'object': '202',
  'a': 'types',
  'ok': ok
}


flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
page_counter = 1

while True:

    response = requests.post('https://www.lsr.ru/ajax/search/msk/', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()
    soup = BeautifulSoup(items['html'], 'html.parser')
    flats_soup = soup.find_all('div', class_=["listingCard listingCard--isFlat", "listingCard--isPromotion"])
    soup2 = BeautifulSoup(items['object_link'], 'html.parser')
    flats_soup2 = soup2.find('a')

    for i in flats_soup:

        url = ''
        date = datetime.date.today()
        project = flats_soup2.text.strip().replace('в ЖК ', '')
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
        try:
            korpus = int(i.find('span', class_= 'label l3').text.strip().split()[1].replace(",", ''))
        except ValueError:
            korpus = i.find('span', class_= 'label l3').text.strip().replace('Wave, ', '')
        konstruktiv = ''
        klass = ''
        if len(all_tags) == 3:
            srok_sdachi = all_tags[0].text.strip()
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
            floor = int(i.find('div', class_= 'listingCard__label').text.strip().split()[4])
        except:
            floor = i.find('div', class_='listingCard__label').text.strip().split()[4]
        flat_number = ''

        print(
            f"{project}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
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