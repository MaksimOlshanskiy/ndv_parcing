import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://novokosino.citi-mix.ru',
    'priority': 'u=1, i',
    'referer': 'https://novokosino.citi-mix.ru/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-device-type': 'desktop',
    'x-site': 'example.com',
}

params = {
    'limit': '10',
    'offset': '0',
    'house_ids': '111054',
    'area_total__gte': '1',
    'area_total__lte': '999.8',
    'min_price__gte': '130000',
    'min_price__lte': '119000099999',
    'ordering': 'price',
}

url = 'https://api.novokosino.citi-mix.ru/api/apartments/properties/'

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            try:
                if i['property_purpose'] == 'commercial':
                    continue
                else:
                    date = datetime.date.today()
                    project = i["project"]['title']
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
                    developer = i["project"]['developer']
                    okrug = ''
                    district = ''
                    adress = ''
                    eskrou = ''
                    korpus = '1'
                    konstruktiv = ''
                    klass = ''
                    srok_sdachi = ''
                    srok_sdachi_old = ''
                    stadia = ''
                    dogovor = ''
                    type = 'Апартаменты'
                    finish_type = 'С отделкой'
                    room_count = ''
                    area = i["area_total"]
                    price_per_metr = ''
                    old_price = i['price']
                    discount = ''
                    price_per_metr_new = i['price_per_meter']
                    price = i['discount_price_value']
                    section = i['section_name_custom']
                    floor = i["floor"]
                    flat_number = ''

                    if price == old_price:
                        price = None

            except:
                continue

            print(
                f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: "
                f"{korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
