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
    '_ct': '1700000000491550923',
    '_ct_client_global_id': '089407ce-d8b4-596e-88ef-eee2bfcb3172',
    'slug_city': 'msk',
    '_slid': '6a16d1663b199d321b41b6ce',
    '_slid_server': '6a16d1663b199d321b41b6ce',
    'auth.strategy': 'users',
    '_ym_uid': '1779880296344972575',
    '_ym_d': '1786522654',
    'tmr_lvid': '6356722ab77c2c055757fa9289bbefd8',
    'tmr_lvidTS': '1779880296490',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1786609054760%2C%22sl%22%3A%7B%22224%22%3A1786522654760%2C%221228%22%3A1786522654760%7D%7D',
    'adrdel': '1786522654793',
    '___dc': 'e2321975-d783-495a-8edb-d1266acfb48a',
    'qrator_jsr': '1787766483.130.IawPaNUcJ9D6ADNa-qmarm7t5pjgei1i8gv8i7d36elacp25f-00',
    'qrator_jsid': '1787766483.130.IawPaNUcJ9D6ADNa-c0mv30h51ajhededgfnfk2imv2qnj74e',
    'cted': 'modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575',
    '_ct_ids': 'om6ni2v1%3A44807%3A768754188',
    '_ct_session_id': '768754188',
    '_ct_site_id': '44807',
    '_slsession': 'c2b0d992-8596-48d1-822f-42fd9c96c643',
    'roistat_visit': '37729662',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_marker': 'seo_google_',
    'roistat_marker_old': 'seo_google_',
    '_slfreq': '68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1787773685',
    'call_s': '___om6ni2v1.1787768287.768754188.201255:1569925|2___',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'nuxt_breakpoint_detector': 'xs',
    'csrftoken': 'xfvgkgOzvvigvnLjOKWopfLbxsJxZncV',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/flats/',
    'origin': 'https://strana.com',
    'platform': 'portal',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/flats/',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'x-csrftoken': 'xfvgkgOzvvigvnLjOKWopfLbxsJxZncV',
    # 'cookie': '_ct=1700000000491550923; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; slug_city=msk; _slid=6a16d1663b199d321b41b6ce; _slid_server=6a16d1663b199d321b41b6ce; auth.strategy=users; _ym_uid=1779880296344972575; _ym_d=1786522654; tmr_lvid=6356722ab77c2c055757fa9289bbefd8; tmr_lvidTS=1779880296490; adrcid=A0r9KB4fc8duMUv2jPsp-tg; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1786609054760%2C%22sl%22%3A%7B%22224%22%3A1786522654760%2C%221228%22%3A1786522654760%7D%7D; adrdel=1786522654793; ___dc=e2321975-d783-495a-8edb-d1266acfb48a; qrator_jsr=1787766483.130.IawPaNUcJ9D6ADNa-qmarm7t5pjgei1i8gv8i7d36elacp25f-00; qrator_jsid=1787766483.130.IawPaNUcJ9D6ADNa-c0mv30h51ajhededgfnfk2imv2qnj74e; cted=modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575; _ct_ids=om6ni2v1%3A44807%3A768754188; _ct_session_id=768754188; _ct_site_id=44807; _slsession=c2b0d992-8596-48d1-822f-42fd9c96c643; roistat_visit=37729662; roistat_visit_cookie_expire=1209600; roistat_marker=seo_google_; roistat_marker_old=seo_google_; _slfreq=68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1787773685; call_s=___om6ni2v1.1787768287.768754188.201255:1569925|2___; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; nuxt_breakpoint_detector=xs; csrftoken=xfvgkgOzvvigvnLjOKWopfLbxsJxZncV',
}


