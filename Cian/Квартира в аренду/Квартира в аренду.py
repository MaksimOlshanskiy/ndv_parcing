import requests
import datetime
import time
import pandas as pd
import os
import random
import asyncio
import json
from telegram import Bot


def parse():
    proxies = {
        "http": "http://STm87nUFS6:6StepJYs2y@185.42.27.210:10270",
    "https": "http://STm87nUFS6:6StepJYs2y@185.42.27.210:10270"
    }

    type_of_lot = 'Вторичка, аренда'

    cookies = {
        '_ym_uid': '174161324651361127',
        'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
        'adrdel': '1744094487237',
        'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
        'ma_id': '6225667261741613246584',
        '__ai_fp_uuid': '245d903c22bdc927%3A15',
        '_gcl_au': '1.1.9818463.1769411842',
        '_ym_d': '1773209373',
        '_ga': 'GA1.1.1538482319.1774343544',
        'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
        'tmr_lvidTS': '1741613242260',
        'uxs_uid': '92604860-28f8-11f1-a98a-bba19a4d4807',
        'uxfb_usertype': 'searcher',
        'cookie_agreement_accepted': '1',
        'newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown': '1',
        'map_preview_onboarding_counter': '3',
        'login_button_tooltip_key': '1',
        'frontend-serp.header_builder_chat_onboarding_shown': '1',
        'newbuilding-search-frontend.builder_chat_onboarding_shown': '1',
        'frontend-serp.chatTooltipAnimationShown': '1',
        'newbuilding-search-frontend.chatTooltipAnimationShown': '1',
        'frontend-serp.offer_chat_onboarding_shown': '1',
        'frontend-offer-card.builder_chat_onboarding_shown': '1',
        'frontend-offer-card.newbuilding_broker_onboarding_shown': '1',
        'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775',
        '_CIAN_GK': '8421b1d7-727f-42ac-9f77-a0ed1f26ad1b',
        'newbuilding-search-frontend.chatAnimationShownCount': '122',
        'countCallNowPopupShowed': '2%3A1776238384809',
        'sopr_utm': '%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D',
        'newbuilding-search-frontend.chatAnimationCounter': '124',
        'newbuilding-search-frontend.chatAnimationPrevPath': '%2Fnewobjects%2Flist%2F%3Fdeal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D4973',
        'frontend-serp.chatAnimationPrevPath': '%2Fkupit-kvartiru-novostroyki-kaliningradskaya-oblast-zelenogradskiy-01413799%2F',
        'frontend-serp.chatAnimationShownCount': '56',
        'frontend-serp.chatAnimationCounter': '57',
        '_ga_L109H0KCP9': 'GS2.1.s1776411488$o2$g0$t1776411488$j60$l0$h0',
        'forever_region_id': '1',
        'forever_region_name': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
        'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1776666295512',
        'DMIR_AUTH': '%2FrUCwMR3eKCUJveYGJ%2FAWFJ7BemL3s84TuWq1AajdkyfBDpCDgiLD7fs5oDcXbASOIF0reduFENPnVWxFdWySOn1WvLDTPcIhyO3tpMQMVfh9lQ3dhklNmx8ouVB%2BjA5YZiWPiKvshMR%2BlAALSarPMoRSSxB4nl5YJWsyAwO3jY%3D',
        'cian_ruid': '8098251',
        'transport-accessibility_onboarding_counter': '3',
        'tmr_detect': '0%7C1776687095287',
        '_yasc': 'vy0ZMKbMCEV5IcmF5KX5hmaKeqdriYyiYFZr5VLrAPNtXVgIN741vAqZ9nwOQRCen4z+',
        '_yasc': 'Fbg1H4rCmC7w5eKfhX8Jx8EtvPPsxJLF+3OGFVPSdzq/O6JHJVyWSsAR8bFBHcRG08If',
        'sopr_session': '27eb2e37d2f446d6',
        'cookieUserID': '8098251',
        '_ym_isad': '2',
        '_ym_visorc': 'b',
        'session_region_id': '1',
        'session_main_town_region_id': '1',
        '_ga_3369S417EL': 'GS2.1.s1776752438$o67$g1$t1776752558$j59$l0$h0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
        'content-type': 'application/json',
        'origin': 'https://www.cian.ru',
        'priority': 'u=1, i',
        'referer': 'https://www.cian.ru/',
        'sec-ch-ua': '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
        # 'cookie': '_ym_uid=174161324651361127; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; ma_id=6225667261741613246584; __ai_fp_uuid=245d903c22bdc927%3A15; _gcl_au=1.1.9818463.1769411842; _ym_d=1773209373; _ga=GA1.1.1538482319.1774343544; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; uxs_uid=92604860-28f8-11f1-a98a-bba19a4d4807; uxfb_usertype=searcher; cookie_agreement_accepted=1; newbuilding-card-desktop-fichering-frontend.builder_chat_onboarding_shown=1; map_preview_onboarding_counter=3; login_button_tooltip_key=1; frontend-serp.header_builder_chat_onboarding_shown=1; newbuilding-search-frontend.builder_chat_onboarding_shown=1; frontend-serp.chatTooltipAnimationShown=1; newbuilding-search-frontend.chatTooltipAnimationShown=1; frontend-serp.offer_chat_onboarding_shown=1; frontend-offer-card.builder_chat_onboarding_shown=1; frontend-offer-card.newbuilding_broker_onboarding_shown=1; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_content=kw:53165000434|ad:16524730146|grp:5496132987|drf:no|dev:desktop|p:premium|n:2|reg:213|s:none&utm_term=---autotargeting&utm_campaign=b2c_nov_mskmo_perf_mix_search_tgo_offers_k50_upperlevel_arwm_111586059&etext=2202.kYaiMM0XDsCfDTGcqPixewmDup7PIJTWa3k1vYESIEN5ZW9pdW1neGNzaHJtdHlw.8b57db14aa5a79ce43ab908f71b58548810a405f&yclid=4681174442620747775; _CIAN_GK=8421b1d7-727f-42ac-9f77-a0ed1f26ad1b; newbuilding-search-frontend.chatAnimationShownCount=122; countCallNowPopupShowed=2%3A1776238384809; sopr_utm=%7B%22utm_source%22%3A+%22web.telegram.org%22%2C+%22utm_medium%22%3A+%22referral%22%7D; newbuilding-search-frontend.chatAnimationCounter=124; newbuilding-search-frontend.chatAnimationPrevPath=%2Fnewobjects%2Flist%2F%3Fdeal_type%3Dsale%26engine_version%3D2%26offer_type%3Dnewobject%26region%3D4973; frontend-serp.chatAnimationPrevPath=%2Fkupit-kvartiru-novostroyki-kaliningradskaya-oblast-zelenogradskiy-01413799%2F; frontend-serp.chatAnimationShownCount=56; frontend-serp.chatAnimationCounter=57; _ga_L109H0KCP9=GS2.1.s1776411488$o2$g0$t1776411488$j60$l0$h0; forever_region_id=1; forever_region_name=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1776666295512; DMIR_AUTH=%2FrUCwMR3eKCUJveYGJ%2FAWFJ7BemL3s84TuWq1AajdkyfBDpCDgiLD7fs5oDcXbASOIF0reduFENPnVWxFdWySOn1WvLDTPcIhyO3tpMQMVfh9lQ3dhklNmx8ouVB%2BjA5YZiWPiKvshMR%2BlAALSarPMoRSSxB4nl5YJWsyAwO3jY%3D; cian_ruid=8098251; transport-accessibility_onboarding_counter=3; tmr_detect=0%7C1776687095287; _yasc=vy0ZMKbMCEV5IcmF5KX5hmaKeqdriYyiYFZr5VLrAPNtXVgIN741vAqZ9nwOQRCen4z+; _yasc=Fbg1H4rCmC7w5eKfhX8Jx8EtvPPsxJLF+3OGFVPSdzq/O6JHJVyWSsAR8bFBHcRG08If; sopr_session=27eb2e37d2f446d6; cookieUserID=8098251; _ym_isad=2; _ym_visorc=b; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS2.1.s1776752438$o67$g1$t1776752558$j59$l0$h0',
    }

    json_data = {
        'jsonQuery': {
            '_type': 'flatrent',
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'sort': {
                'type': 'term',
                'value': 'creation_date_desc',
            },
            'region': {
                'type': 'terms',
                'value': [
                    1,
                ],
            },
            'price': {
                'type': 'range',
                'value': {
                    'lte': 130000,
                },
            },
            'geo': {
                'type': 'geo',
                'value': [
                    {
                        'id': 28,
                        'type': 'district',
                    },
                    {
                        'id': 37,
                        'type': 'district',
                    },
                    {
                        'id': 32,
                        'type': 'district',
                    },
                ],
            },
            'for_day': {
                'type': 'term',
                'value': '!1',
            },
            'total_area': {
                'type': 'range',
                'value': {
                    'gte': 42,
                },
            },
            'repair': {
                'type': 'terms',
                'value': [
                    3,
                    4,
                ],
            },
            'room': {
                'type': 'terms',
                'value': [
                    2,
                    3,
                    4,
                ],
            },
            'page': {
                'type': 'term',
                'value': 1,
            },
        },
        '_liquiditySource': 'web_serp',
    }




    flats = []
    counter = 1
    total_count = 1


    def extract_digits_or_original(s):
        digits = ''.join([char for char in s if char.isdigit()])
        return int(digits) if digits else s

    repair_ids = [3, 4]
    repair_ids_dict = {1: 'Без отделки', 2: 'Косметический', 3: 'Евроремонт', 4: 'Дизайнерский'}
    rooms_ids = [1,2,3,4,5,6,7,9]

    session = requests.Session()

    response = session.post(    # Первичный запрос для определения количества лотов
                            'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                            cookies=cookies,
                            headers=headers,
                            json=json_data,
                            proxies=proxies
                        )

    items_count = response.json()['data']["aggregatedCount"]
    print(f'В городе {items_count} лотов')

    current_date = datetime.datetime.now()

    name_counter = f'Аренда для Ольшанских'
    flats = []

    while True:

        if counter > 1:
            sleep_time = random.uniform(6, 9)
            time.sleep(sleep_time)
        try:
            response = session.post(
                'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                cookies=cookies,
                headers=headers,
                json=json_data,
                proxies=proxies
            )

            print(response.status_code)

            items = response.json()["data"]["offersSerialized"]
        except:
            print("Произошла ошибка, пробуем ещё раз")
            print(response.status_code)
            time.sleep(61)
            session = requests.Session()
            response = session.post(
                'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                cookies=cookies,
                headers=headers,
                json=json_data,
                proxies=proxies
            )
            print(response.status_code)
            items = response.json()["data"]["offersSerialized"]

        for i in items:
            data = i['geo']['address']
            result = {}
            counterr = {}

            for item in data:
                t = item["type"]
                name = item["fullName"]

                # Первый раз — без номера
                if t not in counterr:
                    counterr[t] = 1
                    key = t
                else:
                    counterr[t] += 1
                    key = f"{t}{counterr[t]}"

                result[key] = name

            # список нужных переменных
            keys = ["location", "location2", "location3", "okrug", "raion", "mikroraion", "metro", "street",
                    "house"]

            # создаём переменные
            for key in keys:
                globals()[key] = result.get(key, "")

            try:
                adress = i['geo']['userInput']
            except:
                adress = ''
            try:
                jk = i['geo']['jk']['displayName']
            except:
                jk = ''
            try:
                if not i['roomsCount'] and i['flatType'] == 'studio':
                    rooms_count = 0
                else:
                    rooms_count = i['roomsCount']
            except:
                rooms_count = ''
            try:
                area = float(i['totalArea'])
            except:
                area = ''
            try:
                price = int(i['bargainTerms']['priceRur'])
            except:
                price = i['bargainTerms']['priceRur']
            try:
                finish_type = repair_ids_dict.get(repair_id)
            except:
                finish_type = 'Неизвестно'
            try:
                description = i['description']
            except:
                description = ''
            try:
                if i['fromDeveloper'] == True or i['user']['isBuilder'] == True:
                    property_from = "От застройщика"
                elif i['user']['isAgent'] is True:
                    property_from = "От агента"
                elif i['isByHomeowner'] is True:
                    property_from = 'От собственника'
                else:
                    property_from = ''
            except:
                property_from = ''
            try:
                url = i['fullUrl'].rstrip('/').rpartition('/')[-3]
            except:
                url = ''

            try:
                added = i['added']
            except:
                added = ''
            try:
                balconiesCount = i['balconiesCount']
            except:
                balconiesCount = ''
            try:
                bedroomsCount = i['bedroomsCount']
            except:
                bedroomsCount = ''
            try:
                buildYear = i['building']['buildYear']
            except:
                buildYear = ''
            try:
                cargoLiftsCount = i['building']['cargoLiftsCount']
            except:
                cargoLiftsCount = ''
            try:
                passengerLiftsCount = i['building']['passengerLiftsCount']
            except:
                passengerLiftsCount = ''
            try:
                floorsCount = i['building']['floorsCount']
            except:
                floorsCount = ''
            try:
                materialType = i['building']['materialType']
            except:
                materialType = ''
            try:
                parking = i['building']['parking']['type']
            except:
                parking = ''
            try:
                creationDate = i['creationDate']
            except:
                creationDate = ''
            try:
                floorNumber = i['floorNumber']
            except:
                floorNumber = ''
            try:
                coordinates_lat = i['geo']['coordinates']['lat']
            except:
                coordinates_lat = ''
            try:
                coordinates_lng = i['geo']['coordinates']['lng']
            except:
                coordinates_lng = ''
            try:
                highways_nearest = i['geo']['highways'][0]['name']
            except:
                highways_nearest = ''
            try:
                highway_distance = i['geo']['highways'][0]['distance']
            except:
                highway_distance = ''
            try:
                railways_nearest = i['geo']['railways'][0]['name']
            except:
                railways_nearest = ''
            try:
                railways_id = i['geo']['railways'][0]['id']
            except:
                railways_id = ''
            try:
                railways_nearest_distance = i['geo']['railways'][0]['distance']
            except:
                railways_nearest_distance = ''
            try:
                railways_nearest_time = i['geo']['railways'][0]['time']
            except:
                railways_nearest_time = ''
            try:
                railways_nearest_travelType = i['geo']['railways'][0]['travelType']
            except:
                railways_nearest_travelType = ''
            try:
                jk = i['geo']['jk']['displayName']
            except:
                jk = ''
            try:
                underground_nearest = i['geo']['railways'][0]['name']
            except:
                underground_nearest = ''
            try:
                underground_nearest_time = i['geo']['railways'][0]['time']
            except:
                underground_nearest_time = ''
            try:
                hasFurniture = i['hasFurniture']
            except:
                hasFurniture = ''
            try:
                kitchenArea = i['kitchenArea']
            except:
                kitchenArea = ''
            try:
                livingArea = i['livingArea']
            except:
                livingArea = ''
            try:
                loggiasCount = i['loggiasCount']
            except:
                loggiasCount = ''

            print(
                f"{current_date} | Город {location}, {location2}, {okrug}, {raion}, {metro}, {street}, {house}, {url}, Комнаты: {rooms_count}, площадь: {area}, цена: {price}, ремонт {finish_type}")
            result = url
            flats.append(result)

        break
    return flats



TOKEN = "8782445246:AAH5pIEj_tn2DoEiIMUh2jKm9vpgRA8z2ak"
CHAT_ID = "372911529"

bot = Bot(token=TOKEN)

# 📦 загрузка старых URL
def load_urls(path=r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian\Квартира в аренду\urls.json'):
    try:
        with open(path, "r") as f:
            return set(json.load(f))
    except:
        return set()


# 💾 сохранение URL
def save_urls(urls, path=r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian\Квартира в аренду\urls.json'):
    with open(path, "w") as f:
        json.dump(list(urls), f, indent=2)


# 📩 отправка в Telegram
async def send_flats(flats):
    text = "🏠 Новые квартиры:\n\n"

    for url in flats:
        text += f"🔗 {url}\n"

    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )

# 🚀 основной цикл
async def main():
    old_urls = load_urls()

    while True:
        flats = set(parse())

        new_flats = flats - old_urls

        if new_flats:
            await send_flats(new_flats)

            # 💾 ОБЯЗАТЕЛЬНО сохраняем
            old_urls |= new_flats
            save_urls(old_urls)

        await asyncio.sleep(300)


asyncio.run(main())









