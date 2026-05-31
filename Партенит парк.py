import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests
from Profitbase_token import get_token


tenant_id = 14440
referer = 'https://atlantis-capital.ru'
headers_token = get_token(tenant_id, referer)

print(headers_token)


"""
обновить authorization в headers по ссылке https://atlantis-capital.ru/#/catalog/projects/list?filter=project:36990&filter=property.status:AVAILABLE&genplanId=20
"""

headers = headers_token

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'houseId': '103944',
    'limit': '10',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0
buildings_ids = ['103944', '103945', '119493', '119494']


for buildings_id in buildings_ids:

    params['houseId'] = buildings_id
    params['offset'] = '0'

    while True:

        try:
            response = requests.get('https://pb15265.profitbase.ru/api/v4/json/property', params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                properties = data.get("data", {}).get('properties', [])

                for prop in properties:
                    try:
                        count += 1
                        date = datetime.date.today()
                        project = 'Партенит Парк'
                        developer = "Севастопольстрой"
                        korpus = prop.get("houseName", "").replace('Дом ', '').replace(' - квартиры', '')
                        type_ = 'Квартиры'
                        finish_type = 'Без отделки'
                        room_count = prop.get("rooms_amount")

                        if room_count == 0:
                            room_count = 'студия'

                        area = prop.get("area", {}).get("area_total")
                        price_data = prop.get("price", {})
                        old_price = price_data.get("value")
                        section = prop.get("sectionName")
                        floor = prop.get("floor")

                        print(
                            f"{count} | {project}, комнаты: {room_count}, площадь: {area}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                        result = [
                            date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                            '', '', type_, finish_type, room_count, area, '', old_price, '',
                            '', '', int(section), floor, ''
                        ]
                        flats.append(result)

                    except Exception as e:
                        print(f"Ошибка при обработке квартиры: {e}")
                        continue

                if not properties:
                    break
                params['offset'] = str(int(params['offset']) + 10)

            else:
                print(f'Ошибка запроса: {response.status_code}, {response.text}')

        except Exception as e:
            print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
