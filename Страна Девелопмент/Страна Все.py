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
    'slug_city': 'msk',
    '_ym_uid': '1742906680495120652',
    '_ym_d': '1769525500',
    'tmr_lvid': 'dfa41b5563807a150803810c3db1bd53',
    'tmr_lvidTS': '1742906679116',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    '_slid': '68a8603de9e1a45ab72450e9',
    '_ct': '1700000000451542616',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '___dc': '7f88fd35-7882-4206-b93a-bab62aea98bc',
    '_slid_server': '68a8603de9e1a45ab72450e9',
    'qrator_jsr': '1775659767.326.mG0DdqPLwPTM12ke-m05g5k6e3m6fgkj4upm2kh0com3g2s7q-00',
    'qrator_jsid': '1775659767.326.mG0DdqPLwPTM12ke-g0vndadacdjolft5erp9tdmhk2cm3cvb',
    'auth.strategy': 'users',
    '_slsession': '1afa4da4-0202-4408-b398-f2279cae4200',
    'cted': 'modId%3Dom6ni2v1%3Bya_client_id%3D1742906680495120652',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_ct_ids': 'om6ni2v1%3A44807%3A723908496',
    '_ct_session_id': '723908496',
    '_ct_site_id': '44807',
    'domain_sid': '5V7Z2Dbg0blJdGi5wSPww%3A1775659772040',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1775746172491%2C%22sl%22%3A%7B%22224%22%3A1775659772491%2C%221228%22%3A1775659772491%7D%7D',
    'adrdel': '1775659772919',
    'roistat_visit': '33908504',
    'roistat_visit_cookie_expire': '1209600',
    'tmr_detect': '0%7C1775659773395',
    'roistat_marker': 'seo_yandex_search',
    'roistat_marker_old': 'seo_yandex_search',
    '_slfreq': '68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1775666976',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'call_s': '___om6ni2v1.1775661598.723908496.529857:1505871.529858:1505872|2___',
    'csrftoken': '6POAuNTDqKNMw5WqtwJFobm8OTmdmXulqPujpngjUxgBpZfdQEd5wIQQtTVFYyfm',
    'nuxt_breakpoint_detector': 'sm',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat',
    'origin': 'https://strana.com',
    'platform': 'portal',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/flats/?first=24&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=flat',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-csrftoken': '6POAuNTDqKNMw5WqtwJFobm8OTmdmXulqPujpngjUxgBpZfdQEd5wIQQtTVFYyfm',
    # 'cookie': 'slug_city=msk; _ym_uid=1742906680495120652; _ym_d=1769525500; tmr_lvid=dfa41b5563807a150803810c3db1bd53; tmr_lvidTS=1742906679116; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; _slid=68a8603de9e1a45ab72450e9; _ct=1700000000451542616; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; ___dc=7f88fd35-7882-4206-b93a-bab62aea98bc; _slid_server=68a8603de9e1a45ab72450e9; qrator_jsr=1775659767.326.mG0DdqPLwPTM12ke-m05g5k6e3m6fgkj4upm2kh0com3g2s7q-00; qrator_jsid=1775659767.326.mG0DdqPLwPTM12ke-g0vndadacdjolft5erp9tdmhk2cm3cvb; auth.strategy=users; _slsession=1afa4da4-0202-4408-b398-f2279cae4200; cted=modId%3Dom6ni2v1%3Bya_client_id%3D1742906680495120652; _ym_isad=2; _ym_visorc=w; _ct_ids=om6ni2v1%3A44807%3A723908496; _ct_session_id=723908496; _ct_site_id=44807; domain_sid=5V7Z2Dbg0blJdGi5wSPww%3A1775659772040; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1775746172491%2C%22sl%22%3A%7B%22224%22%3A1775659772491%2C%221228%22%3A1775659772491%7D%7D; adrdel=1775659772919; roistat_visit=33908504; roistat_visit_cookie_expire=1209600; tmr_detect=0%7C1775659773395; roistat_marker=seo_yandex_search; roistat_marker_old=seo_yandex_search; _slfreq=68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1775666976; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; call_s=___om6ni2v1.1775661598.723908496.529857:1505871.529858:1505872|2___; csrftoken=6POAuNTDqKNMw5WqtwJFobm8OTmdmXulqPujpngjUxgBpZfdQEd5wIQQtTVFYyfm; nuxt_breakpoint_detector=sm',
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

