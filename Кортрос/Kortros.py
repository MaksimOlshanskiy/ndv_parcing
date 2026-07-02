import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Иногда нужно обновлять куки и json_data
USE_COOKIES = True  # Если API перестанет работать, установить в False

cookies = {
    'cookieConsentAccepted': 'false',
    'uxs_uid': '87aae340-5cdc-11f1-a249-f31348d18da9',
    'qrator_jsr': 'v2.0.1782113209.099.05b5ca05Pz9JeRd0|MthGBxctP4el3wnE|DOG93dzAeiKrdXREYKVft32aQQJ7x4lEE6rpV0F1DydXc4D5476iqslCEGT4Q9sETqBRP9HPNpvYLPNZHV7yCg==-Z6Q1L1OY4DaemUBvfCL54r+8/U4=-00',
    'qrator_jsid2': 'v2.0.1782113209.099.05b5ca05Pz9JeRd0|tx4ygBS0g4wfa2do|TXqXsPI3yGO7+HY7eYtzH/2nSTSDfgrXNYxRQ0w08rrkp6d6nOegcdFwD+Gi9VfADbjCtqTToWgU+412Kids3Cscrzw57DZeZZxEs5zt5/4ZvPjGusnKwV7cY6Xsagvrlm0S6HA1FggPj4N4DlKx9Q==-+AipORMBmljSnRlWDDsTsCd9Cs4=',
    '_ym_uid': '1782113212698304837',
    '_ym_d': '1782113212',
    '_ym_visorc': 'w',
    '_cmg_csstVoE91': '1782113213',
    '_comagic_idVoE91': '10828121062.14994880137.1782113212',
    '_ym_isad': '2',
    'adrdel': '1782113219038',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782199619087%2C%22sl%22%3A%7B%22224%22%3A1782113219087%2C%221228%22%3A1782113219087%7D%7D',
}

headers = {
    'Accept': 'application/graphql-response+json, application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://kortros.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://kortros.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'cookieConsentAccepted=false; uxs_uid=87aae340-5cdc-11f1-a249-f31348d18da9; qrator_jsr=v2.0.1782113209.099.05b5ca05Pz9JeRd0|MthGBxctP4el3wnE|DOG93dzAeiKrdXREYKVft32aQQJ7x4lEE6rpV0F1DydXc4D5476iqslCEGT4Q9sETqBRP9HPNpvYLPNZHV7yCg==-Z6Q1L1OY4DaemUBvfCL54r+8/U4=-00; qrator_jsid2=v2.0.1782113209.099.05b5ca05Pz9JeRd0|tx4ygBS0g4wfa2do|TXqXsPI3yGO7+HY7eYtzH/2nSTSDfgrXNYxRQ0w08rrkp6d6nOegcdFwD+Gi9VfADbjCtqTToWgU+412Kids3Cscrzw57DZeZZxEs5zt5/4ZvPjGusnKwV7cY6Xsagvrlm0S6HA1FggPj4N4DlKx9Q==-+AipORMBmljSnRlWDDsTsCd9Cs4=; _ym_uid=1782113212698304837; _ym_d=1782113212; _ym_visorc=w; _cmg_csstVoE91=1782113213; _comagic_idVoE91=10828121062.14994880137.1782113212; _ym_isad=2; adrdel=1782113219038; adrcid=A0r9KB4fc8duMUv2jPsp-tg; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782199619087%2C%22sl%22%3A%7B%22224%22%3A1782113219087%2C%221228%22%3A1782113219087%7D%7D',
}


