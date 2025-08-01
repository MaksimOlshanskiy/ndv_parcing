import datetime
import time

from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    'kbSession': '17534287800232504',
    'kbCreated': 'Fri, 25 Jul 2025 07:33:01 GMT',
    'kbRes': 'true',
    'kbLoaded': 'true',
    'kbCheck': 'fbbd476b3873c7dca3172049a6c04bf5',
    'kbT': 'false',
    'kbUserID': '233469098217588478',
    'session': 'a18d8c0f7610d0d6980e4c4238cf2cf4936c72b36c9002cfda6788ab2b61e891',
    '_ym_uid': '1753428790636731976',
    '_ym_d': '1753428790',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://xn-----elchiocal7aidb7bq1d.xn--p1ai/flats',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'X-Host': 'xn-----elchiocal7aidb7bq1d.xn--p1ai',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'kbSession=17534287800232504; kbCreated=Fri, 25 Jul 2025 07:33:01 GMT; kbRes=true; kbLoaded=true; kbCheck=fbbd476b3873c7dca3172049a6c04bf5; kbT=false; kbUserID=233469098217588478; session=a18d8c0f7610d0d6980e4c4238cf2cf4936c72b36c9002cfda6788ab2b61e891; _ym_uid=1753428790636731976; _ym_d=1753428790; _ym_isad=2; _ym_visorc=w',
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
            time.sleep(1)

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')

    except Exception as e:
        print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel_near(flats, project, developer)
else:
    print("Нет данных для сохранения")
