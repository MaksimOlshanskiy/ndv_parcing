import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    '_ym_uid': '1745588587879864524',
    '_ym_d': '1745588587',
    'session': 'a41afb65e733b55a0948028f26b067698d958da9698dd5000c0f86ccbab9ff16',
    'kbSession': '17536851674130544',
    'kbCreated': 'Mon, 28 Jul 2025 06:46:10 GMT',
    'kbRes': 'false',
    'kbLoaded': 'true',
    'kbCheck': 'c6c15e4612e8ec49ad1613f2e70db097',
    'kbT': 'false',
    'kbUserID': '45138542917232978',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://xn-----elchiocal7aidb7bq1d.xn--p1ai/flats',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'X-Host': 'xn-----elchiocal7aidb7bq1d.xn--p1ai',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1745588587879864524; _ym_d=1745588587; session=a41afb65e733b55a0948028f26b067698d958da9698dd5000c0f86ccbab9ff16; kbSession=17536851674130544; kbCreated=Mon, 28 Jul 2025 06:46:10 GMT; kbRes=false; kbLoaded=true; kbCheck=c6c15e4612e8ec49ad1613f2e70db097; kbT=false; kbUserID=45138542917232978; _ym_isad=1; _ym_visorc=w',
}


params = {
    'project_id': '1f155aae-9cbe-43af-8a4b-f48b666d4d4e',
    'offset': 0,
    'limit': 16,
}

flats = []
count = 0

while True:
    try:
        response = requests.get('https://xn-----elchiocal7aidb7bq1d.xn--p1ai/api/realty-filter/residential/real-estates',
                                cookies=cookies,
                                params=params,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()

            if not data:
                print("Все квартиры загружены.")
                break

            for prop in data:
                try:
                    count += 1
                    date = datetime.date.today()
                    project = 'Одинцово Сити'
                    developer = "Атлантис Скай"
                    korpus = prop['building_number'].replace('Корпус ', '')
                    type_ = 'Квартира'
                    finish_type = 'Без отделки'
                    room_count = prop['rooms']

                    if room_count == 0:
                        room_count = 'студия'

                    area = prop['total_area']
                    old_price = prop['old_price']
                    price = prop['price']
                    section = prop['section_number']
                    floor = prop['floor_number']

                    if old_price == price:
                        price = None

                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                        '', '', type_, finish_type, room_count, area, '', old_price, '',
                        '', price, section, floor, ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            params['offset'] += params['limit']
            print(params['offset'])
            time.sleep(1)

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    except Exception as e:
        print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
