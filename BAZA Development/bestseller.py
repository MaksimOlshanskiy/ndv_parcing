import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

'''
Надо обновить в headers поле authorization по ссылке
https://baza.bz/projects/bestseller#/catalog/projects/list?filter=project:50007&filter=property.type:property&filter=property.status:AVAILABLE&genplanId=2176
'''

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjNmODE2YWM2MjVmYTE2MzNkY2U1YTE4MGY4NWFkMDYzNjUwOWYwYjM4Y2MxOGNlNjQwYmI3NTZkMWZkZDFhNjY5MmVhNTYzNzUyZTRjMTMxIiwiaWF0IjoxNzU1MjQwNzIyLjY5MTE1LCJuYmYiOjE3NTUyNDA3MjIuNjkxMTUyLCJleHAiOjE3NTUyNDQzMjIuNjg1MzcxLCJzdWIiOiJTSVRFX1dJREdFVHwyMzQxIiwic2NvcGVzIjpbIlNJVEVfV0lER0VUIl0sInR5cGUiOiJzaXRlV2lkZ2V0IiwiZW50aXRsZW1lbnRzIjoiIiwiYWNjb3VudCI6eyJpZCI6MTUzNTMsInRpdGxlIjoiQkFaQSBEZXZlbG9wbWVudCIsInN1YmRvbWFpbiI6InBiMTUzNTMiLCJiaWxsaW5nT3duZXJJZCI6MTU0MTEsImNvdW50cnlDb2RlIjoiUlUifSwicm9sZXMiOlsiUk9MRV9TSVRFX1dJREdFVCJdLCJzaXRlV2lkZ2V0Ijp7ImlkIjoyMzQxLCJkb21haW4iOiJodHRwczovL2JhemEuYnoifX0.STmh0qn826DRmlOj3gv3pY_fyi7uDipPGItoGqT8bsVvKF6MRZZ4gGVwHzd4CoO9oHpY9iRCdY-jKoHRuDZtFyDhr_DyOJHf7OgFx-sJ-ohX8QlnZxcGKI9GIwbK0ubV_99VB176fmya3nuN9lS6tC525o_R3ukrctDCv04CbrgQIhDr9VtIh_CY3wIe0m_ee2JYvD9HqzzXVJmqVQlIwZ67lVLPsr_VtrcYi0TFvGJudEUgtolgq4EvZOfHFBcLuoZLcV4ykwPmVEa8LLKuQacOY8v7m2csW3Hd-nQKIPCF1MSRDacf-WoTDyMc-rhWH1EFd2d5LnwnKNeUSzH4ZQ',
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
    'projectIds[0]': '50007',
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '100',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []

try:
    response = requests.get('https://pb15353.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                date = datetime.date.today()
                project = 'Бестселлер'
                developer = "BAZA Development"
                korpus = prop.get("houseName", "").replace('Корпус №', '')
                type_ = 'Квартира'
                room_count = prop.get("rooms_amount")
                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("value")
                price_per_metr = round(float(price_data.get("pricePerMeter")))
                price = price_data.get("value")
                section = prop.get("section").replace(',', '.')
                floor = prop.get("floor")

                print(
                    f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, price_per_metr, old_price, '',
                    '', '', section, floor, ''
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
    save_flats_to_excel(flats, 'Бестселлер', 'BAZA Development')
else:
    print("Нет данных для сохранения")
