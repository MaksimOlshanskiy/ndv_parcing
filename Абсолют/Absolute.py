import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    '_ga': 'GA1.1.400089121.1742210146',
    'uxs_uid': '2ced5200-0321-11f0-955e-f91289c39404',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

url = 'https://www.absrealty.ru/graphql/'

after_cursor = ""
flats = []
count = 1

while True:
    json_data = {
        'query': '''
            query allFlats($first: Int, $after: String) {
    allFlats(first: $first, after: $after) {
        pageInfo {
            endCursor
            hasNextPage
        }
        edges {
            node {
                id
                number
                rooms
                area
                price
                originPrice
                building { number }
                section { number }
                floor { number }
                project { name }
                finishTypes {
                    edges {
                        node {
                            title
                        }
                    }
                }
            }
        }
    }
}

        ''',
        'variables': {
            'first': 8,
            'after': after_cursor,
        },
    }

    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()

        edges = data.get('data', {}).get('allFlats', {}).get('edges', [])
        page_info = data.get('data', {}).get('allFlats', {}).get('pageInfo', {})

        for edge in edges:
            node = edge.get('node', {})
            date = datetime.date.today()
            developer = 'Абсолют'
            project = node.get('project', {}).get('name', '')

            if project == 'Заречье Парк':
                continue

            korpus = node.get('building', {}).get('number', '')
            type = 'Квартира'

            finish_types = node.get('finishTypes', {})
            finish_edges = finish_types.get('edges', []) if finish_types else []
            finish_node = finish_edges[0].get('node', {}) if finish_edges else {}
            finish_type = finish_node.get('title', '')

            if finish_type == '':
                finish_type = 'Без отделки'
            elif finish_type == 'White-box':
                finish_type = 'Предчистовая'
            else:
                finish_type='С отделкой'

            room_count = node.get('rooms', '')
            area = node.get('area', '')
            old_price = round(float(node.get('originPrice', '')))
            price = round(float(node.get('price', '')))
            section = node.get('section', {}).get('number', '')
            floor = node.get('floor', {}).get('number', '')

            if price==old_price:
                price=None

            print(
                f"{count}, {project}, дата: {date}, отделка: {finish_type}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '',
                      '', '', '', korpus, '', '', '', '', '', '', type, finish_type, room_count, area, '',
                      old_price, '', '', price, section, floor, '']
            flats.append(result)
            count += 1

        if not page_info.get("hasNextPage", False):
            break
        after_cursor = page_info.get("endCursor", "")
        time.sleep(0.05)
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        break

save_flats_to_excel(flats, project, developer)
