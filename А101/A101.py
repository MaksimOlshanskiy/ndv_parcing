import datetime
from functions import save_flats_to_excel
import requests
import random
import time

flats = []
count = 1

cookies = {
    '_ym_uid': '1749566032723023965',
    '_ym_d': '1774364059',
    '_ymab_param': 'J72-K_LD2sAztOy52QfJWB_wnTp_Rk6EQ8brZlQsYYVBnQwSnq7soDLbQuqXgWiH6UyzmWvdSLtnFk97RXndfYbRT-M',
    'scbsid_old': '2746015342',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_ct': '2000000003558865018',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_gcl_au': '1.1.1726274765.1774364060',
    'tmr_lvid': '07243b423e2c746bec6ba8d10b229834',
    'tmr_lvidTS': '1749566033707',
    'c2d_widget_id': '{%22fa982595d3b0b3c67b7d153d59128b09%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%2017bd648ccb1cf0ce30ee%5C%22%2C%5C%22client_token%5C%22:%5C%2298fcae3aaf000600db8f8d62ce7f810e%5C%22}%22}',
    'city': '1',
    '_ym_isad': '2',
    'cted': 'modId%3De1983db8%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965%7CmodId%3Dac678915%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965%7CmodId%3D6d57e13c%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965',
    '_ym_visorc': 'w',
    'sma_session_id': '2664573904',
    'SCBfrom': 'https%3A%2F%2Fyandex.ru%2F',
    '_ct_ids': 'ac678915%3A2251%3A2536855261_e1983db8%3A1672%3A2536855262',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'SCBstart': '1775717470698',
    'smFpId_old_values': '%5B%22cd14d52d59b08c237e2004225d23c665%22%2C%22ab19ac2380782ae239d725bfec8e9f49%22%5D',
    'domain_sid': 'o-kc4kLSkJHA_2ZNgAWHN%3A1775717471666',
    '_gid': 'GA1.2.35263487.1775717473',
    'cookies_is_accepted': 'true',
    'fav_session': 'eyJzZXNzaW9uX2lkIjogImM1SjltSU01OExobXRuYnFBQV92cFdNVV9hRW9PWkJDRUNaUm5uLTByZWcifQ==.addRTg.p3wlwMr65vbPbbJbsZBRAkV6EUI',
    '_ct_session_id': '2536855261',
    '_ct_site_id': '2251',
    'call_s': '___e1983db8.1775733135.2536855262.200723:1045264|ac678915.1775733135.2536855261.195597:176028|2___',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ga': 'GA1.2.329660285.1774364061',
    'tmr_detect': '0%7C1775718737574',
    '_dc_gtm_UA-18032895-2': '1',
    '_ga_G4C02PB2H3': 'GS2.1.s1775717470$o2$g1$t1775719118$j53$l0$h0',
    '_ga_3RRS9RT4P6': 'GS2.1.s1775717470$o2$g1$t1775719120$j44$l0$h0',
    'sma_index_activity': '81812',
    'SCBindexAct': '3505',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI2ZGMxODIzZS0xODA0LTQ4MGItODYxNS01YTRiOWEyYTQzMTMiLCJpYXQiOjE3NzU3MTc0NzQsIm5iZiI6MTc3NTcxNzQ3NCwianRpIjoiZmUzMDk0YmMtYmYwYS00NWI0LThhMjAtNzk1N2E2NTVjYzAxIiwiZXhwIjoxNzc1ODAzODc0LCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.glYMSWr-1-rL4Kggp6F3RZbRzca714TWf9FkBXbFJlA',
    'baggage': 'sentry-environment=main,sentry-public_key=90be38a2820071f4263db07d0a07cab8,sentry-trace_id=c789d79c655b47cda3807e08a5401f4f,sentry-sampled=false,sentry-sample_rand=0.3958451498645539,sentry-sample_rate=0.1',
    'priority': 'u=1, i',
    'referer': 'https://a101.ru/kvartiry/?order=actual_price&design=2',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'c789d79c655b47cda3807e08a5401f4f-b4acb6a62c28e690-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1749566032723023965; _ym_d=1774364059; _ymab_param=J72-K_LD2sAztOy52QfJWB_wnTp_Rk6EQ8brZlQsYYVBnQwSnq7soDLbQuqXgWiH6UyzmWvdSLtnFk97RXndfYbRT-M; scbsid_old=2746015342; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ct=2000000003558865018; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _gcl_au=1.1.1726274765.1774364060; tmr_lvid=07243b423e2c746bec6ba8d10b229834; tmr_lvidTS=1749566033707; c2d_widget_id={%22fa982595d3b0b3c67b7d153d59128b09%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%2017bd648ccb1cf0ce30ee%5C%22%2C%5C%22client_token%5C%22:%5C%2298fcae3aaf000600db8f8d62ce7f810e%5C%22}%22}; city=1; _ym_isad=2; cted=modId%3De1983db8%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965%7CmodId%3Dac678915%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965%7CmodId%3D6d57e13c%3Bclient_id%3D329660285.1774364061%3Bya_client_id%3D1749566032723023965; _ym_visorc=w; sma_session_id=2664573904; SCBfrom=https%3A%2F%2Fyandex.ru%2F; _ct_ids=ac678915%3A2251%3A2536855261_e1983db8%3A1672%3A2536855262; SCBnotShow=-1; SCBporogAct=5000; SCBstart=1775717470698; smFpId_old_values=%5B%22cd14d52d59b08c237e2004225d23c665%22%2C%22ab19ac2380782ae239d725bfec8e9f49%22%5D; domain_sid=o-kc4kLSkJHA_2ZNgAWHN%3A1775717471666; _gid=GA1.2.35263487.1775717473; cookies_is_accepted=true; fav_session=eyJzZXNzaW9uX2lkIjogImM1SjltSU01OExobXRuYnFBQV92cFdNVV9hRW9PWkJDRUNaUm5uLTByZWcifQ==.addRTg.p3wlwMr65vbPbbJbsZBRAkV6EUI; _ct_session_id=2536855261; _ct_site_id=2251; call_s=___e1983db8.1775733135.2536855262.200723:1045264|ac678915.1775733135.2536855261.195597:176028|2___; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ga=GA1.2.329660285.1774364061; tmr_detect=0%7C1775718737574; _dc_gtm_UA-18032895-2=1; _ga_G4C02PB2H3=GS2.1.s1775717470$o2$g1$t1775719118$j53$l0$h0; _ga_3RRS9RT4P6=GS2.1.s1775717470$o2$g1$t1775719120$j44$l0$h0; sma_index_activity=81812; SCBindexAct=3505',
}

