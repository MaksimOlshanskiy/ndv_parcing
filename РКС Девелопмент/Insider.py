import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    'scbsid_old': '2777220903',
    'tmr_lvid': 'f347782f2edb72a1c122a4ca19bbecba',
    'tmr_lvidTS': '1743163371277',
    '_ym_uid': '1743163371443155248',
    '_ym_d': '1743163371',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstytyUc': '1743163372',
    '_comagic_idytyUc': '10134026036.14326479696.1743163371',
    'domain_sid': 'EZLY56vm-xW3Cvqlh_D4h%3A1743163372343',
    'sma_session_id': '2240923871',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%227f5cf814e808057afe665b09ade31ada%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1743163373046',
    'tmr_detect': '0%7C1743163373777',
    'SCBFormsAlreadyPulled': 'true',
    'SCBindexAct': '2113',
    'sma_index_activity': '3414',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://insiderhome.ru/apartments?priced=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

base_url = 'https://insiderhome.ru/api/realty/offers?priced&_base.status=available,reserved,valuation&_base.profile=a'

flats = []
count = 1
offset = 0
limit = 50  # Можно попробовать увеличить, если сервер позволяет
has_more_data = True

while has_more_data:
    # Формируем URL с текущим offset
    url = f"{base_url}&offset={offset}&limit={limit}"

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("offers", [])

        if not items:
            has_more_data = False
            break

        for i in items:
            date = datetime.date.today()
            project = 'INSIDER'
            developer = "РКС Девелопмент"
            korpus = i['building']["title"]
            room_count = i['rooms']['value']

            if room_count == 0:
                room_count = 'студия'

            type = "Квартира"
            area = i["area"]
            old_price = i['oldPrice']
            price = i["price"]

            if old_price == None:
                old_price = price
                price = None

            if price == None and old_price == None:
                continue

            floor = i["floor"]

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, '', '', '', '', '', '',
                      '',
                      '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', korpus,
                      '', '', '', '',
                      '', '', type, 'С отделкой', room_count, area, '', old_price, '',
                      '', price, '', floor, '']
            flats.append(result)

            count += 1

        # Увеличиваем offset для следующей страницы
        offset += limit

    else:
        print(f'Ошибка: {response.status_code}')
        has_more_data = False
        break

    time.sleep(0.3)

project = 'all'
save_flats_to_excel(flats, project, developer)
