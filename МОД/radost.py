import requests
import datetime
from save_to_excel import save_flats_to_excel_far
import time

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://radost-radumlya.ru',
    'priority': 'u=1, i',
    'referer': 'https://radost-radumlya.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

json_data = {
    'action': 'objects_list',
    'data': {
        'category': 'flat',
        'activity': 'sell',
        'page': 0,
        'filters': {
            'studio': 'null',
            'rooms': [],
            'restorations': [],
            'promos': [],
            'tags': [],
            'riser_side': [],
            'geo_city': '3417',
            'floors': [],
            'houses_ids': [],
            'type': None,
            'areaFrom': None,
            'areaTo': None,
            'priceFrom': None,
            'priceTo': None,
            'priceM2From': None,
            'priceM2To': None,
            'priceRentFrom': None,
            'priceRentTo': None,
            'priceRentM2From': None,
            'priceRentM2To': None,
            'status': None,
        },
        'complex_id': 6944958,
        'house_id': None,
        'orders': [
            {
                'field': 'price',
                'direction': 'asc',
            },
        ],
        'complex_search': None,
        'house_search': [],
        'cabinetMode': False,
    },
    'auth_token': None,
    'locale': None,
}

url = 'https://api.macroserver.ru/estate/catalog/?domain=radost-radumlya.ru&check=V5psWFAx-AxWY33cbD8HuUXUeMAz_hRxBBPXOw73S0lqblUaSwsdIVZYckUdfDE3NDU5MTU1NDF8ZDNmY2M&type=catalog&inline=true&issetJQuery=1&presmode=complex&complexid=6944958&uuid=1780e54a-d93a-46bc-aacd-13c8c41d8cfe&cookie_base64=eyJfeW1fdWlkIjoiMTc0NTkxNTQyOTczOTYyNTMzOSJ9&time=1745915541&token=14d3b19cc4f6f78ecb849ff6d26e5e13/'
count = 1
flats = []
while True:
    try:
        response = requests.get(url, json=json_data, headers=headers)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        break

    item = response.json()

    items = item.get("objects", [])

    for i in items:
        date = datetime.date.today()
        project = "Радость"
        developer = 'МОД'

        text = str(i["house_title"])
        cleaned_text = text.replace("&nbsp;", " ")
        parts = [part.strip() for part in cleaned_text.split(",")]
        korpus = int(parts[-1].replace('корпус&nbsp', ''))

        room_count = i["estate"]["estate_rooms"]
        type = i["category"]
        if type == 'flat':
            type = 'Квартира'
        area = f'{float(i["area"]):.2f}'
        price = f'{float(i["price"]):.0f}'
        floor = i["floor"]

        if price=='0':
            continue

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                  '', '', type, 'Без отделки', room_count, area, '', price, '', '', '',
                  '', floor, '']
        flats.append(result)
        count += 1

    # Проверяем, является ли текущая страница последней
    if item.get("isLastPage", False):  # Если isLastPage == True, завершаем цикл
        print("Достигнута последняя страница.")
        break

    # Увеличиваем номер страницы
    json_data['data']['page'] += 1

    time.sleep(0.05)

save_flats_to_excel_far(flats, project, developer)
