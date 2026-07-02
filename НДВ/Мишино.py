import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all
import requests

cookies = {
    '_ym_uid': '1776591913437946397',
    '_ym_d': '1776591913',
    'device_view': 'full',
    'tmr_lvid': 'c18eca6cb3da30e034ac685e519f1725',
    'tmr_lvidTS': '1776591911319',
    '_dmp_cookie_deny': '1',
    '_ct': '700000001920935760',
    '_ct_client_global_id': 'fbe0ef66-3f93-5e30-a689-c3153a19a53a',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'domain_sid': 'MoUm9hd-oxZ5HqjonnMpA%3A1782897972957',
    'origin_referer': 'https%3A%2F%2Fwww.ndv.ru%2F',
    'tmr_detect': '0%7C1782898496093',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.ndv.ru/novostrojki/zhk/kosmos/placements/2',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-page-path': '/novostrojki/zhk/kosmos/placements/2',
    'x-route-tags': 'slug:kosmos,page:2',
    # 'cookie': '_ym_uid=1776591913437946397; _ym_d=1776591913; device_view=full; tmr_lvid=c18eca6cb3da30e034ac685e519f1725; tmr_lvidTS=1776591911319; _dmp_cookie_deny=1; _ct=700000001920935760; _ct_client_global_id=fbe0ef66-3f93-5e30-a689-c3153a19a53a; _ym_isad=2; _ym_visorc=w; domain_sid=MoUm9hd-oxZ5HqjonnMpA%3A1782897972957; origin_referer=https%3A%2F%2Fwww.ndv.ru%2F; tmr_detect=0%7C1782898496093',
}

params = {
    'filter[complexSlug][condition]': 'eq',
    'filter[complexSlug][property]': 'complexSlug',
    'filter[complexSlug][value]': 'mishino-2',
    'filter[flatRoomsNumber][condition]': 'gte',
    'filter[flatRoomsNumber][property]': 'flatRoomsNumber',
    'filter[flatRoomsNumber][value][0]': '0',
    'filter[flatMinPriceFrom][condition]': 'gte',
    'filter[flatMinPriceFrom][property]': 'flatMinPriceFrom',
    'filter[flatMinPriceFrom][value]': '6756008',
    'filter[flatMinPriceTo][condition]': 'lte',
    'filter[flatMinPriceTo][property]': 'flatMinPriceTo',
    'filter[flatMinPriceTo][value]': '19996008',
    'sort[0][property]': 'objectMinPrice',
    'sort[0][direction]': 'ASC',
    'limit': '12',
    'offset': '0',
}

flats = []
count = 0


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:
    response = requests.get(
        'https://www.ndv.ru/backend-api/realty/new-buildings-flats',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)

    if response.status_code == 200:
        item = response.json()

        items = item["data"]['items']

        for i in items:
            count += 1
            date = datetime.date.today()
            project = 'Мишино-2'
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
            developer = "СЗ Ю-ИНВЕСТ"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["housingNumber"]
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = i['commissionDate']
            stadia = ''
            dogovor = ''
            type_ = i['type'].replace('flat', "Квартира")

            room_count = i['objectRoomsNumber']
            area = i["area"].replace('м²', "")
            price_per_metr = ''

            discount = ''
            price_per_metr_new = ''

            section = ''
            floor = i["objectFloor"]
            flat_number = ''
            if i['objectCostWithFinishing'] != 0 or i['objectCostWithFinishingPromo'] != 0:
                finish_type = 'С отделкой'
                old_price = i["objectCostWithFinishing"]
                price = i["objectCostWithFinishingPromo"]
            else:
                finish_type = 'Без отделки'
                old_price = i["objectMinCalculatedPrice"]
                price = i["objectMinPrice"]

            if not price:
                price = old_price

            print(
                f"{count} | {project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type_, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        # Проверяем, есть ли следующая страница
        params['offset'] = str(int(params['offset']) + 12)
        if not items:
            break
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.3)

save_flats_to_excel(flats, 'all', developer)
