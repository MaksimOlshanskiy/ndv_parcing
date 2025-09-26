import datetime
import time
import traceback
import requests
from functions import save_flats_to_excel
from Profitbase_token import get_token
import sys

tenant_id = 14440
referer = 'https://xn----otbabat2bef9dta.xn--p1ai/'
try:
    headers_token = get_token(tenant_id, referer)
    print('✅ Токен для авторизации успешно получен')
except:
    print('❌ Ошибка получения токена авторизации. Проверьте tenant_id и referer')
    sys.exit()

headers = headers_token

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': 1000,
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
offset = 1
page_size = 75
count = 0

while True:
    params.update({'offset': offset, 'limit': page_size})
    response = requests.get('https://pb14440.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        if not properties:
            print(f"Данных больше нет.")
            break

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Мытищи Сити'
                developer = "Ломоносов Девелопмент"
                korpus = prop["houseName"]
                type_ = 'Квартира'
                finish_type = 'Без отделки'
                room_count = prop["rooms_amount"]
                area = prop["area"]["area_total"]
                old_price = prop['price']["value"]
                price_per_metr_new = prop['price']["pricePerMeter"]
                price = prop['price']["value"]
                section = prop["sectionName"]
                floor = prop["floor"]

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', old_price, '',
                    '', price, int(section), floor, ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                traceback.print_exc()
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

    offset += page_size

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
