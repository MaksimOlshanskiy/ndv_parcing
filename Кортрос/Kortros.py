import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

# Иногда нужно обновлять куки и json_data
USE_COOKIES = True  # Если API перестанет работать, установить в False

cookies = {
    'spid': '1779876879304_d563275472e7daa509a10fb0154bbd8e_xe9ar7ghcwpg2dx1',
    'spsc': '1779876879304_677db50e53ab44b76e86fc36f6bd25cc_i4iKRQbkMcJUe7njxsBLkAuEUrMzFlTfkn4hL9e.OxEZ',
    'PHPSESSID': 'z350aGRB5zhWTpOcMP9XhJIZQwnnrkqo',
    'DOMAIN': 'msk',
    'SiteID': '0000000002',
    'externalId': '54b946ac-963d-4212-9213-8562db2304d3',
    'rrpvid': '120765237761071',
    'scbsid_old': '4097698043',
    'SiteClientID': '4097698043',
    'rcuid': '67011fef2a14462b4409e8d1',
    'sma_session_id': '2716644408',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'SCBstart': '1779876883484',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%2269a8c60d87e15c5e811dc898ec400d63%22%5D',
    'tmr_lvid': 'dc5b0f43aac7a5da6b0fded2ffc702cc',
    'tmr_lvidTS': '1779876883873',
    'domain_sid': '5QDjO_2NkHIr3sSoGF1NI%3A1779876884011',
    '_ym_uid': '1779876884695231886',
    '_ym_d': '1779876884',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstA05bX': '1779876885',
    '_comagic_idA05bX': '13316920474.17776440389.1779876882',
    'number_phone_site': '74951049303',
    'backLink': '%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D14.7%26price%255Bmax%255D%3D79%26obj%255B%255D%3D202%26area%255Bmin%255D%3D20%26area%255Bmax%255D%3D109%26floor%255Bmax%255D%3D52',
    'rr-testCookie': 'testvalue',
    'number_phone_site_arr': '%5B%2274951049303%22%5D',
    'tmr_detect': '0%7C1779876897529',
    'sma_index_activity': '2369',
    'SCBindexAct': '1969',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.lsr.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.lsr.ru/msk/kvartiry-v-novostroikah/?price%5Bmin%5D=14.7&price%5Bmax%5D=79&obj%5B%5D=202&area%5Bmin%5D=20&area%5Bmax%5D=109&floor%5Bmax%5D=52',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'spid=1779876879304_d563275472e7daa509a10fb0154bbd8e_xe9ar7ghcwpg2dx1; spsc=1779876879304_677db50e53ab44b76e86fc36f6bd25cc_i4iKRQbkMcJUe7njxsBLkAuEUrMzFlTfkn4hL9e.OxEZ; PHPSESSID=z350aGRB5zhWTpOcMP9XhJIZQwnnrkqo; DOMAIN=msk; SiteID=0000000002; externalId=54b946ac-963d-4212-9213-8562db2304d3; rrpvid=120765237761071; scbsid_old=4097698043; SiteClientID=4097698043; rcuid=67011fef2a14462b4409e8d1; sma_session_id=2716644408; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; SCBstart=1779876883484; SCBporogAct=5000; smFpId_old_values=%5B%2269a8c60d87e15c5e811dc898ec400d63%22%5D; tmr_lvid=dc5b0f43aac7a5da6b0fded2ffc702cc; tmr_lvidTS=1779876883873; domain_sid=5QDjO_2NkHIr3sSoGF1NI%3A1779876884011; _ym_uid=1779876884695231886; _ym_d=1779876884; _ym_isad=2; _ym_visorc=w; _cmg_csstA05bX=1779876885; _comagic_idA05bX=13316920474.17776440389.1779876882; number_phone_site=74951049303; backLink=%2Fmsk%2Fkvartiry-v-novostroikah%2F%3Fprice%255Bmin%255D%3D14.7%26price%255Bmax%255D%3D79%26obj%255B%255D%3D202%26area%255Bmin%255D%3D20%26area%255Bmax%255D%3D109%26floor%255Bmax%255D%3D52; rr-testCookie=testvalue; number_phone_site_arr=%5B%2274951049303%22%5D; tmr_detect=0%7C1779876897529; sma_index_activity=2369; SCBindexAct=1969',
}


