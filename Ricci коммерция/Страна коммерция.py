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
    '_ym_uid': '1779880296344972575',
    '_ym_d': '1779880296',
    '_slid': '6a16d1663b199d321b41b6ce',
    'tmr_lvid': '6356722ab77c2c055757fa9289bbefd8',
    'tmr_lvidTS': '1779880296490',
    'roistat_first_visit': '35392378',
    'slug_city': 'msk',
    '_ct': '1700000000481613454',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    'adrcid': 'A0r9KB4fc8duMUv2jPsp-tg',
    '___dc': 'e2321975-d783-495a-8edb-d1266acfb48a',
    'uxs_uid': 'd8bd3bc0-59bc-11f1-beee-87e5d47b67d9',
    '_slid_server': '6a16d1663b199d321b41b6ce',
    'roistat_visit': '36009717',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'qrator_jsr': '1782110836.998.mNEKfQpbaTNjuyst-lckkfptprmdhk0csjp8e76c89qua932o-00',
    'qrator_jsid': '1782110836.998.mNEKfQpbaTNjuyst-kmlb3j04escim57skg4h4ctafova8ol3',
    'auth.strategy': 'users',
    'cted': 'modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575',
    '_ct_ids': 'om6ni2v1%3A44807%3A750160378',
    '_ct_session_id': '750160378',
    '_ct_site_id': '44807',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'tmr_detect': '0%7C1782110850866',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    '_slsession': 'd003575b-0c5f-43d2-9479-b1afaaa742ab',
    '_slfreq': '68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1782118054',
    'call_s': '___om6ni2v1.1782112656.750160378.529857:1505871.529858:1505872|2___',
    'acs_3': '%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782197259194%2C%22sl%22%3A%7B%22224%22%3A1782110859194%2C%221228%22%3A1782110859194%7D%7D',
    'adrdel': '1782110860112',
    'nuxt_breakpoint_detector': 'md',
    'domain_sid': 'vTpIVe9ROJlyuN_duMpIp%3A1782110878829',
    'csrftoken': 'TY1LwlNAE5BRTBr97nc7dwZp5n6fmcn2',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'form-referer': 'https://strana.com/msk/commercial/filter/?first=24&project=UHJvamVjdFR5cGU6c3RyYW5hLXphcmVjaG5heWE%3D&project=UHJvamVjdFR5cGU6c3RyYW5hLXBhcmtvdmF5YQ%3D%3D&project=UHJvamVjdFR5cGU6c3RyYW5hb3plcm5heWE%3D&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=commercial',
    'origin': 'https://strana.com',
    'platform': 'portal',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://strana.com/msk/commercial/filter/?first=24&project=UHJvamVjdFR5cGU6c3RyYW5hLXphcmVjaG5heWE%3D&project=UHJvamVjdFR5cGU6c3RyYW5hLXBhcmtvdmF5YQ%3D%3D&project=UHJvamVjdFR5cGU6c3RyYW5hb3plcm5heWE%3D&city=Q2l0eVR5cGU6MQ%3D%3D&orderMostExpensive=true&statuses=0&statuses=4&type=commercial',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-csrftoken': 'TY1LwlNAE5BRTBr97nc7dwZp5n6fmcn2',
    # 'cookie': '_ym_uid=1779880296344972575; _ym_d=1779880296; _slid=6a16d1663b199d321b41b6ce; tmr_lvid=6356722ab77c2c055757fa9289bbefd8; tmr_lvidTS=1779880296490; roistat_first_visit=35392378; slug_city=msk; _ct=1700000000481613454; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; adrcid=A0r9KB4fc8duMUv2jPsp-tg; ___dc=e2321975-d783-495a-8edb-d1266acfb48a; uxs_uid=d8bd3bc0-59bc-11f1-beee-87e5d47b67d9; _slid_server=6a16d1663b199d321b41b6ce; roistat_visit=36009717; roistat_visit_cookie_expire=1209600; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; qrator_jsr=1782110836.998.mNEKfQpbaTNjuyst-lckkfptprmdhk0csjp8e76c89qua932o-00; qrator_jsid=1782110836.998.mNEKfQpbaTNjuyst-kmlb3j04escim57skg4h4ctafova8ol3; auth.strategy=users; cted=modId%3Dom6ni2v1%3Bya_client_id%3D1779880296344972575; _ct_ids=om6ni2v1%3A44807%3A750160378; _ct_session_id=750160378; _ct_site_id=44807; _ym_isad=2; _ym_visorc=w; tmr_detect=0%7C1782110850866; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; _slsession=d003575b-0c5f-43d2-9479-b1afaaa742ab; _slfreq=68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1782118054; call_s=___om6ni2v1.1782112656.750160378.529857:1505871.529858:1505872|2___; acs_3=%7B%22hash%22%3A%2278168166d1d84ba31a91bed5b79968efe721107d%22%2C%22nst%22%3A1782197259194%2C%22sl%22%3A%7B%22224%22%3A1782110859194%2C%221228%22%3A1782110859194%7D%7D; adrdel=1782110860112; nuxt_breakpoint_detector=md; domain_sid=vTpIVe9ROJlyuN_duMpIp%3A1782110878829; csrftoken=TY1LwlNAE5BRTBr97nc7dwZp5n6fmcn2',
}


