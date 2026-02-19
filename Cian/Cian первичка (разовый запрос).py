import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import merge_and_clean, haversine
import re

decoration_dict = {'preFine': 'Предчистовая', 'fine': 'С отделкой', 'without': 'Без отделки',
                   'fineWithFurniture': 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']
rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
all_flats = []
all_multi_ids = []

def parse_cian_page(session, cookies, headers, json_data, decoration_dict):
    """
    Делает запрос к ЦИАН и возвращает:
    - список квартир (flats)
    - список multi_ids
    """

    url_api = "https://api.cian.ru/search-offers/v2/search-offers-desktop/"

    flats = []
    multi_ids = []

    # ========= Запрос =========
    for attempt in range(2):
        try:
            response = session.post(
                url_api,
                cookies=cookies,
                headers=headers,
                json=json_data
            )

            print("Status:", response.status_code)
            items = response.json()["data"]["offersSerialized"]
            break

        except Exception as e:
            print("Ошибка:", e)
            print("Пробуем ещё раз...")
            time.sleep(61)
            session = requests.Session()
    else:
        return [], []

    # ========= Обработка =========
    for i in items:

        # -------- Адрес --------
        address_data = {}
        counter = {}

        for item in i['geo']['address']:
            t = item["type"]
            name = item["fullName"]

            if t not in counter:
                counter[t] = 1
                key = t
            else:
                counter[t] += 1
                key = f"{t}{counter[t]}"

            address_data[key] = name

        keys = ["location", "location2", "okrug", "raion",
                "mikroraion", "metro", "street", "house"]

        location_data = {k: address_data.get(k, "") for k in keys}

        # -------- Остальные поля --------
        project = (
            i.get('geo', {})
             .get('jk', {})
             .get('displayName', '')
             .replace('ЖК ', '')
             .replace('«', '')
             .replace('»', '')
        )

        developer = i.get('geo', {}).get('jk', {}).get('developer', {}).get('name', "")

        korpus = i.get("geo", {}).get("jk", {}).get("house", {}).get("name", "")

        property_type = "Апартаменты" if i.get('isApartments') else "Квартира"

        price = i.get('bargainTerms', {}).get('priceRur', '')

        room_count = int(i["roomsCount"]) if i.get("roomsCount") else 0
        area = float(i["totalArea"]) if i.get("totalArea") else 0
        kitchen_area = float(i.get('kitchenArea', 0) or 0)
        living_area = float(i.get('livingArea', 0) or 0)

        floor = i.get("floorNumber", "")
        try:
            parking = i.get('building', {}).get('parking', {}).get('type', "")
        except:
            parking = ''

        balconies = int(i.get('balconiesCount', 0) or 0)
        loggias = int(i.get('loggiasCount', 0) or 0)
        balconies_total = balconies + loggias

        url = ""
        if i.get('fullUrl'):
            url = i['fullUrl'].rstrip('/').rpartition('/')[-3]

        # -------- Срок сдачи --------
        try:
            if i['building']['deadline']['isComplete']:
                srok_sdachi = "Дом сдан"
            else:
                srok_sdachi = ''
        except:
            srok_sdachi = ''

        # -------- Similar --------
        if i.get('similar'):
            match = re.search(r"multi_id=(\d+)", i['similar']['url'])
            if match:
                multi_ids.append(int(match.group(1)))

        date = datetime.date.today()

        print(
            f"{project}, {url}, дата: {date}, "
            f"комнат: {room_count}, площадь: {area}, цена: {price}"
        )

        flat_row = [
            project,
            developer,
            location_data["location"],
            location_data["location2"],
            location_data["okrug"],
            location_data["raion"],
            location_data["mikroraion"],
            location_data["metro"],
            location_data["street"],
            location_data["house"],
            korpus,
            srok_sdachi,
            property_type,
            room_count,
            area,
            kitchen_area,
            living_area,
            price,
            floor,
            balconies_total,
            parking,
            url
        ]

        flats.append(flat_row)

    return flats, multi_ids


with open("coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


# noinspection PyDictDuplicateKeys
cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrdel': '1744094487237',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
    '_gcl_au': '1.1.358370826.1745923014',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'newbuilding-search-frontend.consultant_cian_chat_onboarding_shown': '1',
    'cookie_agreement_accepted': '1',
    'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'map_preview_onboarding_counter': '1',
    '_ga': 'GA1.1.781516742.1746453483',
    'uxfb_usertype': 'searcher',
    'afUserId': '01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p',
    'AF_SYNC': '1746453484323',
    'uxs_uid': 'f7e2e9d0-29b8-11f0-9dbd-830a513100bc',
    'cian_ruid': '8098251',
    'F6_CIAN_SID': 'a9a48f63f662387d3c35ca6c6cb20740d7c86bb81f0c2b9767f62a64e8087c55',
    '_ym_isad': '2',
    'login_mro_popup': '1',
    'login_button_tooltip_key': '1',
    'countCallNowPopupShowed': '2%3A1746517081809',
    '_yasc': '8R9/wr218vWJMfK05fBo5KUPxW5J6smlJc3lsbzK7vnwV/2oYgxkWZAv+aGBmHZLlQc=',
    '_yasc': '7EJRUjZIw8befWCH7Q8prRioIBnENtPFjOfuiUI6eC63hgTnMLGHoaCZZVuwd2dtOK4=',
    'sopr_session': 'ee304049ec614f4a',
    '_ym_visorc': 'b',
    'session_region_id': '4827',
    'session_main_town_region_id': '4827',
    '_ga_3369S417EL': 'GS2.1.s1746519290$o4$g1$t1746519322$j28$l0$h0',
}
headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://krasnoyarsk.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://krasnoyarsk.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; _gcl_au=1.1.358370826.1745923014; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; map_preview_onboarding_counter=1; _ga=GA1.1.781516742.1746453483; uxfb_usertype=searcher; afUserId=01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p; AF_SYNC=1746453484323; uxs_uid=f7e2e9d0-29b8-11f0-9dbd-830a513100bc; cian_ruid=8098251; F6_CIAN_SID=a9a48f63f662387d3c35ca6c6cb20740d7c86bb81f0c2b9767f62a64e8087c55; _ym_isad=2; login_mro_popup=1; login_button_tooltip_key=1; countCallNowPopupShowed=2%3A1746517081809; _yasc=8R9/wr218vWJMfK05fBo5KUPxW5J6smlJc3lsbzK7vnwV/2oYgxkWZAv+aGBmHZLlQc=; _yasc=7EJRUjZIw8befWCH7Q8prRioIBnENtPFjOfuiUI6eC63hgTnMLGHoaCZZVuwd2dtOK4=; sopr_session=ee304049ec614f4a; _ym_visorc=b; session_region_id=4827; session_main_town_region_id=4827; _ga_3369S417EL=GS2.1.s1746519290$o4$g1$t1746519322$j28$l0$h0',
}