json_data = {
    'query': '\n    query Flats($project: [String]!, $buildingId: [Int], $queue: [Int], $section: [Int], $floor: FRange, $priceMeter: FRange, $area: FRange, $filter: [FlatFilter], $active: Boolean, $guid: [String], $room: [Int], $layoutType: [String], $logic: Logic, $plansFormat: Format, $sortBy: [String], $sort: [Sort], $limit: Int, $from: Int, $finish: Boolean, $typicalFinishingType: [String], $isApartment: Boolean, $readiness: String, $realBuildingNum: [String], $keyIssuance: Boolean, $beginYear: [Int], $readyYear: [Int], $readyQuarter: [Int], $realCost: FRange, $preview: Boolean, $address: String, $subtype: [String], $patio: Boolean, $terrace: Boolean, $isHighceiling: Boolean, $design: Boolean, $extensions: FlatObjectExtensionsInput, $blackFriday: Int, $tradeIn: Boolean, $mobileVersion: Boolean, $generalCatalog: Boolean, $regionId: Int, $needBanners: Boolean, $needMixing: Boolean) {\n  kortrosFlats(\n    filter: {project: $project, buildingId: $buildingId, queue: $queue, section: $section, floor: $floor, priceMeter: $priceMeter, area: $area, filter: $filter, active: $active, guid: $guid, room: $room, layoutType: $layoutType, logic: $logic, plansFormat: $plansFormat, sortBy: $sortBy, sort: $sort, limit: $limit, from: $from, finish: $finish, typicalFinishingType: $typicalFinishingType, isApartment: $isApartment, readiness: $readiness, realBuildingNum: $realBuildingNum, keyIssuance: $keyIssuance, beginYear: $beginYear, readyYear: $readyYear, readyQuarter: $readyQuarter, realCost: $realCost, preview: $preview, address: $address, subtype: $subtype, patio: $patio, terrace: $terrace, isHighceiling: $isHighceiling, design: $design, extensions: $extensions, blackFriday: $blackFriday, tradeIn: $tradeIn, needBanners: $needBanners, mobileVersion: $mobileVersion, generalCatalog: $generalCatalog, regionId: $regionId, needMixing: $needMixing}\n  ) {\n    flats {\n      address\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        isLeadForm\n        catalogType\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n      beginYear\n      blackFriday\n      buildingNums\n      buildingId\n      ceilingHeight\n      constructorLayout\n      costPerMeter\n      crmStatus\n      oralReserv\n      design\n      discount\n      discountM2\n      extensions {\n        windowSideChoices\n        windowViewChoices\n        benefitChoices\n        promotionChoices\n        planRotationValue\n      }\n      firstMixedField\n      floorNumber\n      guid\n      initialFee\n      isApartment\n      isHighceiling\n      keyIssuance\n      layoutType\n      mixed\n      mixedStep\n      monthlyPay\n      number\n      numberBti\n      patio\n      pl\n      plan\n      project\n      queue\n      readiness\n      readyQuarter\n      readyYear\n      realBuildingNum\n      roomCount\n      saleM2\n      salePercent\n      saleSum\n      secondMixedField\n      sectionNumber\n      square\n      status\n      subtype\n      terrace\n      totalCost\n      tradeIn\n      finishType\n      typicalFinishingType\n      windowView\n      windowViewPanorama\n      windowViewRender\n    }\n    horizontalBanners {\n      position\n      banner {\n        id\n        name\n        bannerFormat\n        link\n        isLeadForm\n        catalogType\n        image {\n          id\n          file\n          fileName\n          fileType\n          fileSize\n        }\n      }\n    }\n    summary {\n      beginYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      realBuildingNum {\n        selected\n        value\n      }\n      costPerMeter {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      floorNumber {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      queue {\n        selected\n        value\n      }\n      readyQuarter {\n        selected\n        value\n      }\n      readyYear {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      roomCount {\n        availableValue\n        roomCount\n        selected\n        totalValue\n      }\n      sectionNumber {\n        range {\n          max\n          min\n        }\n        selected\n      }\n      square {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      typicalFinishingType {\n        key\n        totalValue\n        availableValue\n        selected\n      }\n      totalCost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      realCost {\n        available {\n          max\n          min\n        }\n        selected {\n          max\n          min\n        }\n      }\n      totalFlatsCount {\n        selected\n        selectedWithMixed\n        total\n      }\n      totalFlatsCountProjects {\n        project\n        selected\n        total\n      }\n      subtypeProjects {\n        project\n        countableData {\n          subtype\n          count\n          selected\n        }\n      }\n      patio {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      terrace {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      design {\n        value\n        totalValue\n        availableValue\n        selected\n      }\n      extensions {\n        windowSideChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        windowViewChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        benefitChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n        promotionChoices {\n          key\n          totalValue\n          availableValue\n          selected\n        }\n      }\n    }\n  }\n}\n    ',
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
