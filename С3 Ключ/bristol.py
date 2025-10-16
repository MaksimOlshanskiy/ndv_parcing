import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
from Profitbase_token import get_token
import sys

tenant_id = 3890
referer = 'https://zhkbristol-catalog.ru'
try:
    headers_token = get_token(tenant_id, referer)
    print('✅ Токен для авторизации успешно получен')
except:
    print('❌ Ошибка получения токена авторизации. Проверьте tenant_id и referer')
    sys.exit()

headers = headers_token

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