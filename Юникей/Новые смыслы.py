"""

отдельно с отделкой и без, в 'params[finishing]'  Автоматически, менять ничего не надо

"""

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1742827436146654235',
    '_ym_d': '1773662608',
    'tmr_lvid': 'd30c05ee2b9f77dcbb919dc27de11d37',
    'tmr_lvidTS': '1773662608186',
    '_ym_visorc': 'w',
    'scbsid_old': '2746015342',
    'cted': 'modId%3Dli0xsjag%3Bya_client_id%3D1742827436146654235%7CmodId%3D46cqnlyv%3Bya_client_id%3D1742827436146654235%7CmodId%3Dlj2zo781%3Bya_client_id%3D1742827436146654235%7CmodId%3Ddg09qsgb%3Bya_client_id%3D1742827436146654235',
    '_ym_isad': '2',
    '_cmg_csstVKMSr': '1773662609',
    '_comagic_idVKMSr': '12394749031.16939302976.1773662608',
    'roistat_visit': '464135',
    'roistat_first_visit': '464135',
    'roistat_visit_cookie_expire': '1209600',
    '_ct': '3200000000164633209',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    'roistat_marker': 'seo_google_',
    'roistat_marker_old': 'seo_google_',
    '_ct_ids': 'lj2zo781%3A75002%3A244508497_dg09qsgb%3A56483%3A601098743_li0xsjag%3A70248%3A363964101_46cqnlyv%3A61236%3A391526870',
    'domain_sid': 'Y936jCzubaCmJVyUYEjnZ%3A1773662609608',
    'sma_session_id': '2638875113',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    '___dc': '01ad1c1c-383c-4e0d-99da-830bc986c09d',
    'smFpId_old_values': '%5B%22cd14d52d59b08c237e2004225d23c665%22%5D',
    'SCBnotShow': '-1',
    'SCBstart': '1773662610279',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'city': 'moscow',
    'cookiesApply': '1',
    '_ct_session_id': '601098743',
    '_ct_site_id': '56483',
    'call_s': '___46cqnlyv.1773664422.391526870.335118:959614|lj2zo781.1773664422.244508497.499586:1423891|li0xsjag.1773664422.363964101.427067:1195806|dg09qsgb.1773664422.601098743.299232:1491469|2___',
    'tmr_detect': '0%7C1773662624878',
    'roistat_call_tracking': '0',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': '%5B%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'SCBindexAct': '295',
    'sma_index_activity': '6895',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://unikey.space',
    'Referer': 'https://unikey.space/category/?city=3087&complex=2325&filter_finishDates=&area_range=&price_range=&finishing=&filter_building=&floor_range=&order=',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1742827436146654235; _ym_d=1773662608; tmr_lvid=d30c05ee2b9f77dcbb919dc27de11d37; tmr_lvidTS=1773662608186; _ym_visorc=w; scbsid_old=2746015342; cted=modId%3Dli0xsjag%3Bya_client_id%3D1742827436146654235%7CmodId%3D46cqnlyv%3Bya_client_id%3D1742827436146654235%7CmodId%3Dlj2zo781%3Bya_client_id%3D1742827436146654235%7CmodId%3Ddg09qsgb%3Bya_client_id%3D1742827436146654235; _ym_isad=2; _cmg_csstVKMSr=1773662609; _comagic_idVKMSr=12394749031.16939302976.1773662608; roistat_visit=464135; roistat_first_visit=464135; roistat_visit_cookie_expire=1209600; _ct=3200000000164633209; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; roistat_marker=seo_google_; roistat_marker_old=seo_google_; _ct_ids=lj2zo781%3A75002%3A244508497_dg09qsgb%3A56483%3A601098743_li0xsjag%3A70248%3A363964101_46cqnlyv%3A61236%3A391526870; domain_sid=Y936jCzubaCmJVyUYEjnZ%3A1773662609608; sma_session_id=2638875113; SCBfrom=https%3A%2F%2Fwww.google.com%2F; ___dc=01ad1c1c-383c-4e0d-99da-830bc986c09d; smFpId_old_values=%5B%22cd14d52d59b08c237e2004225d23c665%22%5D; SCBnotShow=-1; SCBstart=1773662610279; SCBporogAct=5000; sma_postview_ready=1; city=moscow; cookiesApply=1; _ct_session_id=601098743; _ct_site_id=56483; call_s=___46cqnlyv.1773664422.391526870.335118:959614|lj2zo781.1773664422.244508497.499586:1423891|li0xsjag.1773664422.363964101.427067:1195806|dg09qsgb.1773664422.601098743.299232:1491469|2___; tmr_detect=0%7C1773662624878; roistat_call_tracking=0; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=%5B%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; SCBindexAct=295; sma_index_activity=6895',
}

data = {
    'action': 'get_more_apartments',
    'page': '1',
    'params[city]': '3087',
    'params[complex]': '2325',
    'params[filter_finishDates]': '',
    'params[area_range]': '',
    'params[price_range]': '',
    'params[finishing]': '',
    'params[filter_building]': '',
    'params[floor_range]': '',
    'params[order]': '',
}

finishings = ['UniLoft', 'Без отделки', 'UniBox', 'UniDesign']
finishings_dict = {'UniLoft': 'С отделкой', 'Без отделки' : 'Без отделки', 'UniBox' : 'Предчистовая', 'UniDesign' : 'С отделкой'}

flats = []
flats_nums = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

for finish in finishings:
    print(flats_nums)
    data['params[finishing]'] = finish
    data['page'] = '1'


    while True:

        response = requests.post('https://unikey.space/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)
        print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')
        flats_soup = soup.find_all('li', class_="layouts-parameters__item")
        for flat in flats_soup:

            if int(flat.find('div', class_='layout-card__info-wrp').text.split()[9]) in flats_nums:
                print(f'Квартира {flat.find('div', class_='layout-card__info-wrp').text.split()[9]} уже в списке')
                continue





            # print(flat.text.strip().split())
            price_div = soup.find('div', class_='layout-card__price')

            url = ''
            developer = "Юникей"
            project = 'Новые смыслы'
            korpus = flat.find('div', class_='layout-card__info-wrp').text.split()[4]
            type = 'Квартира'
            finish_type = finishings_dict.get(finish, finish)
            if flat.find('span', class_='layout-card__count').text.split()[0] == 'Студия':
                room_count = 0
            else:
                room_count = extract_digits_or_original(flat.find('span', class_='layout-card__count').text.split()[0])
            try:
                area = float(flat.find('div', class_='layout-card__info-wrp').text.split()[11])
            except:
                area = ''
            try:
                old_price = extract_digits_or_original(price_div.find('span', class_='layout-card__title').get_text(strip=True))
                price = extract_digits_or_original(price_div.find('span', class_='layout-card__count').get_text(
                    strip=True))
            except:
                old_price = extract_digits_or_original(price_div.find('span', class_='layout-card__count').get_text(
                strip=True))
                price = ''

            section = ''
            try:
                floor = int(flat.find('div', class_='layout-card__info-wrp').text.split()[6].split('/')[0])
            except:
                floor = ''
            flat_number = int(flat.find('div', class_='layout-card__info-wrp').text.split()[9])

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



            print(f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)
            flats_nums.append(flat_number)

        if not flats_soup:
            break
        data['page'] = str(int(data['page']) + 1)
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

