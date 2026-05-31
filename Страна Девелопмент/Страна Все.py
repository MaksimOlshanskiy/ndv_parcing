"""

обновляем куки


"""

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

import requests

from functions import save_flats_to_excel

cookies = {
    'qrator_jsr': '1779880293.860.ywcfH1VSRimmYqNz-ssme6t2a3kf7rj89bd1idep819gllr20-00',
    'qrator_jsid': '1779880293.860.ywcfH1VSRimmYqNz-60m14jv25tc7h8jab8039gctceaqkhkm',
    'auth.strategy': 'users',
    '_ym_uid': '1779880296344972575',
    '_ym_d': '1779880296',
    '_slid': '6a16d1663b199d321b41b6ce',
    '_slsession': '7e322021-f882-4f60-855e-4ce84726628c',
    '_slfs': '1779880296484',
    'tmr_lvid': '6356722ab77c2c055757fa9289bbefd8',
    'tmr_lvidTS': '1779880296490',
    'roistat_visit': '35392378',
    'roistat_first_visit': '35392378',
    'roistat_visit_cookie_expire': '1209600',
    '_ym_isad': '2',
    'slug_city': 'msk',
    '_ct_ids': 'om6ni2v1%3A44807%3A741432009',
    '_ct_session_id': '741432009',
    '_ct_site_id': '44807',
    '_ct': '1700000000481613454',
    '_slfreq': '68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1779887497',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking',
    'domain_sid': 'vTpIVe9ROJlyuN_duMpIp%3A1779880297679',
    'adrdel': '1779880297971',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1779966698264%2C%22sl%22%3A%7B%22224%22%3A1779880298264%2C%221228%22%3A1779880298264%7D%7D',
    '___dc': 'e2321975-d783-495a-8edb-d1266acfb48a',
    'tmr_detect': '0%7C1779880299545',
    'call_s': '___om6ni2v1.1779882097.741432009.201255:1331778|2___',
    'nuxt_breakpoint_detector': 'md',
    'csrftoken': 'ltBKbxxmgHeZ9NWtOn3RKWFjK6Ospgf6l7D4OGomjUXF1gj7EAxtwidPV7p69kHQ',
    'uxs_uid': 'd8bd3bc0-59bc-11f1-beee-87e5d47b67d9',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat',
    'origin': 'https://strana.com',
    'platform': 'portal',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-csrftoken': 'ltBKbxxmgHeZ9NWtOn3RKWFjK6Ospgf6l7D4OGomjUXF1gj7EAxtwidPV7p69kHQ',
    # 'cookie': 'qrator_jsr=1779880293.860.ywcfH1VSRimmYqNz-ssme6t2a3kf7rj89bd1idep819gllr20-00; qrator_jsid=1779880293.860.ywcfH1VSRimmYqNz-60m14jv25tc7h8jab8039gctceaqkhkm; auth.strategy=users; _ym_uid=1779880296344972575; _ym_d=1779880296; _slid=6a16d1663b199d321b41b6ce; _slsession=7e322021-f882-4f60-855e-4ce84726628c; _slfs=1779880296484; tmr_lvid=6356722ab77c2c055757fa9289bbefd8; tmr_lvidTS=1779880296490; roistat_visit=35392378; roistat_first_visit=35392378; roistat_visit_cookie_expire=1209600; _ym_isad=2; slug_city=msk; _ct_ids=om6ni2v1%3A44807%3A741432009; _ct_session_id=741432009; _ct_site_id=44807; _ct=1700000000481613454; _slfreq=68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1779887497; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; _ym_visorc=w; cted=modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking; domain_sid=vTpIVe9ROJlyuN_duMpIp%3A1779880297679; adrdel=1779880297971; adrcid=A0r9KB4fc8duMUv2jPsp-tg; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1779966698264%2C%22sl%22%3A%7B%22224%22%3A1779880298264%2C%221228%22%3A1779880298264%7D%7D; ___dc=e2321975-d783-495a-8edb-d1266acfb48a; tmr_detect=0%7C1779880299545; call_s=___om6ni2v1.1779882097.741432009.201255:1331778|2___; nuxt_breakpoint_detector=md; csrftoken=ltBKbxxmgHeZ9NWtOn3RKWFjK6Ospgf6l7D4OGomjUXF1gj7EAxtwidPV7p69kHQ; uxs_uid=d8bd3bc0-59bc-11f1-beee-87e5d47b67d9',
}