params = {
    'order': 'actual_price',
    'limit': '12',
    'offset': '0',
}


while True:
    response = requests.get('https://a101.ru/api/flats/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        item = response.json()
        items = item.get("results", [])

        for i in items:

            if i["project"] == 'Испанские кварталы':
                continue

            if i["project"] == 'Белые ночи':
                continue

            if i['status'] == 4:
                continue

            date = datetime.date.today()
            project = i["project"]
            status = ''
            developer = 'А101'
            district = ''
            korpus = i["building"]
            try:
                if project == 'Скандинавия' and int(korpus.split('.')[0]) < 25:
                    project = 'Скандинавия Юг'
                if project == 'Скандинавия' and int(korpus.split('.')[0]) >= 25:
                    project = 'Скандинавия Центр'
            except:
                pass

            room_count = str(i["room"])
            if i['euro']:
                room_count += 'е'
            if room_count == '1 е':
                room_count = '2 е'
            if i['whitebox']:
                finish_type = 'Предчистовая'
            elif i['design']:
                finish_type = 'С отделкой'
            else:
                finish_type = 'Без отделки'

            type = i["room_name"]
            if type == 'Студия':
                room_count = 'Студия'

            type = i['type'].replace('flat', 'квартиры')
            area = i["area"]
            old_price = i["price"]
            discount = ''
            price = i["actual_price"]
            section = i["section_number"]
            try:
                floor = float(i["floor"])
            except:
                floor = i["floor"].replace(' ', '')

            if price == old_price:
                price = None
            try:
                srok_sdachi_old = i["building_stage_rve_date"]
            except:
                srok_sdachi_old = ''


            print(
                f"{count},{project}, тип: {type}, комнаты: {room_count}, площадь: {area}, цена: {price}, отделка: {finish_type}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', developer, '',
                      '', '', '', korpus, '', '', '', srok_sdachi_old, '', '', type, finish_type, room_count, area,
                      '', old_price, '', '', price, section, floor, '']
            flats.append(result)
            count += 1

        # Проверяем, есть ли следующая страница
        if not items:
            break
        params['offset'] = str(int(params['offset']) + int(params['limit']))

    else:
        print(f'Ошибка: {response.status_code}')
        break
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)


save_flats_to_excel(flats, project, developer, kvartirografia=False)
