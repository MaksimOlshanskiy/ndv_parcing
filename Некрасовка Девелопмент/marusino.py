import datetime
import time
from save_to_excel import save_flats_to_excel_near
import requests

cookies = {
    'session': '91baff7f8063ce779132d2dafdfc2cba02b4e7e9412fb2e7a2046dd42ae82079',
    'roistat_visit': '221812',
    'roistat_first_visit': '221812',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    'scbsid_old': '2796070936',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit',
    '_ym_uid': '1743760347684044274',
    '_ym_d': '1743760347',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '___dc': '3607657e-c6d7-4fd2-a834-08107ad47e26',
    '_cmg_csstIbdzG': '1743760348',
    '_comagic_idIbdzG': '10178920901.14379243286.1743760348',
    'sma_session_id': '2249233526',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%5D',
    'SCBstart': '1743760349278',
    'SCBFormsAlreadyPulled': 'true',
    'sma_index_activity': '3148',
    'SCBindexAct': '1696',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://legendamarusino.ru/flats',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-host': 'legendamarusino.ru',
}

flats = []
limit = 100
offset = 0
total_flats = 0
processed_flats = 0
count = 0

try:

    initial_params = {
        'project_id': 'a5f9b6b9-037d-4cd8-981c-cbd55e93a5c0',
        'status': 'free',
        'offset': 0,
        'limit': 1,  # Минимальный запрос для получения метаданных
        'order_by': 'price',
    }

    initial_response = requests.get('https://legendamarusino.ru/api/realty-filter/residential/real-estates',
                                    params=initial_params,
                                    headers=headers,
                                    cookies=cookies)

    if initial_response.status_code == 200:
        initial_data = initial_response.json()
        total_flats = len(initial_data)  # В вашем случае API может возвращать общее количество в метаданных
        # Если API не возвращает общее количество, можно попробовать получить его из заголовков или другого поля
        # В этом примере предполагаем, что мы знаем общее количество (107)
        total_flats = 107

        print(f"Всего квартир: {total_flats}")

        # Запрашиваем данные пачками по limit записей
        while offset < total_flats:
            params = {
                'project_id': 'a5f9b6b9-037d-4cd8-981c-cbd55e93a5c0',
                'status': 'free',
                'offset': offset,
                'limit': limit,
                'order_by': 'price',
            }

            response = requests.get('https://legendamarusino.ru/api/realty-filter/residential/real-estates',
                                    params=params,
                                    headers=headers,
                                    cookies=cookies)

            if response.status_code == 200:
                data = response.json()
                current_batch = len(data)
                processed_flats += current_batch

                for i in data:
                    try:
                        count += 1
                        date = datetime.date.today()
                        project = 'Легенда Марусино'
                        developer = "Некрасовка Девелопмент"
                        korpus = i['building_number']
                        room_count = i['rooms']

                        if room_count == 0:
                            room_count = 'студия'

                        type_ = "Квартира"

                        if i['finishing_type'] == 'no':
                            finish_type = 'Без отделки'
                        else:
                            finish_type = "С отделкой"

                        area = i['total_area']
                        old_price = i['old_price']
                        price = i['price']
                        section = i['section_number']
                        floor = i['floor_number']

                        if old_price == price:
                            price = None

                        print(
                            f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                        result = [
                            date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                            '', '', type_, finish_type, room_count, area, '', old_price, '',
                            '', price, section, int(str(floor)), ''
                        ]
                        flats.append(result)

                    except Exception as e:
                        print(f"Ошибка при обработке квартиры: {e}")
                        continue

                offset += limit
                print(f"Обработано {processed_flats} из {total_flats} квартир")

                time.sleep(1)
            else:
                print(f'Ошибка запроса: {response.status_code}, {response.text}')
                break
    else:
        print(f'Ошибка начального запроса: {initial_response.status_code}, {initial_response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel_near(flats, project, developer)
else:
    print("Нет данных для сохранения")
