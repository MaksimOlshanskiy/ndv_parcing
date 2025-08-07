import datetime

from functions import save_flats_to_excel
from info import info
import requests
from save_to_excel import save_flats_to_excel_old_new_all

flats = []
count = 1

for key, data in info.items():
    headers = data['headers']
    params = data['params']
    cookies = data['cookies']

    url = 'https://a101.ru/api/v2/flat/'

    while url:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)

        if response.status_code == 200:
            item = response.json()
            items = item.get("results", [])

            for i in items:

                if i["complex"] == 'Испанские кварталы':
                    continue

                if i["complex"] == 'Белые ночи':
                    continue

                if i['status'] == 4:
                    continue

                date = datetime.date.today()
                project = i["complex"]
                status = ''
                developer = 'А101'
                district = ''
                korpus = i["building"]
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
                old_price = i["modified_price"]
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
            next_url = item.get("next")
            if next_url:
                url = next_url  # Переходим на следующую страницу
                params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
            else:
                break  # Если следующей страницы нет, выходим из цикла
        else:
            print(f'Ошибка: {response.status_code}')
            break

            time.sleep(0.01)

save_flats_to_excel(flats, project, developer)