json_data = {
    'query': 'query getLotsList(\n  $type: String,\n  $orderBy: String,\n  $first: Int,\n  $after: String,\n  $id: [ID],\n  $pk: [ID],\n  $status: String,\n  $statuses: [String],\n  $fullFinalPriceMin: String,\n  $fullFinalPriceMax: String,\n  $priceMin: String,\n  $priceMax: String,\n  $areaMin: String,\n  $areaMax: String\n  $floorMin: String,\n  $floorMax: String,\n  $floorChoices: [ID],\n  $completionDate: [String],\n  $building: [ID],\n  $section: [ID],\n  $project: [ID],\n  $rooms: [ID],\n  $action: Boolean,\n  $city: ID,\n  $article: String,\n  $features: [ID],\n  $specialOffers: [ID],\n  $actions: [ID],\n  $landingBlock: Float,\n  $minMortgageMin: String,\n  $minMortgageMax: String,\n  $andSpecialOffers: [ID],\n  $number: String,\n  $projectTemplateType: [String],\n  $commercialPurposes: [ID],\n  $jobsNumbersMin: String,\n  $jobsNumbersMax: String,\n  $metro: [ID]\n) {\n  result: allGlobalFlatsV2(\n    type: $type,\n    orderBy: $orderBy,\n    first: $first,\n    after: $after,\n    id: $id,\n    pk: $pk,\n    status: $status\n    statuses: $statuses\n    fullFinalPriceMin: $fullFinalPriceMin,\n    fullFinalPriceMax: $fullFinalPriceMax,\n    priceMin: $priceMin,\n    priceMax: $priceMax,\n    areaMin: $areaMin,\n    areaMax: $areaMax,\n    floorMin: $floorMin,\n    floorMax: $floorMax,\n    floorChoices: $floorChoices,\n    completionDate: $completionDate,\n    building: $building,\n    section: $section,\n    project: $project,\n    rooms: $rooms,\n    action: $action,\n    city: $city,\n    article: $article,\n    features: $features,\n    specialOffers: $specialOffers,\n    actions: $actions,\n    landingBlock: $landingBlock,\n    minMortgageMin: $minMortgageMin,\n    minMortgageMax: $minMortgageMax,\n    andSpecialOffers: $andSpecialOffers,\n    number: $number,\n    projectTemplateType: $projectTemplateType,\n    commercialPurposes: $commercialPurposes,\n    jobsNumbersMax: $jobsNumbersMax,\n    jobsNumbersMin: $jobsNumbersMin,\n    metro: $metro,\n  ) {\n    totalCount\n    edges {\n      node {\n        id\n        pk\n        status\n        article\n        number\n        type\n        area\n        rooms\n        isEuroLayout\n\n        fullFinalPrice\n        originalPrice\n        percentDiscount\n        installmentPayment\n        officesPaymentByInstallment\n\n        planPngPreview\n        planHover\n        plan\n\n        minFloor\n        maxFloor\n\n        project {\n          id\n          detailProjectId\n          slug\n          name\n          address\n\n          isPremium\n          isBusiness\n          templateType\n\n          isReplacePrice\n          replacedPrice\n          isSoon\n          startSales\n          findOutPrice\n\n          city {\n            id\n            slug\n            name\n          }\n          transport {\n            name\n          }\n          transportTime\n\n          isNotDisplayedFloorPlan\n          isNotDisplayedOfficesFloorPlan # довести до ума\n          openBookingWithSale\n        }\n        building {\n          id\n          name\n          nameDisplay\n          buildingState\n          builtYear\n          readyQuarter\n          currentLevel\n          windowViewPlanLotDisplay\n          windowViewPlanLotPreview\n          bookingActive\n          bookingTypes {\n            id\n            price\n            period\n          }\n          isPriceNdsText\n        }\n        section {\n          id\n          number\n        }\n\n        floor {\n          additionalpointSet {\n            floorPoint\n            kind\n          }\n          plan\n          planWidth\n          planHeight\n          number\n        }\n        buildingTotalFloor\n\n        windowView {\n          ppoi\n          windowviewangleSet {\n            angle\n          }\n        }\n        features {\n          id\n          name\n        }\n        specialOffers {\n          id\n          name\n          badgeLabel\n        }\n\n        bookingDays\n        updateTime\n      }\n    }\n    pageInfo {\n      startCursor\n      endCursor\n      hasNextPage\n      hasPreviousPage\n    }\n  }\n}\n',
    'variables': {
        'first': 24,
        'floorChoices': [],
        'building': [],
        'project': [
            'UHJvamVjdFR5cGU6c3RyYW5hLXphcmVjaG5heWE=',
            'UHJvamVjdFR5cGU6c3RyYW5hLXBhcmtvdmF5YQ==',
            'UHJvamVjdFR5cGU6c3RyYW5hb3plcm5heWE=',
        ],
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
        'type': 'commercial',
        'withoutOffers': None,
        'metro': [],
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
    json_data['variables']['offset'] += 23
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

