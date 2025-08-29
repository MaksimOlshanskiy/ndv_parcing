import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Конфигурация запроса
USE_COOKIES = True  # Если API перестанет работать, установить в False

cookies = {
    'uxs_uid': 'a7fc58f0-03cc-11f0-b76f-47440c1fef64',
    'JSESSIONID': '33329C81F986F0E34E79BE272F975D57',
    '_ym_uid': '1742283798625057585',
    '_ym_d': '1742283798',
    '_ym_isad': '1',
    '_cmg_cssteIuGG': '1742283798',
    '_comagic_ideIuGG': '9191973997.13124352202.1742283798',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'Connection': 'keep-alive',
    'Origin': 'https://kortros.ru',
    'Referer': 'https://kortros.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'uxs_uid=a7fc58f0-03cc-11f0-b76f-47440c1fef64; JSESSIONID=33329C81F986F0E34E79BE272F975D57; _ym_uid=1742283798625057585; _ym_d=1742283798; _ym_isad=1; _cmg_cssteIuGG=1742283798; _comagic_ideIuGG=9191973997.13124352202.1742283798',
}

json_data = {
    'query': '\n    query flats($project: [String]!, $building_id: [Int], $queue: [Int], $section: [Int], $floor: FRange, $price: FRange, $price_meter: FRange, $area: FRange, $filter: [FlatFilter], $active: Boolean, $guid: [String], $room: [Int], $layouttype: [String], $logic: Logic, $plans_format: Format, $sort_by: String, $sort: Sort, $limit: Int, $from: Int, $finish: Boolean, $typicalFinishingType: [String], $is_apartament: Boolean, $readiness: String, $real_building_num: [String], $keyIssuance: Boolean, $beginYear: [Int], $readyYear: [Int], $readyQuarter: [Int], $address: String, $subtype: String, $patio: Boolean, $terrace: Boolean, $is_highceiling: Boolean, $design: Boolean, $extensions: FlatObjectExtensionsInput, $black_friday: Int) {\n  kortrosFlats(\n    filter: {project: $project, building_id: $building_id, queue: $queue, section: $section, floor: $floor, price: $price, price_meter: $price_meter, area: $area, filter: $filter, active: $active, guid: $guid, room: $room, layouttype: $layouttype, logic: $logic, plans_format: $plans_format, sort_by: $sort_by, sort: $sort, limit: $limit, from: $from, finish: $finish, typicalFinishingType: $typicalFinishingType, is_apartament: $is_apartament, readiness: $readiness, real_building_num: $real_building_num, keyIssuance: $keyIssuance, beginYear: $beginYear, readyYear: $readyYear, readyQuarter: $readyQuarter, address: $address, subtype: $subtype, patio: $patio, terrace: $terrace, is_highceiling: $is_highceiling, design: $design, extensions: $extensions, black_friday: $black_friday}\n  ) {\n    flats {\n      layouttype\n      address\n      beginYear\n      real_building_num\n      building_id\n      cost_per_meter\n      crm_status\n      discount\n      discountM2\n      floor_number\n      guid\n      initial_fee\n      is_apartament\n      keyIssuance\n      monthly_pay\n      number\n      pl\n      plan\n      project\n      queue\n      readiness\n      readyQuarter\n      readyYear\n      room_count\n      saleM2\n      salePercent\n      layouttype\n      constructorLayout\n      saleSum\n      section_number\n      square\n      status\n      total_cost\n      type_finish\n      typicalFinishingType\n      patio\n      terrace\n      ceiling_height\n      is_highceiling\n      design\n      subtype\n      extensions {\n        window_side_choices\n        window_view_choices\n        benefit_choices\n        promotion_choices\n        plan_rotation_value\n      }\n      black_friday\n    }\n    summary {\n      beginYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      real_building_num {\n        selected\n        value\n      }\n      cost_per_meter {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      floor_number {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      queue {\n        selected\n        value\n      }\n      readyQuarter {\n        selected\n        value\n      }\n      readyYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      room_count {\n        availableValue\n        room_count\n        selected\n        totalValue\n      }\n      section_number {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      square {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      typicalFinishingType {\n        key\n        totalValue\n        availableValue\n        selected\n      }\n      total_cost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      total_flats_count {\n        selected\n        total\n      }\n      total_flats_count_projects {\n        project\n        selected\n        total\n      }\n      subtype_projects {\n        project\n        countableData {\n          subtype\n          count\n          selected\n        }\n      }\n      patio {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      terrace {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      design {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      extensions {\n        window_side_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        window_view_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        benefit_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        promotion_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n      }\n    }\n  }\n}\n    ',
    'variables': {
        'guid': [],
        'project': [
            'tate',
            'headliner',
            'perhushkovo',
            'ilove',
            'ultima',
        ],
        'limit': 12,
        'sort_by': 'total_cost',
        'sort': 'ASC',
        'extensions': {},
        'from': 0,
        'subtype': '01',
        'layouttype': [],
        'finish': None,
        'design': None,
        'typicalFinishingType': [],
        'floor': {
            'from': None,
            'to': None,
        },
        'price': {
            'from': None,
            'to': 18731330599,
        },
        'area': {
            'from': None,
            'to': None,
        },
        'real_building_num': [],
        'keyIssuance': None,
        'readiness': None,
        'readyYear': [],
        'terrace': None,
        'patio': None,
        'is_highceiling': None,
    },
    'operationName': 'flats',
}

