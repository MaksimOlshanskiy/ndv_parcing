import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import time

cookies = {
    'PHPSESSID': 'nL32WRCo91xAU09LwNL8usIjk5AV5MV6',
    '_ym_uid': '1742300286989408380',
    '_ym_d': '1742300286',
    '_ym_visorc': 'w',
    '_ym_isad': '1',
    '_cmg_csst0SbsV': '1742300286',
    '_comagic_id0SbsV': '10065838361.14245631176.1742300285',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://river-park.ru/lots/table/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

base_url = 'https://river-park.ru/ajax/flats/'

flats = []
count = 1
page = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:
    # Обновляем параметр page в params
    params = {
        'page': str(page),
        'cnt': '30',
        'filter[project]': 'Riverpark',
        'filter[special]': '',
        'filter[type]': '',
        'filter[bld]': '',
        'filter[offers]': '',
        'filter[finishing]': '0',
        'sort[sec]': '0',
        'sort[name]': '0',
        'sort[sq]': '0',
        'sort[price]': '1',
        'sort[rooms]': '0',
        'sort[floor]': '0',
        'art_code': 'flat',
    }

    response = requests.get(base_url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("data", [])

        if not items:
            break

        for i in items:
            date = datetime.date.today()
            project = i.get("project", "Unknown")
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
            developer = "Аеон"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i.get("building", "")
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира'
            finish_type = 'Без отделки'
            room_count = i.get("rooms", "")
            area = float(i.get("sq", ""))
            price_per_metr = ''
            try:
                old_price = int(i.get("price", "").replace(' ', ''))
            except:
                old_price = 0
            discount = ''
            price_per_metr_new = ''
            price = ''
            section = i.get("section", "")
            floor = int(i.get("floor", ""))
            flat_number = ''

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

            count += 1
    else:
        print(f'Ошибка: {response.status_code}')
        break

    # Увеличиваем номер страницы
    page += 1

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
