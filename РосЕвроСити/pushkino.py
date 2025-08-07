import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle

cookies = {
    '_ym_uid': '1744213054178918476',
    '_ym_d': '1744213054',
    'carrotquest_device_guid': '72a6f170-7343-47f7-9dc3-216caa325013',
    'carrotquest_uid': '1947038311734316638',
    'carrotquest_auth_token': 'user.1947038311734316638.41040-5e95f043b3189eee6dfaa1159f.fd6aa0c3405b637775ff96ff2e414f7ff717a749aa19822e',
    '_gcl_au': '1.1.396528762.1748356639',
    'carrotquest_session': 'pk0lp0xl8ev1gwbfgtnt6yptaxvi9q29',
    'carrotquest_session_started': '1',
    'carrotquest_realtime_services_transport': 'wss',
    '_ga': 'GA1.2.700162277.1748356640',
    '_gid': 'GA1.2.1860283679.1748356640',
    '_gat_UA-193331392-1': '1',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDgzNjAyNDAsImlhdCI6MTc0ODM1NjY0MCwianRpIjoiODM3ZGUyZTg4NDYzNDZiMTkzYTg1YjQzMTZjYzNmNGYiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0ODM1NjY0MCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjQxMDQwLiR1c2VyX2lkOjE5NDcwMzgzMTE3MzQzMTY2MzgiXSwiYXBwX2lkIjo0MTA0MCwidXNlcl9pZCI6MTk0NzAzODMxMTczNDMxNjYzOH0.HWcFq6S2ewfy1shFlk7FRlIMwgM_AxbCaybbv39OvII',
    '_ym_isad': '1',
    '_ga_12SJ4GZXVT': 'GS2.2.s1748356640$o1$g0$t1748356640$j60$l0$h0$dEk8RjR6OMPu7-SIPKsw3oytXw71EjyY34g',
    '_ym_visorc': 'w',
    'csrftoken': 'mBBm3jEHM7sbaCMjmjA580s4TyLZBCNNUVlk4jfP2coQ80kAN6lR74zFXLx0ac9y',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://u-pushkino.ru',
    'priority': 'u=1, i',
    'referer': 'https://u-pushkino.ru/flats/?orderBy=price',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1744213054178918476; _ym_d=1744213054; carrotquest_device_guid=72a6f170-7343-47f7-9dc3-216caa325013; carrotquest_uid=1947038311734316638; carrotquest_auth_token=user.1947038311734316638.41040-5e95f043b3189eee6dfaa1159f.fd6aa0c3405b637775ff96ff2e414f7ff717a749aa19822e; _gcl_au=1.1.396528762.1748356639; carrotquest_session=pk0lp0xl8ev1gwbfgtnt6yptaxvi9q29; carrotquest_session_started=1; carrotquest_realtime_services_transport=wss; _ga=GA1.2.700162277.1748356640; _gid=GA1.2.1860283679.1748356640; _gat_UA-193331392-1=1; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDgzNjAyNDAsImlhdCI6MTc0ODM1NjY0MCwianRpIjoiODM3ZGUyZTg4NDYzNDZiMTkzYTg1YjQzMTZjYzNmNGYiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0ODM1NjY0MCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjQxMDQwLiR1c2VyX2lkOjE5NDcwMzgzMTE3MzQzMTY2MzgiXSwiYXBwX2lkIjo0MTA0MCwidXNlcl9pZCI6MTk0NzAzODMxMTczNDMxNjYzOH0.HWcFq6S2ewfy1shFlk7FRlIMwgM_AxbCaybbv39OvII; _ym_isad=1; _ga_12SJ4GZXVT=GS2.2.s1748356640$o1$g0$t1748356640$j60$l0$h0$dEk8RjR6OMPu7-SIPKsw3oytXw71EjyY34g; _ym_visorc=w; csrftoken=mBBm3jEHM7sbaCMjmjA580s4TyLZBCNNUVlk4jfP2coQ80kAN6lR74zFXLx0ac9y',
}

url = 'https://u-pushkino.ru/api/graphql/'

after_cursor = ""
flats = []
count = 1

for facing_value in [False, True]:
    after_cursor = ""
    while True:
        json_data = {
            'operationName': 'allFlats',
            'variables': {
                'rooms': '1,2,3,4',
                'building': [
                    'QnVpbGRpbmdUeXBlOjI=',
                    'QnVpbGRpbmdUeXBlOjM=',
                ],
                'orderBy': 'price',
                'areaMin': None,
                'areaMax': None,
                'facing': facing_value,
                'first': 12,
                'after': after_cursor,
            },
            'query': 'query allFlats($first: Int, $after: String, $orderBy: String, $priceMin: Float, $priceMax: Float, $areaMin: Float, $areaMax: Float, $floorMin: Float, $floorMax: Float, $rooms: String, $facing: Boolean, $hasView: Boolean, $hasDiscount: Boolean, $building: [ID], $id: [ID!], $installment: Boolean) {\n  allFlats(first: $first, after: $after, orderBy: $orderBy, priceMin: $priceMin, priceMax: $priceMax, areaMin: $areaMin, areaMax: $areaMax, floorMin: $floorMin, floorMax: $floorMax, rooms: $rooms, facing: $facing, hasView: $hasView, building: $building, hasDiscount: $hasDiscount, id: $id, installment: $installment) {\n    totalCount\n    edgeCount\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    edges {\n      node {\n        id\n        area\n        rooms\n        price\n        plan\n        promoPrice\n        isFavourite\n        discountPrice\n        discountSize\n        promoEnable\n        floor {\n          number\n          __typename\n        }\n        building {\n          id\n          number\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n',
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
                developer = 'РосЕвроСити'
                project = 'Южное Пушкино'
                korpus = node.get('building', {}).get('number', '')
                type = 'Квартира'
                finish_type = 'С отделкой' if facing_value else 'Без отделки'
                room_count = node.get('rooms', '')
                area = node.get('area', '')
                old_price = node['price']
                price = node.get('discountPrice')
                section = node.get('section', {}).get('number', '')
                floor = node.get('floor', {}).get('number', '')

                if old_price == price:
                    price = None

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

developer = 'РосЕвроСити'
project = 'Южное Пушкино'
save_flats_to_excel(flats, project, developer)
