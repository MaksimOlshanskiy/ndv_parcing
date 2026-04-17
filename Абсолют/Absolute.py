import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    'c2d_widget_id': '{%224d21e7c5cfe0cfe896c4562300f40e37%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20f5e48662658a42459bb7%5C%22%2C%5C%22client_token%5C%22:%5C%22b800bc840863db3ec06f2ba00a68bf41%5C%22}%22}',
    'multidb_pin_writes': 'y',
    'csrftoken': 'JoPZp1CVTme2yQ3bSb3eRmb5aPfHSOYJ7i07FGQknfAx4uoj1Q9GMS4XMNlit3cb',
    '_cmg_csstgCGlG': '1775743184',
    '_comagic_idgCGlG': '10590104342.14727273462.1775743183',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.absrealty.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.absrealty.ru/flats',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-csrftoken': 'JoPZp1CVTme2yQ3bSb3eRmb5aPfHSOYJ7i07FGQknfAx4uoj1Q9GMS4XMNlit3cb',
    # 'cookie': 'c2d_widget_id={%224d21e7c5cfe0cfe896c4562300f40e37%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20f5e48662658a42459bb7%5C%22%2C%5C%22client_token%5C%22:%5C%22b800bc840863db3ec06f2ba00a68bf41%5C%22}%22}; multidb_pin_writes=y; csrftoken=JoPZp1CVTme2yQ3bSb3eRmb5aPfHSOYJ7i07FGQknfAx4uoj1Q9GMS4XMNlit3cb; _cmg_csstgCGlG=1775743184; _comagic_idgCGlG=10590104342.14727273462.1775743183',
}

