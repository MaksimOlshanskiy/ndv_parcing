import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Access-Control-Allow-Origin': '*',
    'Connection': 'keep-alive',
    'Referer': 'https://krost.ru/flats/?complex=55,88,28,70,4,69&ordering=price',
    'SOURCE': 'portal',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1743751083649159549; _ym_d=1743751083; scbsid_old=2796070936; _ga=GA1.1.1274104488.1743751085; _ym_isad=1; _ym_visorc=w; _cmg_csstxFWE5=1753353592; _comagic_idxFWE5=10632809528.14928574068.1753353592; sma_session_id=2368837443; SCBfrom=; smFpId_old_values=%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%2C%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%22ecfc7f3c204692d576ab5de3d3ac35c6%22%2C%2202e1ba1ee8deb0160670e41ccf4ee93b%22%2C%22a932251185d3bf41fcd7e2656de279f5%22%5D; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1753353593178; _ga_8TEVL6KS0T=GS2.1.s1753353592$o10$g1$t1753353723$j49$l0$h0; SCBindexAct=4189; sma_index_activity=17378',
}

params = {
    'limit': '12',
    'offset': '0',
    'complex': '55,88,28,70,4,69',
    'ordering': 'price',
}

url = 'https://krost.ru/api/flats/'

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            count += 1
            date = datetime.date.today()
            project = i["complex"].replace('ЖК ', '')
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
            developer = "КРОСТ"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["building"]

            if korpus == '0':
                korpus = '1'

            if project == 'Трилогия CRYSTAL':
                korpus = i["building_name"].replace('Корпус ', '')

            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''

            if len(i["group_type"]) == 2:
                type_ = "Апартаменты"
            elif len(i["group_type"]) == 1:
                type_ = "Квартира"

            if project in ['Wellton Gold']:
                finish_type = 'С отделкой'
            else:
                finish_type = 'Без отделки'

            room_count = i["rooms"]
            area = i["area"]
            price_per_metr = ''
            old_price = i["old_price"]
            discount = ''
            price_per_metr_new = ''
            price = i["price"]
            section = i["section_count"]
            floor = i["floor"]
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
                      stadia, dogovor, type_, finish_type, room_count, area, price_per_metr, old_price, discount,
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

save_flats_to_excel(flats, 'all', developer)
