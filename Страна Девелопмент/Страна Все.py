import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

cookies = {
    '_ymab_param': '08qI1MeTbZ6KE5qhxDORXMs7AIyYJwpIwhsDMjnwynPzm5XaW_oeb3oCvQ2xP99oJtk32PrPwms2CJ3bdt2feThNs6Y',
    'tmr_lvid': 'dfa41b5563807a150803810c3db1bd53',
    'tmr_lvidTS': '1742906679116',
    'roistat_first_visit': '22659698',
    '_ct': '1700000000371104218',
    '_ga': 'GA1.1.1368495042.1742906680',
    '_ym_uid': '1742906680495120652',
    '_ym_d': '1742906680',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '___dc': '7f88fd35-7882-4206-b93a-bab62aea98bc',
    'uxs_uid': 'eec93500-0976-11f0-97e1-2336612bf0ed',
    'qrator_jsr': '1744813652.518.gOoyTkdBN3fmJCDb-175oktlobnhnvmi4416i2lp9vg36a7ta-00',
    'qrator_jsid': '1744813652.518.gOoyTkdBN3fmJCDb-mvmt8vumh02vakv9vl2qtv9fd6ivepai',
    'auth.strategy': 'users',
    'cted': 'modId%3Dom6ni2v1%3Bclient_id%3D1368495042.1742906680%3Bya_client_id%3D1742906680495120652',
    '_ct_ids': 'om6ni2v1%3A44807%3A574815274',
    '_ct_session_id': '574815274',
    '_ct_site_id': '44807',
    'roistat_visit': '23447266',
    'roistat_visit_cookie_expire': '1209600',
    'domain_sid': '5V7Z2Dbg0blJdGi5wSPww%3A1744813653798',
    '_ga_BE304FWE0N': 'GS1.1.1744813653.6.0.1744813653.0.0.0',
    '_ym_visorc': 'w',
    '_ym_isad': '2',
    'tmr_detect': '0%7C1744813655928',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'auth.selectedCity': 'Q2l0eVR5cGU6MQ%3D%3D',
    'slug_city': 'msk',
    'call_s': '___om6ni2v1.1744815473.574815274.197416:602039|2___',
    'csrftoken': 'n5NOGMDcB2O2lDaqpVWU6AJPRBqzKcepoo8jDhnUMgQq6iRjTrkSiDfL7AVfJkyK',
    'nuxt_breakpoint_detector': 'lg',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/flats/?project=UHJvamVjdFR5cGU6c3RyYW5hb3plcm5heWE%3D&city=Q2l0eVR5cGU6MQ%3D%3D&page=2',
    'origin': 'https://strana.com',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/flats/?project=UHJvamVjdFR5cGU6c3RyYW5hb3plcm5heWE%3D&city=Q2l0eVR5cGU6MQ%3D%3D&page=2',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-csrftoken': 'Rpz8h04sf7rCm6O2VxjKYqJOxeNa1SWvI5AzpcaV8xnodotofgkxoUwv0un8xH8x',
    # 'cookie': '_ymab_param=08qI1MeTbZ6KE5qhxDORXMs7AIyYJwpIwhsDMjnwynPzm5XaW_oeb3oCvQ2xP99oJtk32PrPwms2CJ3bdt2feThNs6Y; tmr_lvid=dfa41b5563807a150803810c3db1bd53; tmr_lvidTS=1742906679116; roistat_first_visit=22659698; roistat_visit_cookie_expire=1209600; _ct=1700000000371104218; _ga=GA1.1.1368495042.1742906680; _ym_uid=1742906680495120652; _ym_d=1742906680; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; ___dc=7f88fd35-7882-4206-b93a-bab62aea98bc; uxs_uid=eec93500-0976-11f0-97e1-2336612bf0ed; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; slug_city=msk; auth.selectedCity=Q2l0eVR5cGU6MQ%3D%3D; auth.strategy=users; cted=modId%3Dom6ni2v1%3Bclient_id%3D1368495042.1742906680%3Bya_client_id%3D1742906680495120652; _ct_site_id=44807; domain_sid=5V7Z2Dbg0blJdGi5wSPww%3A1743426882467; roistat_visit=22828708; roistat_marker=seo_google_; roistat_marker_old=seo_google_; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails%2Croistat_visit%2Croistat_marker%2Croistat_marker_old; _ct_ids=om6ni2v1%3A44807%3A567484541; _ct_session_id=567484541; _ym_isad=2; _ym_visorc=w; qrator_jsid=1743509991.551.MEX1vUAHfhjLRE0Q-edksneec4v82v5ia4l9grmgsusommb1i; call_s=___om6ni2v1.1743512046.567484541.197416:602039|2___; tmr_detect=0%7C1743510249645; nuxt_breakpoint_detector=lg; _ga_BE304FWE0N=GS1.1.1743509993.4.1.1743510260.0.0.0; csrftoken=Rpz8h04sf7rCm6O2VxjKYqJOxeNa1SWvI5AzpcaV8xnodotofgkxoUwv0un8xH8x',
}

