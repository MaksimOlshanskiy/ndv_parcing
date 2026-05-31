import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

cookies = {
    '_ym_uid': '1744356214802326974',
    '_ym_d': '1769512582',
    '_ym_isad': '2',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://domoplaner.ru/catalog/288/UAprmf/plans/?house_id=3686',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1744356214802326974; _ym_d=1769512582; _ym_isad=2',
}

response = requests.get('https://domoplaner.ru/widget-old-api/widget/288-UAprmf/', cookies=cookies, headers=headers)

url = 'https://domoplaner.ru/widget-old-api/widget/288-UAprmf/'

flats = []
count=0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("flats", [])

        for i in items:
            count+=1
            date = datetime.date.today()
            project = 'Port May'
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
            developer = ""
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
            room_count = int(i["rooms"])
            type = i['rooms_sign']

            if type in 'ст':
                room_count='Студия'

            type='Квартиры'
            finish_type="Без отделки"
            area = float(i["area"])
            price_per_metr = ''
            old_price = int(i['price'])

            section = ''
            floor = i["floor_number"]
            flat_number = ''



            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, '',
                      '', '', section, floor, flat_number]
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

save_flats_to_excel(flats, project, developer, kvartirografia=False)