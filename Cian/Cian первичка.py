import requests
import datetime
import time
import pandas as pd
import os
import random
import json
from functions import merge_and_clean, haversine

decoration_dict = {'preFine': 'Предчистовая', 'fine': 'С отделкой', 'without': 'Без отделки',
                   'fineWithFurniture': 'С отделкой и доп опциями'}
decoration_list = ['preFine', 'fine', 'without', 'fineWithFurniture']

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
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'region': {
            'type': 'terms',
            'value': [
                4820,
            ],
        },
    },
    'uri': '/newobjects/list?deal_type=sale&engine_version=2&from_developer=1&offer_type=newobject&region=2&p=4',
    'subdomain': 'spb',
    'offset': 0,
    'count': 25,
    'userCanUseHiddenBase': False,
}

cities_dict = {
    'Москва': 1,
    'Санкт-Петербург': 2,
    'Новосибирск': 4897,
    'Екатеринбург': 4743,
    'Казань': 4777,
    'Красноярск': 4827,
    'Нижний Новгород': 4885,
    'Челябинск': 5048,
    'Уфа': 176245,
    'Краснодар': 4820,
    'Самара': 4966,
    'Ростов-на-Дону': 4959,
    'Омск': 4914,
    'Воронеж': 4713,
    'Пермь': 4927,
    'Волгоград': 4704
}

print("Список доступных регионов:")
for city, city_id in cities_dict.items():
    print(f"{city}: {city_id}")

user_input = input("\nВведите ID нужного региона или введите свой: ")

try:
    user_id = int(user_input)
    if user_id in cities_dict.values():
        selected_city = [city for city, cid in cities_dict.items() if cid == user_id][0]
        print(f"\nВы выбрали город: {selected_city}")
    else:
        print("\nГород не в списке")
except ValueError:
    print("\nОшибка: введите числовой ID.")

coords = city_centers.get(user_input)

# noinspection PyTypeChecker
json_data['jsonQuery']['region']['value'] = [user_input]

ids = []
json_data['offset'] = 0

while True:

    response = requests.post(
        'https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    items = response.json()['newbuildings']

    for i in items:
        if i['fromDeveloperPropsCount'] < 1:
            continue
        id = i['id']
        ids.append(id)
    if not items:
        break
    json_data['offset'] += 25

city_in_work = response.json()['breadcrumbs'][0]['title']
print(city_in_work)
print(response.json()['breadcrumbs'][1]['title'])
print(ids)
print(f'Количество ЖК: {len(ids)}'      )

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
                    'type': 'newobject',
                    'id': 4013017,
                },
            ],
        },
        'decorations_list': {
            'type': 'terms',
            'value': [
                'preFine',
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 99,
            },
        },
        'room': {
            'type': 'terms',
            'value': [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                9,
            ],
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
        },
    },
}

