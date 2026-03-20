import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

'''
может не работать с VPN
'''

cookies = {
    '__ddg9_': '150.241.96.148',
    '__ddg1_': 'eUY2v1pnSvVrVA9nrH8x',
    '_cmg_csstytyUc': '1773818312',
    '_comagic_idytyUc': '12406007816.16952278456.1773818312',
    '_ym_uid': '1773818314597776897',
    '_ym_d': '1773818314',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_comagic_idytyUc': '12406008226.16952278901.1773818316',
    '__ddg8_': 'De7jqf3COxEnsCrF',
    '__ddg10_': '1773818963',
    '_cmg_csstytyUc': '1773819081',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://offers.collection-rks.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '__ddg9_=150.241.96.148; __ddg1_=eUY2v1pnSvVrVA9nrH8x; _cmg_csstytyUc=1773818312; _comagic_idytyUc=12406007816.16952278456.1773818312; _ym_uid=1773818314597776897; _ym_d=1773818314; _ym_isad=2; _ym_visorc=w; _comagic_idytyUc=12406008226.16952278901.1773818316; __ddg8_=De7jqf3COxEnsCrF; __ddg10_=1773818963; _cmg_csstytyUc=1773819081',
}

params = {
    "priced": "y",
    "_base.profile": "flats",
    "offset": 0,
    "limit": 50
}

url = 'https://offers.collection-rks.ru/api/realty/offers'


flats = []
count = 1

while True:

    response = requests.get(url, cookies=cookies, headers=headers, params=params)
    print(params['offset'])
    if response.status_code == 200:
        items = response.json()['offers']

        for i in items:
            date = datetime.date.today()
            project = 'Коллекция'
            developer = "РКС Девелопмент"
            korpus = i['building']["value"]
            room_count = i['rooms']['value']
            type = "Квартиры"
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
        time.sleep(0.3)
        params['offset'] = params['offset'] + 50
        if not items:
            break


    else:
        print(f'Ошибка: {response.status_code}')
        has_more_data = False
        break




save_flats_to_excel(flats, project, developer, kvartirografia=False)
