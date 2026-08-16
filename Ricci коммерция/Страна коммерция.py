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
    '_slfreq': '68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1784293136',
    '_slid_server': '6a16d1663b199d321b41b6ce',
    'qrator_jsr': '1786519549.844.CLrwKAulbOUuX0rm-5tv5r081d25ftfh83pfk7mrk30s9tgq7-00',
    'qrator_jsid': '1786519549.844.CLrwKAulbOUuX0rm-krkkr37jsof9biq0mk8nc26jh9khb1br',
    'auth.strategy': 'users',
    'roistat_visit': '37301350',
    'roistat_visit_cookie_expire': '1209600',
    '_ct_ids': 'om6ni2v1%3A44807%3A764274426',
    '_ct_session_id': '764274426',
    '_ct_site_id': '44807',
    'call_s': '___om6ni2v1.1786521351.764274426.201255:1353707|2___',
    'nuxt_breakpoint_detector': 'md',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'csrftoken': '6HmqEdVSHwZTVX7e4C5mEcTkfoUyV2pI',
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
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'slug-city': 'msk',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'x-csrftoken': '6HmqEdVSHwZTVX7e4C5mEcTkfoUyV2pI',
    # 'cookie': '_ct=1700000000491550923; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; slug_city=msk; _slid=6a16d1663b199d321b41b6ce; _slfreq=68beb63ffb3d7c66230880a6%3A68beb63ffb3d7c66230880ac%3A1784293136; _slid_server=6a16d1663b199d321b41b6ce; qrator_jsr=1786519549.844.CLrwKAulbOUuX0rm-5tv5r081d25ftfh83pfk7mrk30s9tgq7-00; qrator_jsid=1786519549.844.CLrwKAulbOUuX0rm-krkkr37jsof9biq0mk8nc26jh9khb1br; auth.strategy=users; roistat_visit=37301350; roistat_visit_cookie_expire=1209600; _ct_ids=om6ni2v1%3A44807%3A764274426; _ct_session_id=764274426; _ct_site_id=44807; call_s=___om6ni2v1.1786521351.764274426.201255:1353707|2___; nuxt_breakpoint_detector=md; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; csrftoken=6HmqEdVSHwZTVX7e4C5mEcTkfoUyV2pI',
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
        'after': ''
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
    json_data['variables']['after'] = response.json()['data']['result']['pageInfo']['endCursor']
    sleep_time = random.uniform(1, 5)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer)