base_url = 'https://api.kortros.ru/graphql'
flats = []
current_page = 1
count = 0

while True:
    json_data['variables']['from'] = (current_page - 1) * json_data['variables']['limit']

    try:
        response = requests.post(
            base_url,
            headers=headers,
            cookies=cookies if USE_COOKIES else None,
            json=json_data
        )

        # Проверяем HTTP-статус
        if response.status_code != 200:
            print(f"Ошибка запроса: {response.status_code}, {response.text}")
            break

        # Пробуем разобрать JSON
        data = response.json()

        # Если есть ошибки в ответе
        if "errors" in data:
            print("Ошибка от API:", data["errors"])
            break

        if "data" not in data:
            print("Ошибка: поле 'data' отсутствует в ответе API")
            print("Ответ сервера:", response.text)
            break

        flats_data = data["data"].get("kortrosFlats", {}).get("flats", [])

        if not flats_data:
            print("Данные закончились, выхожу из цикла.")
            break

        for flat in flats_data:
            date = datetime.date.today()
            project = flat.get("project", '')
            if project == 'perhushkovo':
                project = 'Равновесие'

            status = ''
            srok_sdachi = ''
            developer = "Кортрос"
            district = ''
            korpus = flat.get('real_building_num', '')
            room_count = flat.get("room_count", '')
            type = flat.get("layouttype", '')

            if type in [0, '1С']:
                room_count = 'студия'

            type = 'Квартира'
            finish_type = flat.get("typicalFinishingType", '')
            if finish_type in ['withoutfinishing', 'finishingKitchen']:
                finish_type = 'Без отделки'
            elif finish_type in ['finishingSlippers', 'whitebox']:
                finish_type = 'Предчистовая'
            else:
                finish_type = 'С отделкой'
            area = flat.get("square", '')
            old_price = int(round(flat.get("total_cost", ''),0))
            price = int(round(flat.get("discount", ''),0))
            section = ''
            floor = flat.get("floor_number", '')

            if old_price == price:
                price = None
            elif price == 0:
                price= None

            count += 1

            print(f"{count}, {project}, прайс: {price}, отделка: {finish_type}, корпус: {korpus}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, '',
                      district, '', '', korpus.replace('Башня-', ''), '', '', srok_sdachi, '', '', '', type,
                      finish_type, room_count, area,
                      '', old_price, '', '', price, section, floor, '']
            flats.append(result)

        current_page += 1
        time.sleep(0.05)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        break

project = 'all'
save_flats_to_excel(flats, project, developer)
