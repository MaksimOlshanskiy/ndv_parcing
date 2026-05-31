import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_far

'''
 меняем headers по ссылке https://xn----ctbblbzciwbb4ap4b9g.xn--p1ai/#/profitbase/projects/houses?filter=property.status:AVAILABLE
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjJmZjZlZDI1ZDlmMDk0ZDI1NzU0MDhhNzUxNDExNjNkNjUwYzc4N2FhYzM2ZmI4N2RjNjMyZDUyMTlkN2ZkOTcwZDkwYzIyYTUyMWI1MjRiIiwiaWF0IjoxNzc5ODk3MTk4LjE4MzA1NCwibmJmIjoxNzc5ODk3MTk4LjE4MzA1NywiZXhwIjoxNzc5OTAwNzk4LjE3NTA5OCwic3ViIjoiU0lURV9XSURHRVR8MjQ1NiIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjMwMDIsInRpdGxlIjoi0KLQtdGF0L3QvtCh0YLRgNC-0LnQntC70LjQvNC_Iiwic3ViZG9tYWluIjoicGIzMDAyIiwiYmlsbGluZ093bmVySWQiOjMwMDksImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjoyNDU2LCJkb21haW4iOiJodHRwczovL3huLS0tLWN0YmJsYnpjaXdiYjRhcDRiOWcueG4tLXAxYWkifX0.lKEwnQGf-9n0LBeRbsVsndwSheB-f_fd0aXyyD_ygLNbcDa2gtCLG4BuaEa1kCryx2yfvVFUn0F95F75kq6Lf_NXIIq4l1JccR5LwIYlyCRN35tmxVt_tEFXaHMHAfPbW1xWe8HRuzRhNemWGjJqedQOS0vuUJUowO3rr3KKNVtV7K9Suozzgz9RXWYqB3FbZLQSPqyPdbM9--0pVJS3Z1Ej1id4E89urWbuzSk-peJwXmoGeFP-qh9XN_hag6ph8a-bezD4O6R9u0_NAyPjCbrtlCgilNo6-E7v0Hx30op8KR5Jhe0s-wHULW4uYLMJwyUtgDghfAJ5z0KSwKlyTA',
    'cache-control': 'no-cache',
    'origin': 'https://smart-catalog.profitbase.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
}

params = {
    'projectIds[0]': '36061',
    'propertyTypeAliases[0]': 'property',
    'status[0]': 'AVAILABLE',
    'limit': '10',
    'full': 'true',
    'showQueueCount': 'true',
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
        response = requests.get('https://pb3002.profitbase.ru/api/v4/json/property',
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
                    count += 1
                    date = datetime.date.today()
                    project = 'Клевер'
                    developer = "Техноолимпстрой"
                    korpus = prop.get("houseName", "").replace('Корпус ', '')
                    type_ = 'Квартира'
                    finish_type = prop['custom_fields'][28]['value']

                    if finish_type=='Чистовая':
                        finish_type='С отделкой'
                    elif finish_type=='Предчистовая':
                        finish_type=finish_type
                    else:
                        finish_type='Без отделки'

                    room_count = prop.get("rooms_amount")
                    area = prop.get("area", {}).get("area_total")
                    price_data = prop.get("price", {})
                    old_price = price_data.get("value")
                    section = int(prop.get("sectionName").split(' ')[1])
                    floor = prop.get("floor")

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