json_data = {
    'query': 'query allFlats(\n    $first: Int\n    $after: String\n    $orderBy: String\n    $priceMin: String\n    $priceMax: String\n    $areaMin: String\n    $areaMax: String\n    $floorNumberMin: String\n    $floorNumberMax: String\n    $rooms: [ID]\n    $facing: Boolean\n    $isWhiteBox: Boolean\n    $project: [ID]\n    $building: [ID]\n    $phase: [ID]\n    $section: [ID]\n    $booked: Boolean\n    $completion: [ID]\n    $completionYear: [ID]\n    $firstFloor: Boolean\n    $lastFloor: Boolean\n    $finishTypes: [ID]\n    $storageOnTheFloor: Boolean\n    $euro: Boolean\n    $beCombined: Boolean\n    $tracing: Boolean\n    $freeLayout: Boolean\n    $fireplace: Boolean\n    $wardrobe: Boolean\n    $enlargedCeilingHeight: Boolean\n    $manyWc: Boolean\n    $balcony: Boolean\n    $loggia: Boolean\n    $terrace: Boolean\n    $bayWindow: Boolean\n    $wardrobeWindow: Boolean\n    $bathroomWindow: Boolean\n    $panoramicWindows: Boolean\n    $cornerWindows: Boolean\n    $extendedVitrifaction: Boolean\n    $windowSides: [ID]\n    $windowViews: [ID]\n    $mortgages: [ID]\n    $hideBuildingFlatsOnPortal: Boolean\n    $apartment: Boolean\n  \t$smart_flat: Boolean\n  \t$smart_building: Boolean\n    $withKitchen: Boolean\n    $kitchenAreaMin: String\n  \t$kitchenAreaMax: String\n    $promotions: [ID]\n) {\n    allFlats(\n        first: $first\n        after: $after\n        orderBy: $orderBy\n        priceMin: $priceMin\n        priceMax: $priceMax\n        areaMin: $areaMin\n        areaMax: $areaMax\n        floorNumberMin: $floorNumberMin\n        floorNumberMax: $floorNumberMax\n        rooms: $rooms\n        facing: $facing\n        isWhiteBox: $isWhiteBox\n        project: $project\n        building: $building\n        phase: $phase\n        booked: $booked\n        completion: $completion\n        completionYear: $completionYear\n        firstFloor: $firstFloor\n        lastFloor: $lastFloor\n        finishTypes: $finishTypes\n        storageOnTheFloor: $storageOnTheFloor\n        euro: $euro\n        beCombined: $beCombined\n        tracing: $tracing\n        freeLayout: $freeLayout\n        fireplace: $fireplace\n        wardrobe: $wardrobe\n        enlargedCeilingHeight: $enlargedCeilingHeight\n        manyWc: $manyWc\n        balcony: $balcony\n        loggia: $loggia\n        terrace: $terrace\n        bayWindow: $bayWindow\n        wardrobeWindow: $wardrobeWindow\n        bathroomWindow: $bathroomWindow\n        panoramicWindows: $panoramicWindows\n        cornerWindows: $cornerWindows\n        extendedVitrifaction: $extendedVitrifaction\n        windowSides: $windowSides\n        windowViews: $windowViews\n        mortgages: $mortgages\n        hideBuildingFlatsOnPortal: $hideBuildingFlatsOnPortal\n        apartment: $apartment\n        section: $section\n      \tsmartFlat: $smart_flat\n      \tsmartBuilding: $smart_building\n        withKitchen: $withKitchen\n        kitchenAreaMin: $kitchenAreaMin\n      \tkitchenAreaMax: $kitchenAreaMax\n        promotions: $promotions\n    ) {\n        totalCount\n        pageInfo {\n            endCursor\n            hasNextPage\n        }\n        edges {\n            node {\n                pk\n                id\n                number\n                rooms\n                area\n                price\n                originPrice\n                minFirstPayment\n                minMonthPayment\n                minFirstPaymentPercent\n                hasDiscount\n                facing\n                plan\n                furniturePlan\n                plan3d\n\n                project {\n                    disableBooking\n                    id\n                    slug\n                    name\n                    title\n                    skipPhase\n                    projectmetroSet {\n                        id\n                        walkingTime\n                        timeOnCar\n                        metro {\n                            id\n                            name\n                        }\n                    }\n                    totalBuildings\n                    totalPhases\n                }\n\n                building {\n                    id\n                    number\n                    totalSections\n                    hasKeys\n                    isParking\n                    completionYear\n                    completionQuarter\n                    completionDate\n                    startSales\n                }\n\n                section {\n                    id\n                    number\n                    totalFloors\n                    group {\n                        name\n                    }\n                }\n\n                floor {\n                    id\n                    number\n                }\n\n                layout {\n                    name\n                    area\n                    layoutwidgetSet {\n                        id\n                        url\n                        name\n                        finishType {\n                            id\n                            title\n                            name\n                        }\n                    }\n                    getFloorPlanWidgets {\n                        id\n                        url\n                        corner2d\n                        view3d360\n                        name\n                        view3d\n                        finishType {\n                            id\n                            title\n                            name\n                        }\n                    }\n                }\n\n                phase {\n                    id\n                    name\n                    number\n\n                    phasemetroSet {\n                        id\n                        timeOnCar\n                        walkingTime\n                        metro {\n                            id\n                            name\n                        }\n                    }\n                }\n                status\n                number\n                rooms\n                area\n                kitchenArea\n                originPrice\n                hasDiscount\n                price\n                plan\n                furniturePlan\n                planWithSize\n                plan3d\n                izometricPlan3d\n\n                facing\n                finishTypesWithPrices {\n                    finishId\n                    finishPrice\n                    originFinishPrice\n                    finishDiscount\n                }\n              \tfinishTypes {\n                    edges {\n                        node {\n                            id\n                            pk\n                            slug\n                            title\n                            shortDescription\n                            filterMiniImage\n                            filterMiniImageDisplay\n                            filterMiniImagePreview\n                            paintRoller {\n                                id\n                                svg\n                            }\n                        }\n                    }\n                }\n                withKitchen\n\n                highlighting\n                highlightingDetail\n                disableBooking\n                inFavorite\n                hasFireplace\n                hasBalcony\n                hasLoggia\n                hasWardrobe\n                wardrobeNumber\n                inCompare\n                hasTerrace\n                smartFlat\n                smartBuilding\n                enlargedCeilingHeight\n                extendedVitrifaction\n                hasStorageOnTheFloor\n                wardrobeHasWindow\n                bathroomHasWindow\n                panoramicWindows\n                cornerWindows\n                windowSidesNumber\n                hasBayWindow\n                hasSpecificView\n                windowDirections\n\n                elevatorsNumber\n                hasStorageInTheHall\n                ceilingHeight\n                flatSizeType\n                flatLayoutType\n                masterBedroomArea\n                showerArea\n                bathroomArea\n                hasGuestBathroom\n                entrancesNumber\n                canAddEntresol\n                studioKitchenArea\n\n                mortgageTag{\n                  id\n                  title\n                  description\n                }\n                windowViews {\n                    id\n                    name\n                }\n                isEuro\n                hasFreeLayout\n                canBeCombined\n                isApartment\n                inCompare\n              \tsmartFlat\n                smartBuilding\n                randomViews\n                promotions {\n                  edges {\n                    node {\n                        pk\n                        order\n                        name\n                        title\n                        subTitle\n                        tagName\n                        description\n                        shortDescription\n                        isPublished\n                        showWithPromo\n                        start\n                        end\n                        popupImage\n                        popupImageDisplay\n                        popupImagePreview\n\n                        isNyStyle\n\n                        projects {\n                            edges {\n                                node {\n                                    slug\n                                    title\n                                }\n                            }\n                        }\n                    }\n                  }\n                }\n            }\n        }\n    }\n}\n',
    'variables': {
        'orderBy': 'price_with_finish',
        'type': 'FlatType',
        'project': [],
        'phase': [],
        'building': [],
        'rooms': [],
        'finishTypes': [],
        'completion': [],
        'completionYear': [],
        'windowSides': [],
        'windowViews': [],
        'mortgages': [],
        'promotions': [],
        'first': 8,
        'after': 'YXJyYXljb25uZWN0aW9uOjE1',
    },
}

