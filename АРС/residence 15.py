import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    '_ym_uid': '1743579187223137904',
    '_ym_d': '1743579187',
    '_ym_isad': '1',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://domoplaner.ru/catalog/302/tCDzeZ/?start=1&domain=aHR0cHM6Ly9yZXNpZGVuY2UtMTUucnU%3D&back=1&state=plans',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1743579187223137904; _ym_d=1743579187; _ym_isad=1',
}

url = 'https://domoplaner.ru/widget-api/widget/302-tCDzeZ/'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("flats", [])

        for i in items:
            count += 1
            date = datetime.date.today()
            project = 'Резиденция 15'
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
            developer = "АРС"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i['house_title'].replace('Корпус ', '')
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = "Апартаменты"

            if i['decoration_id'] == 34:
                finish_type = 'Предчистовая'
            else:
                finish_type = 'Без отделки'

            room_count = i["rooms_sign"]
            if room_count == 'Ст':
                room_count = 'студия'

            area = float(i["area"])
            price_per_metr = ''
            old_price = int(i['price'])
            discount = ''
            price = int(i["price_with_discount"])
            section = int(i['section_title'].replace('Секция ', ''))
            floor = i["floor_number"]
            flat_number = ''

            if old_price == price:
                price = None

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      '', price, section, floor, flat_number]
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
