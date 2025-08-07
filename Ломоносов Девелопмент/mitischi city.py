import datetime
import time
import traceback
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

'''
обновить authorization в headers по ссылке https://xn----otbabat2bef9dta.xn--p1ai/#/catalog/projects/list?filter=project:39970&filter=property.type:property&filter=property.status:AVAILABLE&genplanId=682
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6ImUzYmJiOTg5OWI0YmFjZjcyNzU0ZDE5MDg4NGNjNTk3YjM5ZGU3YTY2YzIzODBjMDU3MjE1YzA1YmI0MTNiNTM0MzBmOGI4NjI0MzIwNGRhIiwiaWF0IjoxNzUzNDM3MTk3LjgwNjI5MiwibmJmIjoxNzUzNDM3MTk3LjgwNjI5NSwiZXhwIjoxNzUzNDQwNzk3LjgwMjMxNiwic3ViIjoiU0lURV9XSURHRVR8MjQzNiIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjE0NDQwLCJ0aXRsZSI6ItCc0YvRgtC40YnQuCDQlNC10LLQtdC70L7Qv9C80LXQvdGCIiwic3ViZG9tYWluIjoicGIxNDQ0MCIsImJpbGxpbmdPd25lcklkIjoxNDQ5OCwiY291bnRyeUNvZGUiOiJSVSJ9LCJyb2xlcyI6WyJST0xFX1NJVEVfV0lER0VUIl0sInNpdGVXaWRnZXQiOnsiaWQiOjI0MzYsImRvbWFpbiI6Imh0dHA6Ly94bi0tLS1vdGJhYmF0MmJlZjlkdGEueG4tLXAxYWkifX0.nOxKRjsM9n0iBA_DADAhxwAO0D9vVDp3CTdcOcfbGX00fQH9SUepCPwE3_mt3CIRnO52arYIqqpELAHs3xGTLMgPm7rdAoTwXz5JtP8to8xahxhVj4xYUMdiqMU404AKMPZwv-ldHSe_vQ8MVcI_EWLDhUO9A3O7SQBqmGHShq-9_Wd3KG968xqt4FSJmr1u03DpZ_k1TkdCeL-d8l9Mun5-3a4xItUUlWcH_sNaOSBN-inN5VbI1IBMZI8XjBixcwmgyVd9Az4A_PMDHZoRO1lNk723HSSWIfaKAnee4Ivf6vnW_WvfF4isOsp7OGL2wWkey73BpkIPwuvE00KkYw',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
}

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
