import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    'csrftoken': '79b626605860f29864e98c4Ece62981eB656817F78Bb45a9D99f79da3eD70834',
    '_ct_ids': 'fx3i2gmg%3A31009%3A562765811',
    '_ct_session_id': '562765811',
    '_ct_site_id': '31009',
    'call_s': '___fx3i2gmg.1743004306.562765811.220776:954912|2___',
    '_ct': '1000000000384252740',
    'scbsid_old': '2746015342',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'tmr_lvid': 'e278f655c25230a82dc3ec3b3ce6c38a',
    'tmr_lvidTS': '1743002506505',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ga': 'GA1.1.1339904881.1743002507',
    '_ym_uid': '1743002507533584732',
    '_ym_d': '1743002507',
    '_gcl_au': '1.1.1348719861.1743002507',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dfx3i2gmg%3Bclient_id%3D1339904881.1743002507%3Bya_client_id%3D1743002507533584732',
    'domain_sid': 'roW1w7GioM9aILU68vCxN%3A1743002507560',
    'tmr_detect': '0%7C1743002508943',
    '_ga_D1P98QQSXV': 'GS1.1.1743002506.1.1.1743002525.0.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic aWRhcHJvamVjdDoyMjMzMjI=',
    'content-type': 'application/json',
    'origin': 'https://alia.moscow',
    'priority': 'u=1, i',
    'referer': 'https://alia.moscow/flats/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-csrftoken': '79b626605860f29864e98c4Ece62981eB656817F78Bb45a9D99f79da3eD70834',
    # 'cookie': 'csrftoken=79b626605860f29864e98c4Ece62981eB656817F78Bb45a9D99f79da3eD70834; _ct_ids=fx3i2gmg%3A31009%3A562765811; _ct_session_id=562765811; _ct_site_id=31009; call_s=___fx3i2gmg.1743004306.562765811.220776:954912|2___; _ct=1000000000384252740; scbsid_old=2746015342; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; tmr_lvid=e278f655c25230a82dc3ec3b3ce6c38a; tmr_lvidTS=1743002506505; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ga=GA1.1.1339904881.1743002507; _ym_uid=1743002507533584732; _ym_d=1743002507; _gcl_au=1.1.1348719861.1743002507; _ym_isad=2; _ym_visorc=w; cted=modId%3Dfx3i2gmg%3Bclient_id%3D1339904881.1743002507%3Bya_client_id%3D1743002507533584732; domain_sid=roW1w7GioM9aILU68vCxN%3A1743002507560; tmr_detect=0%7C1743002508943; _ga_D1P98QQSXV=GS1.1.1743002506.1.1.1743002525.0.0.0',
}

json_data = {
    'query': 'query allFlats(\n    $first: Int,\n    $after: String,\n    $priceMin: String,\n    $priceMax: String,\n    $areaMin: String,\n    $areaMax: String,\n    $floorMin: String,\n    $floorMax: String,\n    $layout: [ID],\n    $decoration: [String],\n    $usp: [String],\n    $orderBy: String,\n    $building: [ID],\n    $section: [ID],\n    $typeFlat: [ID],\n    $isBlackFriday: Boolean,\n    $isReady: Boolean,\n  \t$window_view: [ID],\n  \t$status: String,\n  \t$key_distribution: [String],\n  \t$sale: String,\n  \t$sale25: Boolean,\n  \t$sale2: Boolean,\n  \t$urbanBlock: [ID],\n    $scenario: String,\n    $subgroup: String,\n    $uspLayout: [String],\n    $uspBalcony: [String],\n    $uspLayoutFeatures: [String],\n  \t$newTypeFlat: [ID],\n    $isSalesStart: Boolean,\n) {\n    allFlats(\n        first: $first,\n        after: $after,\n        priceMin: $priceMin,\n        priceMax: $priceMax,\n        areaMin: $areaMin,\n        areaMax: $areaMax,\n        floorMin: $floorMin,\n        floorMax: $floorMax,\n        layout: $layout,\n        decoration: $decoration,\n        usp: $usp,\n        orderBy: $orderBy,\n        building: $building,\n        section: $section,\n        typeFlat: $typeFlat,\n        isBlackFriday: $isBlackFriday,\n        isReady: $isReady,\n      \twindowView: $window_view,\n      \tstatus: $status,\n      \tkeyDistribution: $key_distribution,\n      \tsale: $sale,\n      \tsale25: $sale25,\n      \tsale2: $sale2,\n      \turbanBlock: $urbanBlock,\n        scenario: $scenario,\n        subgroup: $subgroup,\n        uspLayout: $uspLayout,\n        uspBalcony: $uspBalcony,\n      \tuspLayoutFeatures: $uspLayoutFeatures,\n      \tnewTypeFlat: $newTypeFlat,\n        isSalesStart: $isSalesStart,\n    ) {\n        totalCount\n        edges {\n            node {\n                id\n                slug\n                status\n                isPremium\n                plan\n                area\n                rooms\n                ceilingHeight\n                buildingNumber\n                floorNumber\n                floor {\n                    plan\n                    planWidth\n                    planHeight\n                    section {\n                        building {\n                            hidePriceMortgageBlock\n                            completionQuarter\n                            completionYear\n                            isComplete\n                            lotMiniPlan\n                            lotMiniPlanWidth\n                            lotMiniPlanHeight\n                            numberForSite\n                            urbanBlock {\n                                name\n                            }\n                        }\n                    }\n                    floor {\n                        plan\n                        planWidth\n                        planHeight\n                    }\n                }\n                price\n                originPrice\n                euro\n                highlighting\n                layoutType\n                number\n                type\n                isBlackFriday\n                isPremium\n                isReady\n                sectionNumber\n                isPriceIncreased\n                priceIncreasedFrom\n                priceIncreasedValue\n                windowView {\n                    name\n                }\n                plan2\n                plan2d\n                plan2d2\n                plan3\n                plan2d3\n                planWithFurnish\n                planWithFurnish2\n              \tusp {\n                    id\n                    text\n                    order\n              \t}\n\t\t\t\tuspReady {\n                    id\n                    text\n              \t}\n              \tdecoration {\n                  id\n                  title\n                }\n                salePercent\n              \tsale25\n                subgroupId\n                cardSlides {\n                    id\n                    imagePreview\n                    imageDisplay\n                }\n                sunrayWindowViews{\n                    id\n                    point\n                    azimuth\n                }\n                verticalSection {\n                    id\n                    sunrayWindowViews {\n                        id\n                        point\n                        azimuth\n                    }\n                }\n                similar {\n                    id\n                    slug\n                    status\n                }\n            }\n        }\n        pageInfo {\n            endCursor\n            hasNextPage\n        }\n    }\n}\n',
    'variables': {
        'newTypeFlat': [
            '209',  '280', '210'
        ],
        'first': 22,
        'after': '',
    },
}


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

