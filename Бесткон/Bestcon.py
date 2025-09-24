import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests
from info import info

'''
Надо проверять data filter в info.py
'''

flats = []
count=1

for key, item in info.items():
    headers = item['headers']
    data = item['data']
    project=item['project_name']

    url = 'https://planetarf.ru/api/site.php'

    page = 1

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        try:
            item = response.json()

            items = item.get('places', {})

            for flat_id, flat_data in items.items():
                if isinstance(flat_data, dict):
                    date = datetime.date.today()
                    developer = "Бесткон"
                    korpus = flat_data.get("id_house", "")
                    type_ = flat_data.get("category", "")
                    room_count = flat_data.get("RoomsCount", "")
                    area = f'{float(flat_data.get("allSquare", "")):.2f}'
                    old_price = f'{float(flat_data.get("AgentCost_old", "")):.0f}'
                    price = f'{float(flat_data.get("AgentCost")):.0f}'
                    floor = flat_data.get("floor", "")

                    if old_price=="0":
                        old_price=price

                    print(
                        f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '', '',
                        '',
                        '', korpus,
                        '', '', '', '', '', '', type_, 'Без отделки', int(room_count), area, '', int(old_price), '',
                        '', int(price), '', int(floor), ''
                    ]
                    flats.append(result)

                    count+=1
                else:
                    print(f"Неожиданный формат данных для квартиры {flat_id}: {flat_data}")
        except requests.exceptions.JSONDecodeError as e:
            print("Ошибка декодирования JSON:", e)
            print("Содержимое ответа (не JSON):", response.text)
    else:
        print(f'Ошибка: {response.status_code}')

    time.sleep(0.3)

project = 'all'
save_flats_to_excel(flats, project, developer)