json_data = {
    'query': '\n                query getLayoutsList(\n    $type: String,\n    $first: Int,\n    $after: String,\n    $fullFinalPriceMin: String,\n    $fullFinalPriceMax: String,\n    $areaMin: String,\n    $areaMax: String,\n    $floorMin: String,\n    $floorMax: String,\n    $completionDate: [String],\n    $building: [ID],\n    $project: [ID],\n    $section: [ID],\n    $rooms: [ID],\n    $action: Boolean,\n    $orderBy: String,\n    $isFavorite: Boolean,\n    $orderRandom: Boolean,\n    $city: ID,\n    $id: [ID],\n    $article: String,\n    $features: [ID],\n    $specialOffers: [ID],\n    $andSpecialOffers: [ID],\n    $specialOffersPanel: [ID],\n    $actions: String,\n    $orderMostExpensive: Boolean,\n    $minMortgageMin: String,\n    $minMortgageMax: String,\n    $windowViewProfitbase: [ID],\n    $number: String,\n    $offset: Int,\n    $hasParking: Boolean,\n    $statuses: [String],\n) {\n    result: allLayouts(\n        type: $type,\n        first: $first,\n        after: $after,\n        fullFinalPriceMin: $fullFinalPriceMin,\n        fullFinalPriceMax: $fullFinalPriceMax,\n        areaMin: $areaMin,\n        areaMax: $areaMax,\n        floorMin: $floorMin,\n        floorMax: $floorMax,\n        completionDate: $completionDate,\n        building: $building,\n        project: $project,\n        section: $section,\n        rooms: $rooms,\n        action: $action,\n        order: $orderBy,\n        isFavorite: $isFavorite,\n        orderRandom: $orderRandom,\n        city: $city,\n        id: $id,\n        article: $article,\n        features: $features,\n        specialOffers: $specialOffers,\n        andSpecialOffers: $andSpecialOffers,\n        specialOffersPanel: $specialOffersPanel,\n        actions: $actions,\n        orderMostExpensive: $orderMostExpensive,\n        minMortgageMin: $minMortgageMin,\n        minMortgageMax: $minMortgageMax,\n        windowViewProfitbase: $windowViewProfitbase,\n        number: $number,\n        offset: $offset,\n        hasParking: $hasParking,\n        statuses: $statuses,\n    ) {\n        totalCount\n        edges {\n            node {\n                id\n                pk\n                status\n                article\n                name\n                number\n                type\n                area\n                rooms\n                isEuroLayout\n                flatsCountMoreThan\n                flatCount\n                minFlatPriceAfterFiltering\n                fullFinalPrice\n                originalPrice\n                layoutDiscountSize\n                maxDiscount\n                flatSold\n                planPngPreview\n                planHover\n                minFloorPlan\n                plan\n                minFloor\n                maxFloor\n                project {\n                    id\n                    address\n                    detailProjectId\n                    name\n                    slug\n                    templateType\n                    isReplacePrice\n                    replacedPrice\n                    hidePriceFromBroker\n                    isSoon\n                    startSales\n                    findOutPrice\n                    city {\n                        id\n                        slug\n                        name\n                    }\n                    transport {\n                        name\n                    }\n                    transportTime\n                }\n                building {\n                    id\n                    name\n                    nameDisplay\n                    buildingState\n                    builtYear\n                    readyQuarter\n                    currentLevel\n                    windowViewPlanLotDisplay\n                    windowViewPlanLotPreview\n                }\n                floor {\n                    plan\n                    planWidth\n                    planHeight\n                    number\n                }\n                windowView {\n                    ppoi\n                    windowviewangleSet {\n                        angle\n                    }\n                }\n                features {\n                    name\n                }\n                specialOffers {\n                    id\n                    name\n                    badgeLabel\n                    color\n                    finishDate\n                }\n            }\n        }\n        pageInfo {\n            startCursor\n            endCursor\n            hasNextPage\n            hasPreviousPage\n        }\n    }\n}\n\n            ',
    'variables': {
        'first': 23,
        'floorChoices': [],
        'building': [],
        'project': [],
        'section': [],
        'rooms': [],
        'city': 'Q2l0eVR5cGU6MQ==',
        'features': [],
        'specialOffers': [],
        'andSpecialOffers': [],
        'specialOffersPanel': [],
        'orderBy': '',
        'orderMostExpensive': True,
        'actions': [],
        'windowViewProfitbase': [],
        'number': '',
        'hasParking': None,
        'statuses': [
            '0',
            '4',
        ],
        'type': 'flat',
        'offset': 0,

    },
}


flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://strana.com/graphql/', cookies=cookies, headers=headers, json=json_data)

    items = response.json()['data']['result']['edges']


    for i in items:

        url = ''
        developer = "Страна Девелопмент"
        project = i['node']['project']['name']
        korpus = i['node']['building']['nameDisplay']
        type = ''
        finish = i['node']['features']
        try:
            finish_type = 'Без отделки'
            for y in finish:
                if y['name'] == 'Дизайнерская отделка':
                    finish_type = 'С отделкой'
                    break
                elif y['name'] == 'Отделка Whitebox':
                    finish_type = 'Предчистовая'
                    break
        except:
            finish_type = ''

        room_count = i['node']['rooms']
        try:
            area = float(i['node']['area'])
        except:
            area = ''
        try:
            old_price = int(i['node']['originalPrice'])
        except:
            old_price = ''
        try:
            price = int(i['node']['minFlatPriceAfterFiltering'])
        except:
            price = ''
        section = ''
        try:
            floor = int(i['node']['floor']['number'])
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
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''



        print(
            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    if not items:
        break
    json_data['variables']['offset'] += 23
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

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



# Базовый путь для сохранения
base_path = r"Страна Девелопмент"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