flats = []
while True:

    response = requests.post('https://alia.moscow/graphql/', cookies=cookies, headers=headers, json=json_data)
    print(response.status_code)

    items = response.json()['data']['allFlats']['edges']

    for i in items:

        url = ''
        developer = "ВиХолдинг"
        project = 'Алиа'
        korpus = f"{i['node']['floor']['section']['building']['urbanBlock']['name']} {i['node']['buildingNumber']}"
        type = i['node']['type']
        if i['node']['decoration']['title'] == "White box":
            finish_type = 'Предчистовая'
        else:
            finish_type = i['node']['decoration']['title']
        room_count = i['node']['rooms']
        try:
            area = float(i['node']['area'])
        except:
            area = ''
        try:
            old_price = int()
        except:
            old_price = ''
        try:
            price = int(i['node']['price'])
        except:
            price = i['node']['price']
        try:
            section = i['node']['sectionNumber']
        except:
            section = ''
        try:
            floor = int(i['node']['floorNumber'])
        except:
            floor = ''
        flat_number = ''

        english = ''
        promzona = ''
        mestopolozhenie = ''
        subway = ''
        distance_to_subway = ''
        time_to_subway = ''
        mck = ''
        distance_to_mck = ''
        time_to_mck = ''
        bkl = ''
        distance_to_bkl = ''
        time_to_bkl = ''
        status = ''
        start = ''
        comment = ''
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        konstruktiv = ''
        klass = ''
        try:
            srok_sdachi = f"{i['node']['floor']['section']['building']['completionQuarter']} кв {i['node']['floor']['section']['building']['completionYear']} года"
        except:
            srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        date = datetime.now()


        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)



    if not items:
        break
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)
    next_page = response.json()['data']['allFlats']['pageInfo']['endCursor']
    json_data['variables']['after'] = next_page

df = pd.DataFrame(flats, columns=['Дата обновления',
 'Название проекта',
 'на англ',
 'промзона',
 'Местоположение',
 'Метро',
 'Расстояние до метро, км',
 'Время до метро, мин',
 'МЦК/МЦД/БКЛ',
 'Расстояние до МЦК/МЦД, км',
 'Время до МЦК/МЦД, мин',
 'БКЛ',
 'Расстояние до БКЛ, км',
 'Время до БКЛ, мин',
 'статус',
 'старт',
 'Комментарий',
 'Девелопер',
 'Округ',
 'Район',
 'Адрес',
 'Эскроу',
 'Корпус',
 'Конструктив',
 'Класс',
 'Срок сдачи',
 'Старый срок сдачи',
 'Стадия строительной готовности',
 'Договор',
 'Тип помещения',
 'Отделка',
 'Кол-во комнат',
 'Площадь, кв.м',
 'Цена кв.м, руб.',
 'Цена лота, руб.',
 'Скидка,%',
 'Цена кв.м со ск, руб.',
 'Цена лота со ск, руб.',
 'секция',
 'этаж',
 'номер'])

current_date = "2025-03-27"

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\ВиХолдинг"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

