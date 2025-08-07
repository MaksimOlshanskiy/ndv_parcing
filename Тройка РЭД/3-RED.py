import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near_all
import requests

cookies = {
    'connect.sid': 's%3AGB15spuYCDi9vAMJApBhbv-ZFDNXHslJ.3vpcfUNchu0mL08%2BQUMoLfgi900qoNyxwR9XzFPzSQM',
    'carrotquest_session': '97qxq9obssi4ppvul8u44hpivb51b25v',
    '_ga': 'GA1.1.662928379.1742211463',
    '_vector': '%7B%22128173%22%3A%7B%22cid%22%3A29139107%2C%22ph%22%3A74993254993%2C%22sid%22%3A54970825%7D%7D',
    'carrotquest_session_started': '1',
    'carrotquest_device_guid': 'a994cc73-5de6-4a4c-8aeb-aeb73a4bdb8d',
    'carrotquest_uid': '1930247701593588702',
    'carrotquest_auth_token': 'user.1930247701593588702.62974-5d857af0457878e53960d9df44.1c73a06a62b7b07ed6c9a980e45bd3cbee827239dde0593a',
    '_ym_uid': '1742211464211171065',
    '_ym_d': '1742211464',
    '_ym_isad': '1',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDIyMTUwNTgsImlhdCI6MTc0MjIxMTQ1OCwianRpIjoiYmRhNDg4Mjc4NWQxNDdkZWIxZjNjYzZjNDEyY2QzMWUiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0MjIxMTQ1OCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjYyOTc0LiR1c2VyX2lkOjE5MzAyNDc3MDE1OTM1ODg3MDIiXSwiYXBwX2lkIjo2Mjk3NCwidXNlcl9pZCI6MTkzMDI0NzcwMTU5MzU4ODcwMn0.rdeinFc9CVQOL-iqhf9YIfiTaQRsoR1mfSKfXBCNryw',
    'carrotquest_realtime_services_transport': 'wss',
    '_ga_ZM95D9X32Z': 'GS1.1.1742211463.1.1.1742211674.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'content-type': 'application/json',
    'origin': 'https://3-red.com',
    'priority': 'u=1, i',
    'referer': 'https://3-red.com/flats/search',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

base_url = 'https://3-red.com/api/search/common'

flats = []
count=0

# Начальная страница
current_page = 1

while True:
    try:
        # Определяем JSON-данные для запроса
        json_data = {
            'search': {
                'modsBtnList': [
                    {
                        'name': 'Все комплексы',
                        'value': '',
                    },
                    {
                        'name': 'Облака 2.0',
                        'value': 'ОБ2',
                        'objectId': '5f3a43afceb1c7660f2ccec6',
                    },
                    {
                        'name': 'Видный Берег 2.0',
                        'value': 'ВБ2',
                        'objectId': '5f3a476eceb1c7660f2cceca',
                    },
                    {
                        'name': 'Новотомилино',
                        'value': 'НТМ',
                        'objectId': '5f3a47eaceb1c7660f2ccecb',
                    },
                    {
                        'name': 'Светлый',
                        'value': 'ЛП',
                        'objectId': '61a0bfb08594360fead3d78d',
                    },
                ],
                'params': {
                    'spaceMin': 17,
                    'spaceMax': 87,
                    'priceMin': 4011303,
                    'priceMax': 28770942,
                    'floorMin': 2,
                    'floorMax': 25,
                    'type': 'КВ,АП',
                },
                'page': current_page,  # Добавляем параметр пагинации
            },
        }

        # Используем POST для запроса данных
        response = requests.post(base_url, cookies=cookies, headers=headers, json=json_data)

        # Проверка на статус ответа
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break

        data = response.json()

        # Проверяем, является ли data словарем
        if isinstance(data, dict):
            items = data.get("items", [])
            pagination = data.get("pagination", {})
        else:
            # Если data — это список, обрабатываем его напрямую
            items = data
            pagination = {}

        if not items:
            print("Данные закончились, выхожу из цикла.")
            break

        for i in items:
            count+=1
            date = datetime.date.today()
            project = i.get("jkName", "")
            status = ''
            developer = '3-RED'
            district = ''
            korpus = i.get('house', '')
            room_count = i.get("rooms", "")

            if room_count == 0:
                room_count = 'студия'

            type = i.get("type", "")
            if type == "КВ":
                type = "Квартира"
            else:
                type = "Аппартаменты"
            finish_type = i.get("decorationName", "")

            if finish_type == 'Черновая':
                finish_type = 'Без отделки'
            elif finish_type == 'WhiteBox':
                finish_type = 'Предчистовая'
            else:
                finish_type = 'с отделкой'

            area = i.get("space", "")
            old_price = i.get('price')
            discount = ''
            price = i.get("discountedPrice", "")
            section = i.get("section", "")
            floor = i.get("floor", "")

            if old_price == price:
                price = None

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, '',
                      district, '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area, '',
                      old_price, discount, '', price, section, floor, '']
            flats.append(result)

        # Проверяем, есть ли следующая страница
        if pagination.get("currentPage", 0) >= pagination.get("totalPages", 0):
            print("Все страницы обработаны, выхожу из цикла.")
            break

        # Переход на следующую страницу
        current_page += 1
        time.sleep(0.1)  # Задержка между запросами

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        break
    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        break


save_flats_to_excel(flats, project, developer)
