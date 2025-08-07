import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_gcl_au': '1.1.349332159.1741947090',
    '_ym_uid': '1741947090869811353',
    '_ym_d': '1741947090',
    '_ym_isad': '1',
    '_ga_PW97HH4W4P': 'GS1.1.1741947089.1.0.1741947089.60.0.0',
    '_ym_visorc': 'b',
    'scbsid_old': '2750244825',
    '_ga': 'GA1.2.746598723.1741947090',
    '_gid': 'GA1.2.174849562.1741947090',
    '_gat': '1',
    '_cmg_csstvbmgO': '1741947094',
    '_comagic_idvbmgO': '10403323789.14516093819.1741947090',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'priority': 'u=1, i',
    'referer': 'https://rg-dev.ru/flats/?group=1',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_gcl_au=1.1.349332159.1741947090; _ym_uid=1741947090869811353; _ym_d=1741947090; _ym_isad=1; _ga_PW97HH4W4P=GS1.1.1741947089.1.0.1741947089.60.0.0; _ym_visorc=b; scbsid_old=2750244825; _ga=GA1.2.746598723.1741947090; _gid=GA1.2.174849562.1741947090; _gat=1; _cmg_csstvbmgO=1741947094; _comagic_idvbmgO=10403323789.14516093819.1741947090',
}

response = requests.get('https://rg-dev.ru/api/flats/?page=1&active=1&', cookies=cookies, headers=headers)

url = 'https://rg-dev.ru/api/flats/?page=1&active=1&'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            try:
                count += 1
                date = datetime.date.today()
                project = i["complex"]
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
                developer = "РГ"
                okrug = ''
                district = ''
                adress = ''
                eskrou = ''
                korpus = i["building"]
                konstruktiv = ''
                klass = ''
                srok_sdachi = ''
                srok_sdachi_old = ''
                stadia = ''
                dogovor = ''
                type = i['type']

                if type == 1:
                    type = 'Апартаменты'
                else:
                    type = 'Квартира'

                finish_type = 'Без отделки'
                room_count = i["rooms"]
                area = i["total_square"]
                price_per_metr = ''
                old_price = round(float(i["price"]))
                discount = ''
                price_per_metr_new = ''
                price = round(float(i["actual_price"]))
                section = ''
                floor = i["floor"]
                flat_number = ''

                if old_price == price:
                    price = None

            except:
                continue

            print(
                f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: "
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

project = 'all'
save_flats_to_excel(flats, project, developer)