json_data = {
    'query': 'query getLayoutsListV2(\n    $type: String,\n    $first: Int,\n    $after: String,\n    $fullFinalPriceMin: String,\n    $fullFinalPriceMax: String,\n    $areaMin: String,\n    $areaMax: String,\n    $floorMin: String,\n    $floorMax: String,\n    $completionDate: [String],\n    $building: [ID],\n    $project: [ID],\n    $section: [ID],\n    $rooms: [ID],\n    $action: Boolean,\n    $orderBy: String,\n    $isFavorite: Boolean,\n    $orderRandom: Boolean,\n    $city: ID,\n    $id: [ID],\n    $article: String,\n    $features: [ID],\n    $specialOffers: [ID],\n    $andSpecialOffers: [ID],\n    $specialOffersPanel: [ID],\n    $orderMostExpensive: Boolean,\n    $minMortgageMin: String,\n    $minMortgageMax: String,\n    $windowViewProfitbase: [ID],\n    $number: String,\n    $offset: Int,\n    $hasParking: Boolean,\n    $statuses: [String],\n    $withoutOffers: Boolean,\n    $projectTemplateType: [String],\n) {\n    result: allLayouts(\n        type: $type,\n        first: $first,\n        after: $after,\n        fullFinalPriceMin: $fullFinalPriceMin,\n        fullFinalPriceMax: $fullFinalPriceMax,\n        areaMin: $areaMin,\n        areaMax: $areaMax,\n        floorMin: $floorMin,\n        floorMax: $floorMax,\n        completionDate: $completionDate,\n        building: $building,\n        project: $project,\n        section: $section,\n        rooms: $rooms,\n        action: $action,\n        order: $orderBy,\n        isFavorite: $isFavorite,\n        orderRandom: $orderRandom,\n        city: $city,\n        id: $id,\n        article: $article,\n        features: $features,\n        specialOffers: $specialOffers,\n        andSpecialOffers: $andSpecialOffers,\n        specialOffersPanel: $specialOffersPanel,\n        orderMostExpensive: $orderMostExpensive,\n        minMortgageMin: $minMortgageMin,\n        minMortgageMax: $minMortgageMax,\n        windowViewProfitbase: $windowViewProfitbase,\n        number: $number,\n        offset: $offset,\n        hasParking: $hasParking,\n        statuses: $statuses,\n        withoutOffers: $withoutOffers,\n        projectTemplateType: $projectTemplateType,\n    ) {\n        totalCount\n        edges {\n            node {\n                id\n                pk\n                status\n                article\n                number\n                type\n                area\n                rooms\n\n                flatsCountMoreThan\n                flatCount\n                flatsCountAfterFiltering\n\n                minFlatPriceAfterFiltering\n                fullFinalPrice\n                originalPrice\n                percentDiscount,\n                monthlyPaymentAmount\n                firstPayment\n\n                planPngPreview\n                minFloorPlan\n                plan\n                planHover\n\n                project {\n                    id\n                    slug\n                    name\n                    templateType\n                    isReplacePrice\n                    replacedPrice\n                    isNotDisplayedFloorPlan\n\n                    city {\n                        slug\n                    }\n                }\n                building {\n                    id\n                    name\n                    nameDisplay\n                    windowViewPlanLotDisplay\n                }\n                section {\n                    id\n                    number\n                }\n\n                floor {\n                    plan\n                    planWidth\n                    planHeight\n                    number\n                }\n                buildingTotalFloor\n\n                windowView {\n                    ppoi\n                    windowviewangleSet {\n                        angle\n                    }\n                }\n\n                features {\n                    id\n                    name\n                }\n                specialOffers {\n                    id\n                    name\n                }\n\n                actionTimer\n            }\n        }\n        pageInfo {\n            startCursor\n            endCursor\n            hasNextPage\n            hasPreviousPage\n        }\n    }\n}\n',
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
        'metro': [],
        'after': '',
    },
}




flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://strana.com/graphql/', cookies=cookies, headers=headers, json=json_data)
    print(response.status_code)
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
    next_cursor = response.json()['data']['result']['pageInfo']['endCursor']
    json_data['variables']['after'] = next_cursor
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

