import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'origin': 'https://bruno-vemz.ru',
    'priority': 'u=1, i',
    'referer': 'https://bruno-vemz.ru/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
}

params = {
    'storepartuid': '163572716012',
    'recid': '893357461',
    'c': '1773925205542',
    'slice': '1',
    'filters[quantity]': 'y',
    'getparts': 'true',
    'sort[price]': 'asc',
    'size': '20',
    'flag_root': 'withroot',
}


url = 'https://store.tildaapi.com/api/getproductslist/'

flats = []

while True:

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("products", [])

        for i in items:
            date = datetime.date.today()
            project = 'Бруно'
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
            developer = "ВЭМЗ-Эстейт"
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
            type = 'Квартиры'
            finish_type = i["characteristics"][2]["value"]
            room_count = 'студия'
            area = float(i["characteristics"][0]["value"])
            price_per_metr = ''
            try:
                old_price = float(i['priceold'].strip().replace('.0000', ''))
            except:
                old_price = ''
            discount = ''
            price_per_metr_new = ''
            try:
                price = float(i["price"].replace('.0000', ''))
            except:
                price = ''
            section = ''

            flat_number = str(i['title'].replace(' ', '').replace('№', ''))
            floor = i["characteristics"][3]["value"]
            flat_number = ''

            if old_price == '':
                old_price = price
                price = None

            print(
                f"{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        if not items:
            break

        params['slice'] = str(int(params['slice'])+ 1)

    else:
        print(f'Ошибка: {response.status_code}')

time.sleep(0.3)

save_flats_to_excel(flats, project, developer, kvartirografia=False)
