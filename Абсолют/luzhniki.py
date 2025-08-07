import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

cookies = {
    'lang': 'ru',
    '_ga_V1F69ETEV0': 'GS1.1.1743520578.1.0.1743520578.0.0.0',
    '_ga': 'GA1.1.593385048.1743520579',
    '_ym_uid': '1743520579344394064',
    '_ym_d': '1743520579',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_cmg_cssta5C3Q': '1743520580',
    '_comagic_ida5C3Q': '10160399376.14357532186.1743520579',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'access-control-allow-origin': '*',
    'priority': 'u=1, i',
    'referer': 'https://luzhniki-collection.ru/flats?order=price_rub&or_filter=is_penthouse%3Atrue%7Cbedrooms_count%3A1,2,3,4&finish_types=true,false',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'lang=ru; _ga_V1F69ETEV0=GS1.1.1743520578.1.0.1743520578.0.0.0; _ga=GA1.1.593385048.1743520579; _ym_uid=1743520579344394064; _ym_d=1743520579; _ym_isad=1; _ym_visorc=w; _cmg_cssta5C3Q=1743520580; _comagic_ida5C3Q=10160399376.14357532186.1743520579',
}

params = {
    'limit': '9',
    'offset': '0',
    'order': 'price_rub',
}

url = 'https://luzhniki-collection.ru/api/flats/'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            date = datetime.date.today()
            project = 'LUZHNIKI'
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
            developer = "Абсолют"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = f'{i["building_class"]} {i['building_number'].replace('HL', '').replace('G', '').replace('W', '')}'
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = ''
            finish_type = i['facing']

            if finish_type == False:
                finish_type = 'Без отделки'
            else:
                finish_type = 'Предчистовая'

            room_count = i["bedrooms_count"]
            type = 'Квартира'
            area = float(i["area"])
            price_per_metr = ''
            old_price = int(i["price_rub"])
            discount = ''
            price_per_metr_new = ''
            price = ''
            section = i['section_number']
            floor = i["floor"]
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