json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'polygon',
                    'name': 'Выделенная область',
                    'coordinates': [
                        [
                            '92.724158',
                            '56.0695531',
                        ],
                        [
                            '92.7021853',
                            '56.0699374',
                        ],
                        [
                            '92.6857058',
                            '56.0691688',
                        ],
                        [
                            '92.6733462',
                            '56.0622512',
                        ],
                        [
                            '92.6829592',
                            '56.0518748',
                        ],
                        [
                            '92.6973788',
                            '56.0457259',
                        ],
                        [
                            '92.7131716',
                            '56.0411142',
                        ],
                        [
                            '92.7282778',
                            '56.0457259',
                        ],
                        [
                            '92.7344577',
                            '56.0553336',
                        ],
                        [
                            '92.7269045',
                            '56.0641727',
                        ],
                        [
                            '92.7145449',
                            '56.0703217',
                        ],
                        [
                            '92.724158',
                            '56.0695531',
                        ],
                    ],
                },
            ],
        },
        'bbox': {
            'type': 'term',
            'value': [
                [
                    92.534729663,
                    56.0271337911,
                ],
                [
                    92.8643195068,
                    56.0962824402,
                ],
            ],
        },
        'decorations_list': {
            'type': 'terms',
            'value': [
                'fineWithFurniture',
            ],
        },
        'building_status': {
            'type': 'term',
            'value': 2,
        },
        'page': {
            'type': 'term',
            'value': 2,
        },
    },
}


json_data['jsonQuery']['room'] = {
        'type': 'terms',
        'value': [1, 2, 3, 4, 5, 6, 7, 9]
    }

