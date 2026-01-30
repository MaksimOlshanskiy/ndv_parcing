'''

Подстановка названия ЖК и номеров корпусов идёт через словари. При добавлении нового ЖК нужно обновить и словари тоже.
Снимаем сразу оба ЖК
https://ddoomm.moscow/ добавить как цены появятся

'''

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from Developer_dict import developer_dict, name_dict
from functions import save_flats_to_excel

jks = {1317 : "SOLOS", 1316: "Rakurs", 1318: "DOM"}
houses = {1183: '2', 1184: '3', 1185: '4', 1186 : '1', 1187: '2', 1189: '1'}
flats = []
projects_id = [258, 883]
urls = {258: 'https://solos.moscow/api/apartment', 883: 'https://rakurs.moscow/api/v3/places', }

for pr in projects_id:

    cookies = {
        '_ym_uid': '1741613300701002441',
        '_ym_d': '1769428854',
        'FavoritesPlaces': '{"flats":[],"parking":[],"storerooms":[]}',
        'scbsid_old': '2746015342',
        '_ym_visorc': 'w',
        'cted': 'modId%3Dweu33rf4%3Bya_client_id%3D1741613300701002441',
        'ytm_session_start': '1769428854719',
        '_ym_isad': '2',
        'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
        'tmr_lvid': 'a35e064aeb5e2669b52abcab3b10442c',
        'tmr_lvidTS': '1741613300403',
        'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769515254852%2C%22sl%22%3A%7B%22224%22%3A1769428854852%2C%221228%22%3A1769428854852%7D%7D',
        '_ct_ids': 'weu33rf4%3A66232%3A358451759',
        '_ct_session_id': '358451759',
        '_ct_site_id': '66232',
        '_ct': '2700000000248281668',
        '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
        'adrdel': '1769428855109',
        'adtech_uid': 'aaafc87b-08cd-48b3-85bf-21ff7da5d0e9%3Arakurs.moscow',
        'top100_id': 't1.7733839.1661598632.1769428855191',
        'PHPSESSID': '6010a1507e7e4fef87ecd1848201f26d',
        'domain_sid': 'DcobcUAhUtzhp8Nml1yTk%3A1769428855973',
        'tmr_detect': '0%7C1769428857232',
        'sma_session_id': '2578561065',
        'SCBfrom': '',
        'smFpId_old_values': '%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%5D',
        'SCBnotShow': '-1',
        'SCBstart': '1769428859360',
        'SCBFormsAlreadyPulled': 'true',
        'SCBporogAct': '5000',
        'call_s': '___weu33rf4.1769430668.358451759.416043:1272985|2___',
        't3_sid_7733839': 's1.2092223646.1769428855192.1769428870207.1.5.1.1..',
        'sma_index_activity': '1598',
        'SCBindexAct': '1098',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
        'apptoken': 'e66a54282eb3dfcb12383577c08fe6c4',
        'content-type': 'application/json',
        'priority': 'u=0, i',
        'referer': 'https://rakurs.moscow/catalog?AgentCostStart=1628000&AgentCostEnd=60146955&allSquareStart=13&allSquareEnd=127&floorStart=-2&floorEnd=43&placeAttr[]=noBooking&page=2&category[]=%D0%9A%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D0%B0&orderBy=AgentCost%20ASC&id_projects[]=883&saleStatus[]=1',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'subdomain': 'bestcon',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        # 'cookie': '_ym_uid=1741613300701002441; _ym_d=1769428854; FavoritesPlaces={"flats":[],"parking":[],"storerooms":[]}; scbsid_old=2746015342; _ym_visorc=w; cted=modId%3Dweu33rf4%3Bya_client_id%3D1741613300701002441; ytm_session_start=1769428854719; _ym_isad=2; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=a35e064aeb5e2669b52abcab3b10442c; tmr_lvidTS=1741613300403; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1769515254852%2C%22sl%22%3A%7B%22224%22%3A1769428854852%2C%221228%22%3A1769428854852%7D%7D; _ct_ids=weu33rf4%3A66232%3A358451759; _ct_session_id=358451759; _ct_site_id=66232; _ct=2700000000248281668; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; adrdel=1769428855109; adtech_uid=aaafc87b-08cd-48b3-85bf-21ff7da5d0e9%3Arakurs.moscow; top100_id=t1.7733839.1661598632.1769428855191; PHPSESSID=6010a1507e7e4fef87ecd1848201f26d; domain_sid=DcobcUAhUtzhp8Nml1yTk%3A1769428855973; tmr_detect=0%7C1769428857232; sma_session_id=2578561065; SCBfrom=; smFpId_old_values=%5B%22cee3409c9a4246b33f9e02c26b6483bc%22%5D; SCBnotShow=-1; SCBstart=1769428859360; SCBFormsAlreadyPulled=true; SCBporogAct=5000; call_s=___weu33rf4.1769430668.358451759.416043:1272985|2___; t3_sid_7733839=s1.2092223646.1769428855192.1769428870207.1.5.1.1..; sma_index_activity=1598; SCBindexAct=1098',
    }

    params = {
            'AgentCostStart': 1,
            'AgentCostEnd': 57368927999,
            'allSquareStart': 1,
            'allSquareEnd': 500,
            'floorStart': 2,
            'floorEnd': 999,
            'id_house': '',
            'windowView': '',
            'viewsType': '',
            'repair': '',
            'placeAttr[]': 'noBooking',
            'page': 1,
            'category[]': 'Квартира',
            'orderBy': 'AgentCost ASC',
            'id_projects[]': pr,
            'saleStatus[]': 1,
        }




    date = datetime.now().date()

    def extract_digits_or_original(s):
        digits = ''.join([char for char in s if char.isdigit()])
        return int(digits) if digits else s

    while True:

        url = 'https://api.planetarf.ru/api/v3/places'


        response = requests.get(url, cookies=cookies, headers = headers, params=params)
        print(response.status_code)

        items = response.json()["places"]


        for i in items:

            url = ''
            developer = "Дар"
            project = jks.get(i['id_jk'])
            korpus = houses.get(i["id_house"])
            type = 'Квартиры'
            if i["repair"] == 'Предчистовая отделка':
                finish_type = 'Предчистовая'
            else:
                finish_type = i["repair"]
            room_count = int(i["rooms"])
            try:
                area = float(i["allSquare"])
            except:
                area = ''
            try:
                old_price = int(i['AgentCost_old'])
            except:
                old_price = ''
            try:
                price = int(i["AgentCost"])
            except:
                price = ''
            section = ''
            try:
                floor = int(i["floor"])
            except:
                floor = i["floor"]
            flat_number = int(i["id"])

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
        params['page'] += 1
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)

save_flats_to_excel(flats, project, developer)