url = 'https://www.absrealty.ru/graphql/'

after_cursor = ""
flats = []
count = 1

while True:

    try:
        response = requests.post(url, cookies=cookies, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()

        edges = data.get('data', {}).get('allFlats', {}).get('edges', [])
        page_info = data.get('data', {}).get('allFlats', {}).get('pageInfo', {})
        node2 = data['data']['allFlats']['edges']
        for edge in edges:

            node = edge.get('node', {})
            date = datetime.date.today()
            developer = 'Абсолют'
            project = node.get('project', {}).get('name', '')

            if project == 'Заречье Парк':
                continue
            if project == 'Сколково':
                korpus = node.get('building', {}).get('number', '')
            else:
                korpus = f"Фаза {node.get('phase', '').get('number', '').replace('_', ' ')} корп. {node.get('building', {}).get('number', '')}"
            type = 'Квартира'

            finish_types = node.get('finishTypes', {})
            finish_edges = finish_types.get('edges', []) if finish_types else []
            finish_node = finish_edges[0].get('node', {}) if finish_edges else {}
            finish_type = finish_node.get('title', '')

            if finish_type == '':
                finish_type = 'Без отделки'
            elif finish_type == 'White-box':
                finish_type = 'Предчистовая'
            else:
                finish_type='С отделкой'

            room_count = node.get('rooms', '')
            area = node.get('area', '')
            old_price = round(float(node.get('originPrice', '')))
            price = round(float(node.get('price', '')))
            section = node.get('section', {}).get('number', '')
            floor = node.get('floor', {}).get('number', '')

            srok_sdachi_old = node.get('building', {}).get('completionDate', '')


            if price==old_price:
                price=None

            print(
                f"{count}, {project}, дата: {date}, отделка: {finish_type}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '',
                      '', '', '', korpus, '', '', '', srok_sdachi_old, '', '', type, finish_type, room_count, area, '',
                      old_price, '', '', price, section, floor, '']
            flats.append(result)
            count += 1

        if not page_info.get("hasNextPage", False):
            break
        after_cursor = page_info.get("endCursor", "")
        json_data['variables']['after'] = after_cursor
        time.sleep(0.05)
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
        break

save_flats_to_excel(flats, project, developer)