json_data = {
    'query': '\n                query getLayoutsListV2(\n    $type: String,\n    $first: Int,\n    $after: String,\n    $fullFinalPriceMin: String,\n    $fullFinalPriceMax: String,\n    $areaMin: String,\n    $areaMax: String,\n    $floorMin: String,\n    $floorMax: String,\n    $completionDate: [String],\n    $building: [ID],\n    $project: [ID],\n    $section: [ID],\n    $rooms: [ID],\n    $action: Boolean,\n    $orderBy: String,\n    $isFavorite: Boolean,\n    $orderRandom: Boolean,\n    $city: ID,\n    $id: [ID],\n    $article: String,\n    $features: [ID],\n    $specialOffers: [ID],\n    $andSpecialOffers: [ID],\n    $specialOffersPanel: [ID],\n    $actions: String,\n    $orderMostExpensive: Boolean,\n    $minMortgageMin: String,\n    $minMortgageMax: String,\n    $windowViewProfitbase: [ID],\n    $number: String,\n    $offset: Int,\n    $hasParking: Boolean,\n    $statuses: [String],\n    $withoutOffers: Boolean,\n    $projectTemplateType: [String],\n) {\n    result: allLayouts(\n        type: $type,\n        first: $first,\n        after: $after,\n        fullFinalPriceMin: $fullFinalPriceMin,\n        fullFinalPriceMax: $fullFinalPriceMax,\n        areaMin: $areaMin,\n        areaMax: $areaMax,\n        floorMin: $floorMin,\n        floorMax: $floorMax,\n        completionDate: $completionDate,\n        building: $building,\n        project: $project,\n        section: $section,\n        rooms: $rooms,\n        action: $action,\n        order: $orderBy,\n        isFavorite: $isFavorite,\n        orderRandom: $orderRandom,\n        city: $city,\n        id: $id,\n        article: $article,\n        features: $features,\n        specialOffers: $specialOffers,\n        andSpecialOffers: $andSpecialOffers,\n        specialOffersPanel: $specialOffersPanel,\n        actions: $actions,\n        orderMostExpensive: $orderMostExpensive,\n        minMortgageMin: $minMortgageMin,\n        minMortgageMax: $minMortgageMax,\n        windowViewProfitbase: $windowViewProfitbase,\n        number: $number,\n        offset: $offset,\n        hasParking: $hasParking,\n        statuses: $statuses,\n        withoutOffers: $withoutOffers,\n        projectTemplateType: $projectTemplateType,\n    ) {\n        totalCount\n        edges {\n            node {\n                id\n                pk\n                status\n                article\n                number\n                type\n                area\n                rooms\n\n                flatsCountMoreThan\n                flatCount\n\n                minFlatPriceAfterFiltering\n                fullFinalPrice\n                originalPrice\n                percentDiscount,\n                monthlyPaymentAmount\n\n                planPngPreview\n                minFloorPlan\n                plan\n                planHover\n\n                project {\n                    id\n                    slug\n                    name\n                    isPremium\n                    isBusiness\n                    isReplacePrice\n                    replacedPrice\n                    isNotDisplayedFloorPlan\n\n                    city {\n                        slug\n                    }\n                }\n                building {\n                    id\n                    name\n                    nameDisplay\n                    windowViewPlanLotDisplay\n                }\n                section {\n                    id\n                    number\n                }\n\n                floor {\n                    plan\n                    planWidth\n                    planHeight\n                    number\n                }\n                buildingTotalFloor\n\n                windowView {\n                    ppoi\n                    windowviewangleSet {\n                        angle\n                    }\n                }\n\n                features {\n                    id\n                    name\n                }\n                specialOffers {\n                    id\n                    name\n                }\n            }\n        }\n        pageInfo {\n            startCursor\n            endCursor\n            hasNextPage\n            hasPreviousPage\n        }\n    }\n}\n\n            ',
    'variables': {
        'first': 24,
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
        'withoutOffers': None,
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
        if i['node']['type'] == 'FLAT':
            type = 'Квартиры'
        else:
            type = i['node']['type']
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

save_flats_to_excel(flats, project, developer)

