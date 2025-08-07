import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

'''
обновить в headers authorization по ссылке
'''

#https://zhkbristol.ru/#/catalog/projects/list?filter=property.status:AVAILABLE

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6Ijg3YWYyYzczNTZhZjExOGUyMjBjMzg2M2Q1MzI3Yzk2Y2UzYjkwYjEzYWExZmMyMjA0N2IyZTE3ZGFlM2ZkOWJlYzcwMTdkOTlhNzU0NDVlIiwiaWF0IjoxNzUzMzYzNjg4LjE1Njc2OCwibmJmIjoxNzUzMzYzNjg4LjE1Njc3MSwiZXhwIjoxNzUzMzY3Mjg4LjE1MjUwMSwic3ViIjoiU0lURV9XSURHRVR8MzIyNCIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjM4OTAsInRpdGxlIjoi0J7QntCeICDQodCXIFwi0JrQu9GO0YctNDJcIiIsInN1YmRvbWFpbiI6InBiMzg5MCIsImJpbGxpbmdPd25lcklkIjozODk4LCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MzIyNCwiZG9tYWluIjoiaHR0cHM6Ly96aGticmlzdG9sLnJ1In19.WG0LjbPcUey8B5j2BU7j5RMha10oEvLR0y8jjvCXEazHg1llH9ThJyPtWIB2EpnoR2U0G_59j2oM_3YIodiMKcibDXwAjI7OK5k143_1WTSfHzYUn_w4m5zeY7bMA-JGNv9o_ifqZgQ8PDXS-OSH3mQ9q9recvGAiZKZr18t5RGdNFsDtOb3pvY2yt46UtERvdz5wijJk-x-9yFjr0JWPDAICdPITEhcaO0F85oXG6HdC4fiF9XB6HUGTPxZ0qmcd0WNQ9OACD-Xp5go0ohw02akpm1XeGN4bYNLmnbHljJaDkOWmtC6MSkWYYIWAb9RPBTGfHzq7q5Z8pwfnHCG5A',
    'origin': 'https://smart-catalog.profitbase.ru',
    'priority': 'u=1, i',
    'referer': 'https://smart-catalog.profitbase.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

params = {
    'propertyTypeAliases[0]': 'property',
    'isHouseFinished': '0',
    'status[0]': 'AVAILABLE',
    'limit': '100',
    'full': 'true',
    'returnFilteredCount': 'true',
}

flats = []
count=0

try:
    response = requests.get('https://pb3890.profitbase.ru/api/v4/json/property',
                            params=params,
                            headers=headers)

    if response.status_code == 200:
        data = response.json()
        properties = data.get("data", {}).get('properties', [])

        for prop in properties:
            try:
                count+=1
                date = datetime.date.today()
                project = 'Бристоль'
                developer = "СЗ Ключ"
                korpus = prop.get("houseName", "").replace('Корпус №', '')
                type_ = 'Квартира'
                room_count = prop.get("rooms_amount")
                area = prop.get("area", {}).get("area_total")
                price_data = prop.get("price", {})
                old_price = price_data.get("value")
                price = price_data.get("priceReserved")
                section = prop.get("section").replace(',','.')
                floor = prop.get("floor")


                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, '', old_price, '',
                    '', price, section, floor, ''
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
    save_flats_to_excel(flats,'Бристоль','СЗ Ключ')
else:
    print("Нет данных для сохранения")