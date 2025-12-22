import datetime
import time
import requests

from functions import save_flats_to_excel
from info import info
from save_to_excel import save_flats_to_excel_old_new_all

base_url = 'https://msk.group-akvilon.ru/api/flats/'

flats = []
count = 1


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])

    return int(digits) if digits else s


for key, selected_info in info.items():
    print(f"Обработка данных из {key}...")

    # Извлекаем cookies, headers и params
    cookies = selected_info.get('cookies', {})
    headers = selected_info['headers']
    params = selected_info['params']

    url = base_url
    while url:
        response = requests.get(url, params=params, cookies=cookies, headers=headers)
        if response.status_code == 200:
            item = response.json()
            items = item.get("results", [])
            for i in items:
                date = datetime.date.today()
                project = i["project_title"].replace('Аквилон ', '').replace(' by Akvilon', '')
                english = ''
                promzona = ''
                mestopolozhenie = ''
                subway = ''
                distance_to_subway = ''
                time_to_subway = ''
                mck = ''
                distance_to_mck = ''
                time_to_mck = ''
                bkl = ''
                distance_to_bkl = ''
                time_to_bkl = ''
                status = ''
                start = ''
                comment = ''
                developer = "Аквилон"
                okrug = ''
                district = ''
                adress = ''
                eskrou = ''
                if project == 'NEXUS':
                    korpus = i["building_number"]
                else:
                    korpus = i["building_number"][:1]
                konstruktiv = ''
                klass = ''
                srok_sdachi = ''

                srok_sdachi_old = ''
                stadia = ''
                dogovor = ''

                if project == 'SIGNAL':
                    type = 'Апартаменты'
                else:
                    type = 'Квартира'

                finish_type = "Без отделки"
                room_count = i["rooms"]
                if room_count == None:
                    room_count = 'студия'

                area = float(i["area"])
                price_per_metr = ''
                old_price = i["original_price"]
                discount = ''
                price_per_metr_new = ''
                price = i["price"]
                section = ''
                floor = i["floor"]
                flat_number = ''

                if price == old_price:
                    price = None

                print(
                    f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
                result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                          mck,
                          distance_to_mck, time_to_mck, distance_to_bkl,
                          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                          konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                          price_per_metr_new, price, section, floor, flat_number]
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

        time.sleep(0.3)
project = 'all'
save_flats_to_excel(flats, project, developer)
