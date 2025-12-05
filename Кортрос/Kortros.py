import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Иногда нужно обновлять куки
USE_COOKIES = True  # Если API перестанет работать, установить в False

cookies = {
    '_ym_uid': '174732046945412953',
    '_ym_d': '1762769942',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'qrator_jsr': 'v2.0.1764602319.151.5b6ce31flAXvmHcU|LWtmKfibrKRdePVt|XCjBYnPlKqzcuyIoR+GrPkTom21M3RZqg4MzFHowV2L12mHTlrBUqd/kC1FLRz6sqX/PnvlOH6hsrVg8dpB52g==-EK5M6UeKrE+Rw668SzGBtKrVrgU=-00',
    'qrator_jsid2': 'v2.0.1764602319.151.5b6ce31flAXvmHcU|IXIkjcYYI2tcHJlj|a5Po+f+rqliI5k32GQWPdJH37hUGa+OQaT2aYSdTbhPFG9xXZJiY6gUnCD1jj09sJ0ALgN9RkHHJqJqkVMOly2CWlsdBQGaZcHw7JPfcTUkrD3gvdhKx7qUqiVeSgzrZU0cPaCla9/vCN4eJ9rWyqD+nrrm3w5Fc2ekFpljuTeU=-JU90BUgB1P7hkL+vrtLPR5mzsfA=',
    'cookieConsentAccepted': 'false',
    '_cmg_csstVoE91': '1764602327',
    '_comagic_idVoE91': '10114073817.14189255292.1764602326',
    'JSESSIONID': 'D3B748D986CA5DCDCF3FF57FB1D3D2ED',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764688729484%2C%22sl%22%3A%7B%22224%22%3A1764602329484%2C%221228%22%3A1764602329484%7D%7D',
    'adrdel': '1764602329821',
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=174732046945412953; _ym_d=1762769942; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; qrator_jsr=v2.0.1764602319.151.5b6ce31flAXvmHcU|LWtmKfibrKRdePVt|XCjBYnPlKqzcuyIoR+GrPkTom21M3RZqg4MzFHowV2L12mHTlrBUqd/kC1FLRz6sqX/PnvlOH6hsrVg8dpB52g==-EK5M6UeKrE+Rw668SzGBtKrVrgU=-00; qrator_jsid2=v2.0.1764602319.151.5b6ce31flAXvmHcU|IXIkjcYYI2tcHJlj|a5Po+f+rqliI5k32GQWPdJH37hUGa+OQaT2aYSdTbhPFG9xXZJiY6gUnCD1jj09sJ0ALgN9RkHHJqJqkVMOly2CWlsdBQGaZcHw7JPfcTUkrD3gvdhKx7qUqiVeSgzrZU0cPaCla9/vCN4eJ9rWyqD+nrrm3w5Fc2ekFpljuTeU=-JU90BUgB1P7hkL+vrtLPR5mzsfA=; cookieConsentAccepted=false; _cmg_csstVoE91=1764602327; _comagic_idVoE91=10114073817.14189255292.1764602326; JSESSIONID=D3B748D986CA5DCDCF3FF57FB1D3D2ED; _ym_isad=2; _ym_visorc=w; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1764688729484%2C%22sl%22%3A%7B%22224%22%3A1764602329484%2C%221228%22%3A1764602329484%7D%7D; adrdel=1764602329821',
}

