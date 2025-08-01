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
    'qrator_jsid': '1753693176.811.s2vwYJLagZrzDcta-be3tj1bl3vcpv13fu0gp34jbun3g392v',
    'auth.strategy': 'users',
    'slug_city': 'msk',
    '_ymab_param': '8Ii4WKTXM68hlz29bowwz2KASOhfWM2565xObp4iXZjMERJjR22xyTeNQfcLCOzFU5-QPuwo-vhCS7xlr7GLEI4YzLM',
    'tmr_lvid': 'dfa41b5563807a150803810c3db1bd53',
    'tmr_lvidTS': '1742906679116',
    'roistat_visit': '26597184',
    'roistat_visit_cookie_expire': '1209600',
    '_ym_uid': '1742906680495120652',
    '_ym_d': '1753693186',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': '5V7Z2Dbg0blJdGi5wSPww%3A1753693187182',
    '_ct_ids': 'om6ni2v1%3A44807%3A618422048',
    '_ct_session_id': '618422048',
    '_ct_site_id': '44807',
    'call_s': '___om6ni2v1.1753694984.618422048.197416:602039|2___',
    '_ct': '1700000000404488947',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'rai': '4651ff7441e717a9bf891e98848e4b5c',
    'cted': 'modId%3Dom6ni2v1%3Bya_client_id%3D1742906680495120652',
    'tmr_detect': '0%7C1753693188412',
    '___dc': '7f88fd35-7882-4206-b93a-bab62aea98bc',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'nuxt_breakpoint_detector': 'sm',
    'csrftoken': 'd9FGrPQ7nD6jgHPeM6C30T6GOifECtb92CVfw4CDmeCl27JTBw23fvnbSMlgLg28',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat&utm_referrer=https%3A%2F%2Fwww.google.com%2F&page=4',
    'origin': 'https://strana.com',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat&utm_referrer=https%3A%2F%2Fwww.google.com%2F&page=4',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-csrftoken': 'd9FGrPQ7nD6jgHPeM6C30T6GOifECtb92CVfw4CDmeCl27JTBw23fvnbSMlgLg28',
    # 'cookie': 'qrator_jsid=1753693176.811.s2vwYJLagZrzDcta-be3tj1bl3vcpv13fu0gp34jbun3g392v; auth.strategy=users; slug_city=msk; _ymab_param=8Ii4WKTXM68hlz29bowwz2KASOhfWM2565xObp4iXZjMERJjR22xyTeNQfcLCOzFU5-QPuwo-vhCS7xlr7GLEI4YzLM; tmr_lvid=dfa41b5563807a150803810c3db1bd53; tmr_lvidTS=1742906679116; roistat_visit=26597184; roistat_visit_cookie_expire=1209600; _ym_uid=1742906680495120652; _ym_d=1753693186; _ym_isad=2; _ym_visorc=w; domain_sid=5V7Z2Dbg0blJdGi5wSPww%3A1753693187182; _ct_ids=om6ni2v1%3A44807%3A618422048; _ct_session_id=618422048; _ct_site_id=44807; call_s=___om6ni2v1.1753694984.618422048.197416:602039|2___; _ct=1700000000404488947; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; rai=4651ff7441e717a9bf891e98848e4b5c; cted=modId%3Dom6ni2v1%3Bya_client_id%3D1742906680495120652; tmr_detect=0%7C1753693188412; ___dc=7f88fd35-7882-4206-b93a-bab62aea98bc; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; nuxt_breakpoint_detector=sm; csrftoken=d9FGrPQ7nD6jgHPeM6C30T6GOifECtb92CVfw4CDmeCl27JTBw23fvnbSMlgLg28',
}