json_data["jsonQuery"]["floor"] = {}
json_data["jsonQuery"]["floor"]["type"] = "range"
json_data["jsonQuery"]["floor"]["value"] = {}
json_data["jsonQuery"]["floor"]["value"]["gte"] = 1
json_data["jsonQuery"]["floor"]["value"]["lte"] = 99
json_data["jsonQuery"]["page"]["value"] = 1
json_data["jsonQuery"]["decorations_list"]["value"][0] = []

session = requests.Session()

current_date = datetime.date.today()

while True:

    flats = []

    for decoration in decoration_list:


        json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
        json_data["jsonQuery"]["page"]["value"] = 1

        response = session.post(
            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
            cookies=cookies,
            headers=headers,
            json=json_data
        )

        print(json_data)
        flats_count = response.json()['data']['aggregatedCount']
        print(f'Снимаем отделку: {decoration}')
        print(f'Количество отображаемых объявлений с отделкой {decoration}: {response.json()['data']['aggregatedCount']}')
        print(f'Количество объявлений с отделкой {decoration} всего: {response.json()['data']['offerCount']}')
        time.sleep(7)

        if response.json()['data']['aggregatedCount'] == 0:
            continue
        if response.json()['data']['aggregatedCount'] <= 1500:

            json_data['jsonQuery']['room'] = {
                'type': 'terms',
                'value': [1],
            }
            rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
            total_floor_list = [[1, 200]]
            print(f'Количество квартир меньше 1500')


        elif 1500 <= response.json()['data']['aggregatedCount'] <= 2500:

            json_data['jsonQuery']['room'] = {
                'type': 'terms',
                'value': [1],
            }
            rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
            total_floor_list = [[1, 100]]

        else:
            del json_data['jsonQuery']['room']
            rooms_ids = [[1, 2, 3, 4, 5, 6, 7, 9]]
            total_floor_list = [[1, 100]]


        for room_id in rooms_ids:

            json_data["jsonQuery"]["page"]["value"] = 1

            try:
                json_data["jsonQuery"]["room"]["value"][0] = room_id
            except:
                ''
            print(json_data["jsonQuery"]["room"]["value"])


            for f in total_floor_list:


                json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
                json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
                json_data["jsonQuery"]["page"]["value"] = 1
                print(f'Этажи квартир: {f}')

                name_counter = f'{room_id}-{f[0]}-{f[1]}-{decoration}'

                while True:

                    flats, multi_ids = parse_cian_page(
                        session=session,
                        cookies=cookies,
                        headers=headers,
                        json_data=json_data,
                        decoration_dict=decoration_dict
                    )

                    # если объявлений больше нет — выходим

                    sleep_time = random.uniform(1, 5)
                    time.sleep(sleep_time)

                    if not flats:
                        print("Объявления закончились")
                        break

                    all_flats.extend(flats)
                    all_multi_ids.extend(multi_ids)

                    # увеличиваем страницу
                    json_data["jsonQuery"]["page"]["value"] += 1

                    print("Переходим на страницу:",
                          json_data["jsonQuery"]["page"]["value"])


    print(multi_ids)
    if len(flats_total) > 1:

        df = pd.DataFrame(flats_total, columns=['Название проекта',
                                                'Девелопер',
                                                'Локация',
                                                'Локация2',
                                                          'Округ',
                                                          'Район',
                                                          'Микрорайон',
                                                          'Метро',
                                                          'Улица',
                                                          'Дом',
                                                'Корпус',
                                                'Срок сдачи',
                                                'Тип помещения',
                                                'Отделка',
                                                'Кол-во комнат',
                                                'Площадь, кв.м',
                                                'Площадь кухни, кв.м',
                                                'Жилая площадь, кв.м',
                                                'Цена лота, руб.',
                                                'Этаж',
                                                'Балконы/лоджии',
                                                'Паркинг',
                                                'Ссылка'
                                                ])

        current_date = datetime.date.today()

        # Базовый путь для сохранения
        base_path = r""

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


        def sanitize_filename(name):
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                name = name.replace(char, '_')
            return name


        project = sanitize_filename(project)
        filename = f"{project}__{current_date}_{name_counter}.xlsx"

        # Полный путь к файлу0
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        try:
            df.to_excel(file_path, index=False)
        except:
            filename = f"{project}_{current_date}_2.xlsx"
            file_path = os.path.join(folder_path, filename)
            df.to_excel(file_path, index=False)

# merge_and_clean(folder_path, f'Первичка_{city_in_work}_{current_date}.xlsx')
