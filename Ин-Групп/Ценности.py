import datetime
import time
from functions import save_flats_to_excel
import requests
from Profitbase_token import get_token


tenant_id = 15474
referer = 'https://xn--80abidp3aadf4alo4a.xn--p1ai'
headers_token = get_token(tenant_id, referer)

print(headers_token)

headers = headers_token

params = {
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '150',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0
total_count = 0
offset = 0

try:
    while True:
        # Добавляем параметр offset для пагинации
        params_with_offset = params.copy()
        params_with_offset['offset'] = offset

        response = requests.get('https://pb15474.profitbase.ru/api/v4/json/property',
                                params=params_with_offset,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            properties = data.get("data", {}).get('properties', [])
            filtered_count = data.get("data", {}).get('filteredCount', 0)

            # Если это первый запрос, получаем общее количество
            if offset == 0:
                total_count = filtered_count
                print(f"Всего доступно квартир: {total_count}")

            for prop in properties:
                try:
                    if '-кладовки' in prop.get("houseName", ""):
                        continue
                    count += 1
                    date = datetime.date.today()
                    project = 'Ценности'
                    developer = "Ин-групп"
                    korpus = prop.get("houseName", "").replace('Корпус ', '').replace('Луговая ','')
                    type_ = 'Квартира'
                    finish_type = 'Без отделки'
                    room_count = prop.get("rooms_amount")
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

            # Проверяем, нужно ли делать следующий запрос
            offset += len(properties)
            if offset >= total_count or not properties:
                break

            time.sleep(1)

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            break

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
