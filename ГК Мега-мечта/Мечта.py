'''

Количество квартир на сайте и фактическое количество не совпадают

'''

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
    '__ddg1_': 'ZRyROBeQARGk2nXIvwj2',
    'tmr_lvid': 'c30c50b0541ba21ba401a8b744a17f78',
    'tmr_lvidTS': '1746432915678',
    '_ym_uid': '1746432917635770962',
    '_ym_d': '1746432917',
    '_ct': '2900000000101622311',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'RAuJDq': 'rSKsDjgoWbLBpIcNQiRFEUHJVzCkTv',
    '_ym_isad': '2',
    'cted': 'modId%3Dzuel8ymv%3Bya_client_id%3D1746432917635770962',
    'domain_sid': '7Ro2Ltfg-4qeRRN0H52AO%3A1748425455891',
    '_ct_site_id': '69926',
    '_ct_ids': 'zuel8ymv%3A69926%3A169426538',
    '_ct_session_id': '169426538',
    'cf7-amocrm-ga-cookie': '%7B%22utm_referrer%22%3A%22https%3A%5C%2F%5C%2Fmechta.su%5C%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dtw_mechta_all_projects_yandekh_search_msk_brand%257C116199075%26utm_content%3Dtype_search%257Cpl_none%257Cgrid_5516581353%257Cadid_16950368357%257Crt_53778046826%257Cptype_premium%257Cpos_1%257Cdevice_desktop%26utm_term%3D%25D0%25B6%25D0%25BA%2520%25D0%25BC%25D0%25B5%25D1%2587%25D1%2582%25D0%25B0%257Ckwid_53778046826%26calltouch_tm%3Dyd_c%253A116199075_gb%253A5516581353_ad%253A16950368357_ph%253A53778046826_st%253Asearch_pt%253Apremium_p%253A1_s%253Anone_dt%253Adesktop_reg%253A213_ret%253A53778046826_apt%253Anone%26mango%3D%257Cc%253A116199075%257Cg%253A5516581353%257Cb%253A16950368357%257Ck%253A53778046826%257Cst%253Asearch%257Ca%253Ano%257Cs%253Anone%257Ct%253Apremium%257Cp%253A1%257Cr%253A53778046826%257Creg%253A213%257Cnet%253A%257Byad%257D%26yclid%3D198271354710261759%22%2C%22utm_source%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_campaign%22%3A%22%22%2C%22utm_term%22%3A%22%22%2C%22utm_content%22%3A%22%22%7D',
    'tmr_detect': '0%7C1748434239176',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://mechta.su',
    'priority': 'u=1, i',
    'referer': 'https://mechta.su/catalog/?currentType=%5B%7B%22value%22%3A%22townhouse%22%2C%22label%22%3A%22%D0%A2%D0%B0%D1%83%D0%BD%D1%85%D0%B0%D1%83%D1%81%22%7D%2C%7B%22value%22%3A%22ready-townhouse%22%2C%22label%22%3A%22%D0%93%D0%BE%D1%82%D0%BE%D0%B2%D1%8B%D0%B9+%D1%82%D0%B0%D1%83%D0%BD%D1%85%D0%B0%D1%83%D1%81%22%7D%2C%7B%22value%22%3A%22flat%22%2C%22label%22%3A%22%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0%22%7D%2C%7B%22value%22%3A%22cottage%22%2C%22label%22%3A%22%D0%9A%D0%BE%D1%82%D1%82%D0%B5%D0%B4%D0%B6%22%7D%5D',
    'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '__ddg1_=ZRyROBeQARGk2nXIvwj2; tmr_lvid=c30c50b0541ba21ba401a8b744a17f78; tmr_lvidTS=1746432915678; _ym_uid=1746432917635770962; _ym_d=1746432917; _ct=2900000000101622311; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; RAuJDq=rSKsDjgoWbLBpIcNQiRFEUHJVzCkTv; _ym_isad=2; cted=modId%3Dzuel8ymv%3Bya_client_id%3D1746432917635770962; domain_sid=7Ro2Ltfg-4qeRRN0H52AO%3A1748425455891; _ct_site_id=69926; _ct_ids=zuel8ymv%3A69926%3A169426538; _ct_session_id=169426538; cf7-amocrm-ga-cookie=%7B%22utm_referrer%22%3A%22https%3A%5C%2F%5C%2Fmechta.su%5C%2F%3Futm_source%3Dyandex%26utm_medium%3Dcpc%26utm_campaign%3Dtw_mechta_all_projects_yandekh_search_msk_brand%257C116199075%26utm_content%3Dtype_search%257Cpl_none%257Cgrid_5516581353%257Cadid_16950368357%257Crt_53778046826%257Cptype_premium%257Cpos_1%257Cdevice_desktop%26utm_term%3D%25D0%25B6%25D0%25BA%2520%25D0%25BC%25D0%25B5%25D1%2587%25D1%2582%25D0%25B0%257Ckwid_53778046826%26calltouch_tm%3Dyd_c%253A116199075_gb%253A5516581353_ad%253A16950368357_ph%253A53778046826_st%253Asearch_pt%253Apremium_p%253A1_s%253Anone_dt%253Adesktop_reg%253A213_ret%253A53778046826_apt%253Anone%26mango%3D%257Cc%253A116199075%257Cg%253A5516581353%257Cb%253A16950368357%257Ck%253A53778046826%257Cst%253Asearch%257Ca%253Ano%257Cs%253Anone%257Ct%253Apremium%257Cp%253A1%257Cr%253A53778046826%257Creg%253A213%257Cnet%253A%257Byad%257D%26yclid%3D198271354710261759%22%2C%22utm_source%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_campaign%22%3A%22%22%2C%22utm_term%22%3A%22%22%2C%22utm_content%22%3A%22%22%7D; tmr_detect=0%7C1748434239176',
}