json_data = {
    'query': '\n                query getLayoutsList(\n    $type: String,\n    $first: Int,\n    $after: String,\n    $fullFinalPriceMin: String,\n    $fullFinalPriceMax: String,\n    $areaMin: String,\n    $areaMax: String,\n    $floorMin: String,\n    $floorMax: String,\n    $completionDate: [String],\n    $building: [ID],\n    $project: [ID],\n    $section: [ID],\n    $rooms: [ID],\n    $action: Boolean,\n    $orderBy: String,\n    $isFavorite: Boolean,\n    $orderRandom: Boolean,\n    $city: ID,\n    $id: [ID],\n    $article: String,\n    $features: [ID],\n    $specialOffers: [ID],\n    $andSpecialOffers: [ID],\n    $specialOffersPanel: [ID],\n    $actions: String,\n    $orderMostExpensive: Boolean,\n    $minMortgageMin: String,\n    $minMortgageMax: String,\n    $windowViewProfitbase: [ID],\n    $number: String,\n    $offset: Int,\n    $hasParking: Boolean,\n    $statuses: [String],\n) {\n    result: allLayouts(\n        type: $type,\n        first: $first,\n        after: $after,\n        fullFinalPriceMin: $fullFinalPriceMin,\n        fullFinalPriceMax: $fullFinalPriceMax,\n        areaMin: $areaMin,\n        areaMax: $areaMax,\n        floorMin: $floorMin,\n        floorMax: $floorMax,\n        completionDate: $completionDate,\n        building: $building,\n        project: $project,\n        section: $section,\n        rooms: $rooms,\n        action: $action,\n        order: $orderBy,\n        isFavorite: $isFavorite,\n        orderRandom: $orderRandom,\n        city: $city,\n        id: $id,\n        article: $article,\n        features: $features,\n        specialOffers: $specialOffers,\n        andSpecialOffers: $andSpecialOffers,\n        specialOffersPanel: $specialOffersPanel,\n        actions: $actions,\n        orderMostExpensive: $orderMostExpensive,\n        minMortgageMin: $minMortgageMin,\n        minMortgageMax: $minMortgageMax,\n        windowViewProfitbase: $windowViewProfitbase,\n        number: $number,\n        offset: $offset,\n        hasParking: $hasParking,\n        statuses: $statuses,\n    ) {\n        totalCount\n        edges {\n            node {\n                id\n                pk\n                status\n                article\n                name\n                number\n                type\n                area\n                rooms\n                isEuroLayout\n                flatsCountMoreThan\n                flatCount\n                minFlatPriceAfterFiltering\n                fullFinalPrice\n                originalPrice\n                layoutDiscountSize\n                maxDiscount\n                flatSold\n                planPngPreview\n                planHover\n                minFloorPlan\n                plan\n                minFloor\n                maxFloor\n                project {\n                    id\n                    address\n                    detailProjectId\n                    name\n                    slug\n                    templateType\n                    isReplacePrice\n                    replacedPrice\n                    hidePriceFromBroker\n                    isSoon\n                    startSales\n                    findOutPrice\n                    city {\n                        id\n                        slug\n                        name\n                    }\n                    transport {\n                        name\n                    }\n                    transportTime\n                }\n                building {\n                    id\n                    name\n                    nameDisplay\n                    buildingState\n                    builtYear\n                    readyQuarter\n                    currentLevel\n                    windowViewPlanLotDisplay\n                    windowViewPlanLotPreview\n                }\n                floor {\n                    plan\n                    planWidth\n                    planHeight\n                    number\n                }\n                windowView {\n                    ppoi\n                    windowviewangleSet {\n                        angle\n                    }\n                }\n                features {\n                    name\n                }\n                specialOffers {\n                    id\n                    name\n                    badgeLabel\n                    color\n                    finishDate\n                }\n\n                specialofferSet {\n                    finishDate\n                }\n            }\n        }\n        pageInfo {\n            startCursor\n            endCursor\n            hasNextPage\n            hasPreviousPage\n        }\n    }\n}\n\n            ',
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
        'utm_referrer': 'https://www.google.com/',
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

