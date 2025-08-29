import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

'''
заменить в headers authorization по ссылке https://xn--80abdl0adtby.xn--p1ai/#/catalog/projects/houses?filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjBmZjljYjlmMjRmOWRiOGFkYzdkODFiYWU1YjJhN2Y2YzcxZDVjZTEyYjFiZGE1ZmQxMTBjNGQ5Nzk4NGViZGU1ZWJjNzJiZjY2NmU0ZDUzIiwiaWF0IjoxNzU1NzYyMjkxLjIyODAxLCJuYmYiOjE3NTU3NjIyOTEuMjI4MDEzLCJleHAiOjE3NTU3NjU4OTEuMjEzNDY2LCJzdWIiOiJTSVRFX1dJREdFVHwyODMwIiwic2NvcGVzIjpbIlNJVEVfV0lER0VUIl0sInR5cGUiOiJzaXRlV2lkZ2V0IiwiZW50aXRsZW1lbnRzIjoiIiwiYWNjb3VudCI6eyJpZCI6NDI0MiwidGl0bGUiOiLQntCe0J4g0JPRgNCw0L3QtCIsInN1YmRvbWFpbiI6InBiNDI0MiIsImJpbGxpbmdPd25lcklkIjo0MjUwLCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MjgzMCwiZG9tYWluIjoiaHR0cHM6Ly94bi0tODBhZWlsaXVqNWRwLnhuLS1wMWFpIn19.0dExiQkpLtY20uxXAaeqFFfFY3tlFVr2osrxQzJOTNMjb2824uATSIZM8L-h6JUD5OVMVWk_CX2OEx8IpawYy7q6qTKJHsXSgv6coB3wLhb2W5LRHhATxZvrL6n-APMDysNkTHUJoEZjtYMzOpzvf9vBrnx0sZkg9h_oyQMTr7p8CTKCCX5IOuzWzlVpQqTE8e34wZpkcTJpO4lAnB35InQ759-z43THUR-suY10C0ib3vqht8GDjJaKV3NzQNzacVv-dMVqGo4dB4YM0dS2XEE0TVhQgnTJJm_4AMKxEX_JNrIFDnALIxLI7f7NrrVzAQuZZewGNjbHRiMIge6JHg',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '10',
    'offset': '10',
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
        response = requests.get('https://pb4242.profitbase.ru/api/v4/json/property',
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
                    count+=1
                    date = datetime.date.today()
                    project = prop['projectName']
                    developer = "Гранд"
                    korpus = prop["houseName"].replace('Дом №', '')
                    type_ = 'Квартира'
                    finish_type = 'Без отделки'
                    room_count = prop["rooms_amount"]
                    area = prop["area"]["area_total"]
                    old_price = prop["custom_fields"][2]['value']
                    section = prop["sectionName"]
                    floor = prop["floor"]


                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                        '', '', type_, finish_type, room_count, area, '', old_price, '',
                        '', '', section, floor, ''
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

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
