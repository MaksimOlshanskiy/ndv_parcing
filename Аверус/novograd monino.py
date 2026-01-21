import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://novograd-monino.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://novograd-monino.ru/vybor-po-parametram/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ym_uid=1744123206900568629; _ym_d=1744123206; PHPSESSID=357e91f55a64c3fc346182f89c303632; _ym_isad=1; _ym_visorc=w; marquiz__url_params={}; _cmg_csst9iSd7=1744123207; _comagic_id9iSd7=10111397268.14324116323.1744123207; _pk_id.501.c663=3c9a49e79b510515.1744123207.; _pk_ses.501.c663=1; __hid=019615d8-2a8e-714b-bf8f-7f976c9a1863; __buttonly_id=97872692; marquiz__count-opened_6071edfbeebf400044680aa4=1',
}

data = {
    'type': 'flat',
    'home[]': 'all',
    'facing': 'all',
    'floor_min': '1',
    'floor_max': '7',
    'area_min': '10.1',
    'area_max': '800.7',
    'price_min': '1.8',
    'price_max': '110.9',
    'sort': 'default',
    'rooms_1': 'false',
    'rooms_2': 'false',
    'rooms_3': 'false',
    'sale': 'false',
    'flatFinish': 'false',
    'offset': '0',
    'roomsValidate': 'false',
}

url = 'https://novograd-monino.ru/wp-content/plugins/srt-genplan/components/appartament-search_v2/ajax.php'

flats = []
count = 0

response = requests.post(url, data=data, headers=headers)

if response.status_code == 200:
    print(response.status_code)
    item = response.json()["home"]

    for i in item:
        count += 1
        date = datetime.date.today()
        project = 'Новоград монино'
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
        developer = "Аверус"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = i['home']
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = ''
        finish_type = i['facing']
        room_count = int(i["rooms"])
        type_ = 'Квартира'
        area = float(i["full_area"])
        price_per_metr = ''
        old_price = int(i['price'])
        discount = ''
        price_per_metr_new = ''
        price = int(i["sale_price"])
        section = int(i['section'])
        floor = int(i["floor"])
        flat_number = ''

        if price == 0:
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

else:
    print(f'Ошибка: {response.status_code}')

time.sleep(0.3)

save_flats_to_excel(flats, project, developer)
