import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'session': '47e56a55723e0a944186bc5e7444f1b5f41f84ec0289d15f11e874e1e1e28ee2',
    '_ym_uid': '1743603667361296850',
    '_ym_d': '1743603667',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
    '_cmg_csstxB_xG': '1743603668',
    '_comagic_idxB_xG': '9249129767.13192890542.1743603667',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://s-odintsovo.ru/flats',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 's-odintsovo.ru',
    # 'cookie': 'session=47e56a55723e0a944186bc5e7444f1b5f41f84ec0289d15f11e874e1e1e28ee2; _ym_uid=1743603667361296850; _ym_d=1743603667; _ym_isad=1; _ym_visorc=w; _cmg_csstxB_xG=1743603668; _comagic_idxB_xG=9249129767.13192890542.1743603667',
}

params = {
    'project_id': 'b62585ce-3aee-4f84-89bf-f3781e3c3781',
    'status': 'free',
    'offset': '0',
    'limit': '40',
    'order_by': 'price',
}

flats = []

try:
    response = requests.get('https://s-odintsovo.ru/api/realty-filter/residential/real-estates',
                            params=params,
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                date = datetime.date.today()
                project = 'Сердце Одинцово'
                developer = "Стройтехинвест"
                korpus = i['building_number'].replace('Корпус ','')
                finish_type = i['finishing_type']
                if finish_type == 'no':
                    finish_type = 'Без отделки'
                else:
                    finish_type='Предчистовая'

                room_count = i['rooms']

                if room_count == 0:
                    room_count = 'студия'

                type_ = "Квартира"
                area = i['total_area']
                old_price = i['old_price']
                price = i['price']
                section = i['section_number']
                floor = i['floor_number']

                if old_price == price:
                    price = None

                print(
                    f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                    '', '', type_, finish_type, room_count, area, '', old_price, '',
                    '', price, int(section), int(str(floor)), ''
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
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