json_data = {
    'query': '\n    query Flats($project: [String]!, $buildingId: [Int], $queue: [Int], $section: [Int], $floor: FRange, $priceMeter: FRange, $area: FRange, $filter: [FlatFilter], $active: Boolean, $guid: [String], $room: [Int], $layoutType: [String], $logic: Logic, $plansFormat: Format, $sortBy: [String], $sort: [Sort], $limit: Int, $from: Int, $finish: Boolean, $typicalFinishingType: [String], $isApartment: Boolean, $readiness: String, $realBuildingNum: [String], $keyIssuance: Boolean, $beginYear: [Int], $readyYear: [Int], $readyQuarter: [Int], $realCost: FRange, $preview: Boolean, $address: String, $subtype: [String], $patio: Boolean, $penthouse: Boolean, $terrace: Boolean, $isHighceiling: Boolean, $design: Boolean, $extensions: FlatObjectExtensionsInput, $blackFriday: Int, $tradeIn: Boolean, $mobileVersion: Boolean, $generalCatalog: Boolean, $regionId: Int, $needBanners: Boolean, $needMixing: Boolean) {\n  kortrosFlats(\n    filter: {project: $project, buildingId: $buildingId, queue: $queue, section: $section, floor: $floor, priceMeter: $priceMeter, area: $area, filter: $filter, active: $active, guid: $guid, room: $room, layoutType: $layoutType, logic: $logic, plansFormat: $plansFormat, sortBy: $sortBy, sort: $sort, limit: $limit, from: $from, finish: $finish, typicalFinishingType: $typicalFinishingType, isApartment: $isApartment, readiness: $readiness, realBuildingNum: $realBuildingNum, keyIssuance: $keyIssuance, beginYear: $beginYear, readyYear: $readyYear, readyQuarter: $readyQuarter, realCost: $realCost, preview: $preview, address: $address, subtype: $subtype, patio: $patio, penthouse: $penthouse, terrace: $terrace, isHighceiling: $isHighceiling, design: $design, extensions: $extensions, blackFriday: $blackFriday, tradeIn: $tradeIn, needBanners: $needBanners, mobileVersion: $mobileVersion, generalCatalog: $generalCatalog, regionId: $regionId, needMixing: $needMixing}\n  ) {\n    flats {\n      address\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        isLeadForm\n        catalogType\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n      beginYear\n      blackFriday\n      buildingNums\n      buildingId\n      ceilingHeight\n      constructorLayout\n      costPerMeter\n      crmStatus\n      oralReserv\n      design\n      discount\n      discountM2\n      extensions {\n        windowSideChoices\n        windowViewChoices\n        benefitChoices\n        promotionChoices\n        planRotationValue\n      }\n      firstMixedField\n      floorNumber\n      guid\n      initialFee\n      isApartment\n      isHighceiling\n      keyIssuance\n      layoutType\n      mixed\n      mixedStep\n      monthlyPay\n      number\n      numberBti\n      patio\n      pl\n      plan\n      project\n      penthouse\n      queue\n      readiness\n      readyQuarter\n      readyYear\n      realBuildingNum\n      roomCount\n      saleM2\n      salePercent\n      saleSum\n      secondMixedField\n      sectionNumber\n      square\n      status\n      subtype\n      terrace\n      totalCost\n      tradeIn\n      finishType\n      typicalFinishingType\n      windowView\n      windowViewPanorama\n      windowViewRender\n    }\n    horizontalBanners {\n      position\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        isLeadForm\n        catalogType\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n    }\n    summary {\n      beginYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      realBuildingNum {\n        selected\n        value\n      }\n      costPerMeter {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      floorNumber {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      queue {\n        selected\n        value\n      }\n      readyQuarter {\n        selected\n        value\n      }\n      readyYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      readyYearList\n      keyIssuance {\n        ...booleanTypeData\n      }\n      penthouse {\n        ...booleanTypeData\n      }\n      isApartment {\n        ...booleanTypeData\n      }\n      tradeIn {\n        ...booleanTypeData\n      }\n      roomCount {\n        availableValue\n        roomCount\n        selected\n        totalValue\n      }\n      sectionNumber {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      square {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      typicalFinishingType {\n        key\n        totalValue\n        availableValue\n        selected\n      }\n      totalCost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      realCost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      totalFlatsCount {\n        selected\n        selectedWithMixed\n        total\n      }\n      totalFlatsCountProjects {\n        project\n        selected\n        total\n      }\n      subtypeProjects {\n        project\n        countableData {\n          subtype\n          count\n          selected\n        }\n      }\n      patio {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      terrace {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      design {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      extensions {\n        windowSideChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        windowViewChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        benefitChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        promotionChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n      }\n      layoutType {\n        availableValue\n        layoutType\n        selected\n        totalValue\n      }\n    }\n  }\n}\n    \n    fragment booleanTypeData on BooleanTypeData {\n  selected\n  availableValue\n  totalValue\n  value\n}\n    ',
    'variables': {
        'guid': [],
        'project': [
            'ultima',
            'baumanhouse',
            'secretgarden',
            'tate',
            'headliner',
            'perhushkovo',
            'ilove',
        ],
        'penthouse': None,
        'section': None,
        'limit': 12,
        'sortBy': [
            'real_cost',
        ],
        'sort': [
            'ASC',
        ],
        'extensions': {},
        'generalCatalog': True,
        'regionId': 1,
        'from': 12,
        'isApartment': None,
        'layoutType': [],
        'finish': None,
        'design': None,
        'typicalFinishingType': [],
        'floor': {
            'from': None,
            'to': None,
        },
        'realCost': {
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
        'subtype': [
            '01',
            '05',
        ],
        'mobileVersion': True,
        'needBanners': True,
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
        print(response.status_code)

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
            # type = flat.get("layoutType", '')
            #
            # if type in [0, '1С']:
            #     room_count = 'студия'
            if flat['isApartment']:
                type = 'Апартаменты'
            else:
                type = 'Квартиры'
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
            srok_sdachi_old = f"{flat['readyQuarter']} кв {flat['readyYear']}"


            if old_price == price:
                price = None
            elif price == 0:
                price= None

            count += 1

            print(f"{count}, {project}, прайс: {price}, отделка: {finish_type}, корпус: {korpus}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', status, '', '', developer, '',
                      district, '', '', korpus.replace('Башня-', ''), '', '', srok_sdachi, srok_sdachi_old, '', '', type,
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