current_date = datetime.date.today()
ids = [3961301, 50202, 3718327, 5155847, 3752407, 4664801, 3783950, 747719, 92957, 3884807, 4362585, 3361069, 4095940, 92316, 4815246, 3848284, 3019502, 3877206, 5432617, 1258683, 5238228, 3260347, 3735596, 3952382, 7984, 8172, 3910227, 4752770, 900192, 4800628, 4130711, 2038797, 4441515, 5283548, 43956, 4735589, 4927010, 4019247, 219525]
for y in ids:

    flats = []
    session = requests.Session()
    flats_total = []

    if y in []:
        continue

    print(f"Новый ЖК, {y}, {ids.index(y) + 1} из {len(ids)}")

    json_data['jsonQuery']['room'] = {
        'type': 'terms',
        'value': [1, 2, 3, 4, 5, 6, 7, 9]
    }

    json_data["jsonQuery"]["floor"]["value"]["gte"] = 1
    json_data["jsonQuery"]["floor"]["value"]["lte"] = 99
    json_data["jsonQuery"]["geo"]["value"][0]["id"] = y
    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["decorations_list"]["value"][0] = []

    response = session.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        cookies=cookies,
        headers=headers,
        json=json_data
    )
    flats_count = response.json()['data']['aggregatedCount']
    print(f'Количество квартир в проекте: {flats_count}')
    time.sleep(7)

    if flats_count > 2500:

        json_data['jsonQuery']['room'] = {
            'type': 'terms',
            'value': [1],
        }
        rooms_ids = [1, 2, 3, 4, 5, 6, 7, 9]
        total_floor_list = [[1, 3], [4, 7], [8, 12], [13, 17], [18, 23], [24, 30], [31, 40], [41, 200]]

    elif 1500 <= flats_count <= 2500:

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

    print(json_data)

    for decoration in decoration_list:

        json_data["jsonQuery"]["decorations_list"]["value"][0] = decoration
        json_data["jsonQuery"]["page"]["value"] = 1

        for room_id in rooms_ids:

            json_data["jsonQuery"]["page"]["value"] = 1

            try:
                json_data["jsonQuery"]["room"]["value"][0] = room_id
            except:
                ''
            counter = 1
            total_count = 1

            for f in total_floor_list:


                json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
                json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
                json_data["jsonQuery"]["page"]["value"] = 1
                print(f'Этажи квартир: {f}')

                name_counter = f'{room_id}-{f[0]}-{f[1]}-{decoration}'

                while True:

                    print(f"Число комнат: {room_id}")
                    if counter > 1:
                        sleep_time = random.uniform(7, 9)
                        time.sleep(sleep_time)
                    try:
                        response = session.post(
                            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                            cookies=cookies,
                            headers=headers,
                            json=json_data
                        )

                        print(response.status_code)

                        items = response.json()["data"]["offersSerialized"]
                    except:
                        print("Произошла ошибка, пробуем ещё раз")
                        time.sleep(61)
                        session = requests.Session()
                        response = session.post(
                            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                            cookies=cookies,
                            headers=headers,
                            json=json_data
                        )
                        print(response.status_code)
                        items = response.json()["data"]["offersSerialized"]

                    for i in items:
                        try:
                            geo1 = i['geo']['address'][0]['fullName']
                        except:
                            geo1 = ''
                        try:
                            geo2 = i['geo']['address'][1]['fullName']
                        except:
                            geo2 = ''
                        try:
                            geo3 = i['geo']['address'][2]['fullName']
                        except:
                            geo3 = ''
                        try:
                            geo4 = i['geo']['address'][3]['fullName']
                        except:
                            geo4 = ''
                        try:
                            if i['building']['deadline']['isComplete']:
                                srok_sdachi = "Дом сдан"
                            elif i['building']['deadline']['quarterEnd'] is None and i['building']['deadline'][
                                'year'] is None:
                                srok_sdachi = ''
                            else:
                                srok_sdachi = f"Cдача ГК: {i['newbuilding']['house']['finishDate']['quarter']} квартал, {i['newbuilding']['house']['finishDate']['year']} года".replace(
                                    'None', '')
                        except:
                            srok_sdachi = ''
                        try:
                            url = i['fullUrl']
                        except:
                            url = ''

                        try:
                            if i['isApartments']:
                                type = "Апартаменты"
                            else:
                                type = "Квартира"
                        except:
                            type = ''

                        try:
                            price = i['bargainTerms']['priceRur']
                        except:
                            price = ''
                        try:
                            project = i['geo']['jk']['displayName'].replace('ЖК ', '').replace('«', '').replace('»', '')
                        except:
                            project = ''
                        # try:
                        #   if i['decoration'] == "fine":
                        #      finish_type = "С отделкой"
                        #    elif i['decoration'] == "without" or i['decoration'] == "rough":
                        #       finish_type = "Без отделки"
                        #   else:
                        #      finish_type = i['decoration']
                        # except:
                        #   finish_type = ''
                        # if not finish_type:
                        #    finish_type = classify_renovation(i['description'])
                        try:
                            finish_type = decoration_dict.get(decoration)
                        except:
                            finish_type = 'Не определён'

                        try:
                            adress = i['geo']['userInput']
                        except:
                            adress = ""

                        try:
                            korpus = i["geo"]["jk"]["house"]["name"]
                        except:
                            korpus = ''

                        try:
                            developer = i['geo']['jk']['developer']['name']
                        except:
                            developer = ""

                        try:
                            if i["roomsCount"] is None:
                                room_count = 0
                            else:
                                room_count = int(i["roomsCount"])
                        except:
                            room_count = ''
                        try:
                            area = float(i["totalArea"])
                        except:
                            area = ''

                        date = datetime.date.today()

                        try:
                            floor = i["floorNumber"]
                        except:
                            floor = ''
                        try:
                            added = i['added']
                        except:
                            added = ''
                        try:
                            kitchenArea = float(i['kitchenArea'])
                        except:
                            kitchenArea = 0
                        try:
                            livingArea = float(i['livingArea'])
                        except:
                            livingArea = 0
                        try:
                            parking = i['building']['parking']['type']
                        except:
                            parking = ''
                        try:
                            balconiesCount = int(i['balconiesCount'])
                        except:
                            balconiesCount = 0
                        try:
                            loggiasCount = int(i['loggiasCount'])
                        except:
                            loggiasCount = 0
                        balconies_and_loggias_count = balconiesCount + loggiasCount
                        try:

                            lat_jk = i['geo']['coordinates']['lat']
                            lon_jk = i['geo']['coordinates']['lng']
                            lat_center = coords["lat_center"]
                            lon_center = coords["lon_center"]
                            distance = round(haversine(lat_jk, lon_jk, lat_center, lon_center), 2)

                        except:
                            distance = ''

                        print(
                            f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                        result = [project, developer, geo1, geo2, geo3, geo4, korpus, distance, srok_sdachi, type,
                                  finish_type, room_count, area, kitchenArea, livingArea, price, floor,
                                  balconies_and_loggias_count, parking, url]
                        flats.append(result)
                        flats_total.append(result)

                    if not items:
                        break
                    json_data["jsonQuery"]["page"]["value"] += 1
                    print(len(flats))
                    print("-----------------------------------------------------------------------------")
                    total_count = response.json()["data"]["offerCount"]
                    downloaded = len(flats)
                    print(
                        f'ID ЖК: {y}, {ids.index(y) + 1} из {len(ids)}. Загружено {downloaded} предложений из {total_count}')
                    counter += 1

    if len(flats_total) > 1:

        df = pd.DataFrame(flats_total, columns=['Название проекта',
                                                'Девелопер',
                                                'Гео1',
                                                'Гео2',
                                                'Гео3',
                                                'Гео4',
                                                'Корпус',
                                                'Расстояние до центра, км',
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

merge_and_clean(folder_path, f'Первичка_{city_in_work}_{current_date}.xlsx')
