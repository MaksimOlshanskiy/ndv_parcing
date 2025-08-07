import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests
import time

cookies = {
    '_ym_uid': '1743601239618056131',
    '_ym_d': '1743601239',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://domoplaner.ru/catalog/361/mmucvk/?start=1&domain=aHR0cHM6Ly92bHViZXIucnU%3D&back=1&state=plans&house_id=1312',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Storage-Access': 'active',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1743601239618056131; _ym_d=1743601239; _ym_isad=1; _ym_visorc=w',
}

flats = []
count = 0
page = 1
has_more_data = True

try:
    response = requests.get('https://domoplaner.ru/widget-api/widget/361-mmucvk/',
                            cookies=cookies,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        items = data.get('flats', [])

        print(f"Получено {len(items)} записей со страницы {page}")

        for i in items:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Влюберцы'
                developer = "Девелопмент 54"
                korpus = i['house_title'].replace('К', '')
                type_ = i['rooms_sign']

                if '1с' in type_:
                    room_count = "студия"
                else:
                    room_count = i['rooms']

                type_ = 'Квартира'
                area = i['area']
                old_price = i['price']
                price = i['price_with_discount']
                section = ''
                floor = i['floor_number']

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    'Продано', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, "", old_price, '',
                    "", price, section, floor, ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

        time.sleep(1)

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