data = {
    'action': 'get_realty',
    'nextPostIndex': '0',
    'amount': '500',
    'housesParsed[]': [
        '161',
        '160',
        '159',
        '158',
        '157',
        '156',
        '154',
        '153',
    ],
    'filters[maxPrice]': '99900000',
    'filters[minPrice]': '100000',
    'filters[maxSquare]': '999.7',
    'filters[minSquare]': '1.14',
    'filters[currentType][]': [
        'townhouse',
        'ready-townhouse',
        'flat',
        'cottage',
    ],
    'filters[currentSort]': '',
    'filters[currentCheckInData]': '',
    'filters[currentFloors]': '',
    'filters[currentBuildings]': '',
    'filters[currentBuildingsMkd]': '',
    'filters[currentLayoutType]': '',
    'filters[currentWindowView]': '',
    'filters[currentFeatures]': '',
    'filters[currentAdvantages]': '',
    'onlyAmount': '',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://mechta.su/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)
    print(response.status_code)
    items = response.json()['realty']

    for i in items:

        if i['realty_type'] == 'Таунхаусы':

            for town in i['group_data']:

                url = ''
                developer = "ГК Мега-Мечта"
                project = 'Мечта'
                try:
                    korpus = i['building_number']
                except:
                    korpus = ''
                section = ''
                type = 'Таунхаусы'
                try:
                    if i['finishing'] == 'base':
                        finish_type = 'Без отделки'
                    elif i['finishing'] == 'semiclear':
                        finish_type = 'Предчистовая'
                    elif i['finishing'] == 'clear':
                        finish_type = 'С отделкой'
                except:
                    finish_type = ''

                try:
                    room_count = i['layout_rooms_amount']
                except:
                    room_count = ''
                try:
                    flat_number = i['title']
                except:
                    flat_number = ''
                try:
                    area = float(i['layout_square'])
                except:
                    area = ''
                if not area:
                    continue
                print(i['price_old'])
                if i['price_old'] != '':
                    old_price = int(i['price_old'])
                    price = int(i['price'])
                else:
                    old_price = int(i['price'])
                    price = ''

                try:
                    floor = i['floor']
                except:
                    floor = ''

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
                result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                          mck, distance_to_mck, time_to_mck, distance_to_bkl,
                          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                          konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                          price_per_metr_new, price, section, floor, flat_number]
                flats.append(result)

        else:

            url = ''
            developer = "ГК Мега-Мечта"
            project = 'Мечта'
            try:
                korpus = i['building_number']
            except:
                korpus = ''
            section = ''
            if i['realty_type'] == 'cottage':
                type = 'Коттеджи'
            elif i['realty_type'] == 'flat':
                type = 'Квартиры'
            elif i['realty_type'] == 'townhouse' or i['realty_type'] == 'ready-townhouse':
                type = 'Таунхаусы'
            else:
                type = i['realty_type']
            try:
                if i['finishing'] == 'base':
                    finish_type = 'Без отделки'
                elif i['finishing'] == 'semiclear':
                    finish_type = 'Предчистовая'
                elif i['finishing'] == 'clear':
                    finish_type = 'С отделкой'
            except:
                finish_type = ''


            try:
                room_count = i['layout_rooms_amount']
            except:
                room_count = ''
            try:
                flat_number = i['title']
            except:
                flat_number = ''
            try:
                area = float(i['layout_square'])
            except:
                area = ''
            if not area:
                continue
            try:
                if i['price_old'] != '':
                    old_price = int(i['price_old'])
                    price = int(i['price'])
                else:
                    old_price = int(i['price'])
                    price = ''
            except:
                old_price = int(i['price'])
                price = ''
            try:
                floor = i['floor']
            except:
                floor = ''


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

    break
    data['nextPostIndex'] = str(int(data['nextPostIndex']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

