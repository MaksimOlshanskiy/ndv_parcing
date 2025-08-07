import datetime
import requests
import time
import json

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://dogma.ru',
    'referer': 'https://dogma.ru/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

flats = []
count=0
limit = 100
offset = 0
has_more_data = True
total_objects = 445
max_attempts = 3  # Максимальное количество попыток при ошибках
attempt = 0

try:
    while has_more_data and attempt < max_attempts:
        json_data = {
            'areas': [17.63,83.21,],
            'costs': [4000000,16100000,],
            'deadlines': [],
            'floors': [2,15],
            'layout_id': [],
            'letter_ids': [],
            'limit': 12,
            'offset': offset,
            'ids': [],
            'project_ids': [6],
            'rooms': [],
            'statuses': [2],
            'tags': [],
            'types': [1],
            'group_by': '',
            'order': {
                'field': 'cost',
                'type': 'desc',
            },
        }

        json_payload = json.dumps(json_data, ensure_ascii=False)

        try:
            response = requests.post(
                'https://service.1dogma.ru/api/layouts-filter/v2/objects/filter',
                data=json_payload,
                headers=headers,
                timeout=30
            )

            print(f"Response status: {response.status_code}")

            if response.status_code == 200:
                try:
                    item = response.json()
                    items = item.get('objects', [])

                    # Обновляем общее количество объектов при первом запросе
                    if offset == 0:
                        total_objects = item.get('total', 445)
                        print(f"Всего найдено объектов: {total_objects}")

                    print(f"Получено {len(items)} записей, offset: {offset}")

                    for i in items:
                        try:
                            count+=1
                            date = datetime.date.today()
                            project = 'Публицист'
                            developer = "Догма"
                            korpus = i.get('letter_name', '')
                            room_count = i.get('room', '')
                            type_='Квартира'
                            tags = i.get('tags', [])
                            finish_type = tags[0].get('text', '') if tags and isinstance(tags[0],
                                                                                                    dict) else 'Без отделки'

                            if finish_type in ['Квартиры недели','Квартиры дня']:
                                finish_type='Без отделки'

                            area = i.get('area', 0)
                            price = i.get('cost_sale', 0)
                            old_price = i.get('cost', 0)
                            price_per_metr_new = ''
                            price_per_metr = i.get('square_price', '')
                            section = i.get('entrance_number', '')
                            floor = i.get('floor', '')

                            if price == 0:
                                price = None


                            print(
                                f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {i.get('floor', '')}")

                            result = [
                                date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                                '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                                '', '', type_, finish_type, room_count, area, price_per_metr,
                                old_price, '', price_per_metr_new, price,
                                section, floor, ''
                            ]
                            flats.append(result)

                        except Exception as e:
                            print(f"Ошибка при обработке квартиры: {e}")
                            continue

                    # Проверяем, есть ли еще данные для загрузки
                    offset += len(items)  # Увеличиваем offset на количество полученных записей

                    # Условия завершения:
                    # 1. Получили все объекты (offset >= total_objects)
                    # 2. Сервер вернул пустой список
                    # 3. Достигли максимального количества объектов (на всякий случай)
                    if offset >= total_objects or len(items) == 0 or len(flats) >= total_objects:
                        has_more_data = False
                    else:
                        print(f"Загружено {len(flats)} из {total_objects} объектов")

                    attempt = 0  # Сбрасываем счетчик попыток при успешном запросе
                    time.sleep(0.05)  # Увеличиваем паузу между запросами

                except json.JSONDecodeError as e:
                    print(f"Ошибка декодирования JSON: {e}")
                    print(f"Ответ сервера: {response.text}")
                    attempt += 1
                    time.sleep(5)
                except Exception as e:
                    print(f"Ошибка при обработке ответа: {e}")
                    attempt += 1
                    time.sleep(5)
            else:
                print(f'Ошибка запроса: {response.status_code}, {response.text}')
                attempt += 1
                time.sleep(10)  # Увеличиваем паузу при ошибке

        except requests.exceptions.RequestException as e:
            print(f"Ошибка соединения: {e}")
            attempt += 1
            time.sleep(10)

except Exception as e:
    print(f"Общая ошибка: {e}")

print(f"Всего получено записей: {len(flats)} (ожидалось: {total_objects})")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
