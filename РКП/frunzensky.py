import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
import requests

cookies = {
    'session': '39aa63958008563b6728d56113ce3f5708ca5c9f5f63804d323ee9c6e535ac26',
    '_ym_uid': '174427988640780778',
    '_ym_d': '1744279886',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dt1he8a81%3Bya_client_id%3D174427988640780778',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://xn----jtbbfggcdyc3aqvm.xn--p1ai/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'xn----jtbbfggcdyc3aqvm.xn--p1ai',
    # 'cookie': 'session=faebabe85f2dd1fa3f0e4291108cc484693efbceca9cfdb6fdb27031d15dffce; _ym_uid=174427988640780778; _ym_d=1753688964; _ym_isad=1; _ym_visorc=w',
}

params = {
    'project_id': '823c3be0-6a4c-4383-8607-cfcc4414d9da',
    'status': 'free',
    'offset': '0',
    'limit': '50',
}

flats = []
count = 0

try:
    response = requests.get('https://xn----jtbbfggcdyc3aqvm.xn--p1ai/api/realty-filter/residential/real-estates',
                            params=params,
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Фрунзенский'
                developer = "РКП"
                korpus = '1'
                room_count = i['rooms']

                if room_count == 0:
                    room_count = 'студия'

                type_ = "Квартира"
                area = i['total_area']
                old_price = i['old_price']
                price = i['price']
                section = i['section_number']
                floor = i['floor_number']

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, '', old_price, '',
                    '', price, int(section), int(str(floor)), ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
