import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near
import requests

"""
обновить authorization в headers по ссылке https://atlantis-capital.ru/#/catalog/projects/list?filter=project:36990&filter=property.status:AVAILABLE&genplanId=20
"""

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6ImIwMjE3YzdiZDQ3MWE3ZGYwZmFlZDg4MzY1OGUyZmRiYmY1ZDlkMzhhN2I4ZDY0NmFkNGYxZGMzN2ExZjE3MWE2NGZkZDM0ZmQ1ODY5OTc1IiwiaWF0IjoxNzY0NTc5OTUzLjA0MzUxNiwibmJmIjoxNzY0NTc5OTUzLjA0MzUyLCJleHAiOjE3NjQ1ODM1NTMuMDMzNDU0LCJzdWIiOiJTSVRFX1dJREdFVHwyMjAxIiwic2NvcGVzIjpbIlNJVEVfV0lER0VUIl0sInR5cGUiOiJzaXRlV2lkZ2V0IiwiZW50aXRsZW1lbnRzIjoiIiwiYWNjb3VudCI6eyJpZCI6MTQ0NDAsInRpdGxlIjoi0JzRi9GC0LjRidC4INCU0LXQstC10LvQvtC_0LzQtdC90YIiLCJzdWJkb21haW4iOiJwYjE0NDQwIiwiYmlsbGluZ093bmVySWQiOjE0NDk4LCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MjIwMSwiZG9tYWluIjoiaHR0cHM6Ly9hdGxhbnRpcy1jYXBpdGFsLnJ1In19.t6r1rdsxv_4lu9dJ1lnV3GIwlPhrnmyoyEP8gboIYNVWV-q87eDmz-ulMCTq0PVmPFi9COTgpMSR87kKdQ0UrPRJWE1M7l_JQq1RtdeWDEnwZYtVYW9u8JuFMCXtCGZhQoBLE7RUtaqrXsxbBHsJI-60yZA8E0xvHIYCSvWTfP-B3exuOJG1M0W1cibOxWs14CzOnayRlyTqiFiWYdrRVRCdcYxNBhH_6EFNXWOqFg2YmteY-2MncrNyMDdLrsvhQA7TsQPFGuAyi6dLofJ_EiIr09-aFeRY-0qEv5joIwqym5CQjCHI0Ok5yNX6eSJRAdN0fvFkSEF1MZqC1PKUzw',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '75',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count = 0

try:
    response = requests.get('https://pb14440.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Атлантис'
                developer = "Березовец"
                korpus = prop.get("houseName", "").replace('Дом ', '').replace(' - квартиры', '')
                type_ = 'Квартира'
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

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
