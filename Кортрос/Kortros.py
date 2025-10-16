import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Иногда нужно обновлять куки
USE_COOKIES = False  # Если API перестанет работать, установить в False

cookies = {
    '_ym_uid': '174732046945412953',
    '_ym_d': '1758632015',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'JSESSIONID': '2D3C543ED7460A5C1BC5D0613BE44310',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1758957929950%2C%22sl%22%3A%7B%22224%22%3A1758871529950%2C%221228%22%3A1758871529950%7D%7D',
    'adrdel': '1758871530292',
    '_cmg_csstVoE91': '1758871548',
    '_comagic_idVoE91': '9861490022.13904654207.1758871547',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://kortros.ru',
    'Referer': 'https://kortros.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=174732046945412953; _ym_d=1758632015; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; JSESSIONID=2D3C543ED7460A5C1BC5D0613BE44310; _ym_isad=2; _ym_visorc=w; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1758957929950%2C%22sl%22%3A%7B%22224%22%3A1758871529950%2C%221228%22%3A1758871529950%7D%7D; adrdel=1758871530292; _cmg_csstVoE91=1758871548; _comagic_idVoE91=9861490022.13904654207.1758871547',
}

json_data = {
    'query': '\n    query Flats($project: [String]!, $building_id: [Int], $queue: [Int], $section: [Int], $floor: FRange, $price: FRange, $price_meter: FRange, $area: FRange, $filter: [FlatFilter], $active: Boolean, $guid: [String], $room: [Int], $layouttype: [String], $logic: Logic, $plans_format: Format, $sort_by: String, $sort: Sort, $limit: Int, $from: Int, $finish: Boolean, $typicalFinishingType: [String], $is_apartament: Boolean, $readiness: String, $real_building_num: [String], $keyIssuance: Boolean, $beginYear: [Int], $readyYear: [Int], $readyQuarter: [Int], $preview: Boolean, $address: String, $subtype: String, $patio: Boolean, $terrace: Boolean, $is_highceiling: Boolean, $design: Boolean, $extensions: FlatObjectExtensionsInput, $black_friday: Int, $tradeIn: Boolean) {\n  kortrosFlats(\n    filter: {project: $project, building_id: $building_id, queue: $queue, section: $section, floor: $floor, price: $price, price_meter: $price_meter, area: $area, filter: $filter, active: $active, guid: $guid, room: $room, layouttype: $layouttype, logic: $logic, plans_format: $plans_format, sort_by: $sort_by, sort: $sort, limit: $limit, from: $from, finish: $finish, typicalFinishingType: $typicalFinishingType, is_apartament: $is_apartament, readiness: $readiness, real_building_num: $real_building_num, keyIssuance: $keyIssuance, beginYear: $beginYear, readyYear: $readyYear, readyQuarter: $readyQuarter, preview: $preview, address: $address, subtype: $subtype, patio: $patio, terrace: $terrace, is_highceiling: $is_highceiling, design: $design, extensions: $extensions, black_friday: $black_friday, tradeIn: $tradeIn}\n  ) {\n    flats {\n      address\n      beginYear\n      black_friday\n      buildingNums\n      building_id\n      ceiling_height\n      constructorLayout\n      cost_per_meter\n      crm_status\n      design\n      discount\n      discountM2\n      extensions {\n        window_side_choices\n        window_view_choices\n        benefit_choices\n        promotion_choices\n        plan_rotation_value\n      }\n      firstMixedField\n      floor_number\n      guid\n      initial_fee\n      is_apartament\n      is_highceiling\n      keyIssuance\n      layouttype\n      mixed\n      mixedStep\n      monthly_pay\n      number\n      patio\n      pl\n      plan\n      project\n      queue\n      readiness\n      readyQuarter\n      readyYear\n      real_building_num\n      room_count\n      saleM2\n      salePercent\n      saleSum\n      secondMixedField\n      section_number\n      square\n      status\n      subtype\n      terrace\n      total_cost\n      tradeIn\n      type_finish\n      typicalFinishingType\n      window_view\n      window_view_panorama\n      window_view_render\n    }\n    summary {\n      beginYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      real_building_num {\n        selected\n        value\n      }\n      cost_per_meter {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      floor_number {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      queue {\n        selected\n        value\n      }\n      readyQuarter {\n        selected\n        value\n      }\n      readyYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      room_count {\n        availableValue\n        room_count\n        selected\n        totalValue\n      }\n      section_number {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      square {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      typicalFinishingType {\n        key\n        totalValue\n        availableValue\n        selected\n      }\n      total_cost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      total_flats_count {\n        selected\n        selectedWithMixed\n        total\n      }\n      total_flats_count_projects {\n        project\n        selected\n        total\n      }\n      subtype_projects {\n        project\n        countableData {\n          subtype\n          count\n          selected\n        }\n      }\n      patio {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      terrace {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      design {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      extensions {\n        window_side_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        window_view_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        benefit_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        promotion_choices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n      }\n    }\n  }\n}\n    ',
    'variables': {
        'guid': [],
        'project': [
            'ultima',
            'baumanhouse',
            'tate',
            'headliner',
            'perhushkovo',
            'ilove',
        ],
        'limit': 12,
        'sort_by': 'total_cost',
        'sort': 'ASC',
        'extensions': {},
        'from': 12,
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
            'to': None,
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
        'preview': False,
        'patio': None,
        'is_highceiling': None,
        'tradeIn': False,
        'black_friday': None,
    },
    'operationName': 'Flats',
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
