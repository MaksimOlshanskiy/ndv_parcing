import datetime
from functions import save_flats_to_excel
from info import info
import requests
import random
import time

flats = []
count = 1

for key, data in info.items():
    headers = data['headers']
    params = data['params']
    cookies = data['cookies']

    url = 'https://a101.ru/api/flats/'

    while url:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        print(response.status_code)

        if response.status_code == 200:
            item = response.json()
            items = item.get("results", [])

            for i in items:

                if i["project"] == 'Испанские кварталы':
                    continue

                if i["project"] == 'Белые ночи':
                    continue

                if i['status'] == 4:
                    continue

                date = datetime.date.today()
                project = i["project"]
                status = ''
                developer = 'А101'
                district = ''
                korpus = i["building"]
                try:
                    if project == 'Скандинавия' and int(korpus.split('.')[0]) < 25:
                        project = 'Скандинавия Юг'
                    if project == 'Скандинавия' and int(korpus.split('.')[0]) >= 25:
                        project = 'Скандинавия Центр'
                except:
                    pass

                room_count = i["room"]

                if params.get("design") == '2':
                    finish_type = 'Предчистовая'
                elif params.get("design") == '3':
                    finish_type = 'С отделкой'
                elif params.get("design") == '1':
                    finish_type = 'Без отделки'

                type = i["room_name"]
                if type == 'Студия':
                    room_count = 'Студия'

                type = 'Квартира'
                area = i["area"]
                old_price = i["price"]
                discount = ''
                price = i["actual_price"]
                section = i["section_number"]
                try:
                    floor = float(i["floor"])
                except:
                    floor = i["floor"].replace(' ', '')

                if price == old_price:
                    price = None

                print(
                    f"{count},{project}, тип: {type}, комнаты: {room_count}, площадь: {area}, цена: {price}, отделка: {finish_type}")

                result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '',
                          '', '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area,
                          '', old_price, '', '', price, section, floor, '']
                flats.append(result)
                count += 1

            # Проверяем, есть ли следующая страница
            if not items:
                break
            params['offset'] = str(int(params['offset']) + int(params['limit']))

        else:
            print(f'Ошибка: {response.status_code}')
            break
        sleep_time = random.uniform(0.1, 2)
        time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)