json_data = {
    'query': '\n    query Flats($project: [String]!, $buildingId: [Int], $queue: [Int], $section: [Int], $floor: FRange, $price: FRange, $priceMeter: FRange, $area: FRange, $filter: [FlatFilter], $active: Boolean, $guid: [String], $room: [Int], $layoutType: [String], $logic: Logic, $plansFormat: Format, $sortBy: String, $sort: Sort, $limit: Int, $from: Int, $finish: Boolean, $typicalFinishingType: [String], $isApartment: Boolean, $readiness: String, $realBuildingNum: [String], $keyIssuance: Boolean, $beginYear: [Int], $readyYear: [Int], $readyQuarter: [Int], $preview: Boolean, $address: String, $subtype: [String], $patio: Boolean, $terrace: Boolean, $isHighceiling: Boolean, $design: Boolean, $extensions: FlatObjectExtensionsInput, $blackFriday: Int, $tradeIn: Boolean, $mobileVersion: Boolean, $generalCatalog: Boolean, $regionId: Int) {\n  kortrosFlats(\n    filter: {project: $project, buildingId: $buildingId, queue: $queue, section: $section, floor: $floor, price: $price, priceMeter: $priceMeter, area: $area, filter: $filter, active: $active, guid: $guid, room: $room, layoutType: $layoutType, logic: $logic, plansFormat: $plansFormat, sortBy: $sortBy, sort: $sort, limit: $limit, from: $from, finish: $finish, typicalFinishingType: $typicalFinishingType, isApartment: $isApartment, readiness: $readiness, realBuildingNum: $realBuildingNum, keyIssuance: $keyIssuance, beginYear: $beginYear, readyYear: $readyYear, readyQuarter: $readyQuarter, preview: $preview, address: $address, subtype: $subtype, patio: $patio, terrace: $terrace, isHighceiling: $isHighceiling, design: $design, extensions: $extensions, blackFriday: $blackFriday, tradeIn: $tradeIn, needBanners: true, mobileVersion: $mobileVersion, generalCatalog: $generalCatalog, regionId: $regionId}\n  ) {\n    flats {\n      address\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n      beginYear\n      blackFriday\n      buildingNums\n      buildingId\n      ceilingHeight\n      constructorLayout\n      costPerMeter\n      crmStatus\n      oralReserv\n      design\n      discount\n      discountM2\n      extensions {\n        windowSideChoices\n        windowViewChoices\n        benefitChoices\n        promotionChoices\n        planRotationValue\n      }\n      firstMixedField\n      floorNumber\n      guid\n      initialFee\n      isApartment\n      isHighceiling\n      keyIssuance\n      layoutType\n      mixed\n      mixedStep\n      monthlyPay\n      number\n      numberBti\n      patio\n      pl\n      plan\n      project\n      queue\n      readiness\n      readyQuarter\n      readyYear\n      realBuildingNum\n      roomCount\n      saleM2\n      salePercent\n      saleSum\n      secondMixedField\n      sectionNumber\n      square\n      status\n      subtype\n      terrace\n      totalCost\n      tradeIn\n      finishType\n      typicalFinishingType\n      windowView\n      windowViewPanorama\n      windowViewRender\n    }\n    horizontalBanners {\n      position\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n    }\n    summary {\n      beginYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      realBuildingNum {\n        selected\n        value\n      }\n      costPerMeter {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      floorNumber {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      queue {\n        selected\n        value\n      }\n      readyQuarter {\n        selected\n        value\n      }\n      readyYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      roomCount {\n        availableValue\n        room_count\n        selected\n        totalValue\n      }\n      sectionNumber {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      square {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      typicalFinishingType {\n        key\n        totalValue\n        availableValue\n        selected\n      }\n      totalCost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      totalFlatsCount {\n        selected\n        selectedWithMixed\n        total\n      }\n      totalFlatsCountProjects {\n        project\n        selected\n        total\n      }\n      subtypeProjects {\n        project\n        countableData {\n          subtype\n          count\n          selected\n        }\n      }\n      patio {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      terrace {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      design {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      extensions {\n        windowSideChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        windowViewChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        benefitChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        promotionChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n      }\n    }\n  }\n}\n    ',
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
        'sort_by': 'totalCost',
        'sort': 'ASC',
        'extensions': {},
        'generalCatalog': True,
        'regionId': 1,
        'sortBy': 'totalCost',
        'from': 12,
        'layoutType': [],
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
        'realBuildingNum': [],
        'keyIssuance': None,
        'readiness': None,
        'readyYear': [],
        'terrace': None,
        'preview': False,
        'patio': None,
        'isHighceiling': None,
        'tradeIn': False,
        'blackFriday': None,
        'subtype': '01',
        'mobileVersion': False,
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
            if not project:
                continue
            status = ''
            srok_sdachi = ''
            developer = "Кортрос"
            district = ''
            korpus = flat.get('realBuildingNum', '')
            room_count = flat.get("roomCount", '')
            type = flat.get("layoutType", '')

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
            try:
                old_price = flat["totalCost"]
            except:
                old_price = 0
            price = int(round(flat.get("discount", ''),0))
            section = ''
            floor = flat.get("floorNumber", '')

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
save_flats_to_excel(flats, 'all', developer)
