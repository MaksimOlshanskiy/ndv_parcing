import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
from Profitbase_token import get_token

'''
обновить в headers authorization по ссылке
'''



tenant_id = 3890
headers = get_token(tenant_id)

print(headers)

#https://zhkbristol.ru/#/catalog/projects/list?filter=property.status:AVAILABLE

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJzaXRlX3dpZGdldCIsImp0aSI6IjI0NDk3OTE3M2I1YTY1ZDJmY2RkMzkxZDdmZmNlM2ZmNDdmZTdhZDBmOGJjZTAxMjUzOThmN2NmZmZiODcxZmZmY2Y1MGY4ZGNhNTNhZmFkIiwiaWF0IjoxNzU1ODU3MjQ2LjI1Mzk5MywibmJmIjoxNzU1ODU3MjQ2LjI1Mzk5NSwiZXhwIjoxNzU1ODYwODQ2LjI0OTcyOSwic3ViIjoiU0lURV9XSURHRVR8MzIyNCIsInNjb3BlcyI6WyJTSVRFX1dJREdFVCJdLCJ0eXBlIjoic2l0ZVdpZGdldCIsImVudGl0bGVtZW50cyI6IiIsImFjY291bnQiOnsiaWQiOjM4OTAsInRpdGxlIjoi0J7QntCeICDQodCXIFwi0JrQu9GO0YctNDJcIiIsInN1YmRvbWFpbiI6InBiMzg5MCIsImJpbGxpbmdPd25lcklkIjozODk4LCJjb3VudHJ5Q29kZSI6IlJVIn0sInJvbGVzIjpbIlJPTEVfU0lURV9XSURHRVQiXSwic2l0ZVdpZGdldCI6eyJpZCI6MzIyNCwiZG9tYWluIjoiaHR0cHM6Ly96aGticmlzdG9sLnJ1In19.1ha0VPnfkwOWvSgyg2g7_NXzRQdZcR3ugDV9O3oRfr0sGikVZMEMdejftp_-LcjgGO-fVGKUAqJpvCZwlZVSlPsAhjpHXnIzdluSsOMnIKXt75lrf0R3xqGZDwv46L_L1_9a9GLVOP58EhSLEqIGKlESFvf2XiVYTHxCYkvOcHHquHc0PGX4qtJuvdE5fK12dFFnKPPti8VEbaGRpPi3BUqQPq9t-WOK6fRv7EOAb1VT94Cu6etJhlsTtuJ_bpeBRZ_nWZ-r_hqaP1flvqcrogDDbhPB0XA3g-i8F8u_26Cf8UIUS_7TUMN4kMhVfjpWoE44UPnq_KyzeybEh8Rvfg',
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