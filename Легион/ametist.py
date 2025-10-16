import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
from Profitbase_token import get_token

tenant_id = 17494
referer = 'https://ametist-hotel.ru/'
headers_token = get_token(tenant_id, referer)

print('Токен для авторизации успешно получен')

headers = headers_token

params = {
    'propertyTypeAliases[0]': 'hotel_room',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'houseId': '111759',
    'limit': '100',
    'offset': '0',
    'full': 'true',
    'returnFilteredCount': 'true',
}

base_url = 'https://pb17494.profitbase.ru/api/v4/json/property'

flats = []
count = 0
project = 'Гостиничный комплекс Аметист'
developer = "Легион"
korpus = '1'
type_ = 'Апартаменты'
finish_type = 'Без отделки'

while True:
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            break

        data = response.json()
        properties = data.get("data", {}).get('properties', [])
        total = data.get("data", {}).get("filteredCount", 0)

        if not properties:
            break

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                room_count = prop.get("rooms_amount")
                if room_count == 0:
                    room_count = 'студия'

                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("prevValue")
                price = price_data.get("value")
                section = ''
                floor = prop.get("floor")

                if old_price is None:
                    old_price = price
                    price = None

                print(f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

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

        # обновляем offset
        params['offset'] = str(int(params['offset']) + int(params['limit']))

        if len(flats) >= total:
            break

        time.sleep(0.5)  # задержка между запросами, если нужно

    except Exception as e:
        print(f"Общая ошибка: {e}")
        break

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
