import datetime
from functions import save_flats_to_excel
import requests
import random
import time

flats = []
count = 1

cookies = {
    'scbsid_old': '16031261345',
    '_gcl_au': '1.1.431150181.1785250803',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    '_ct': '2000000003595950677',
    '_ct_client_global_id': '089407ce-d8b4-596e-88ef-eee2bfcb3172',
    'c2d_widget_id': '{%22fa982595d3b0b3c67b7d153d59128b09%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20878a0f47f3c168127f6f%5C%22%2C%5C%22client_token%5C%22:%5C%22ba87cf51d31b8dfe4756a43228c33fd0%5C%22}%22}',
    '_ym_uid': '1741087840470175198',
    '_ym_d': '1786523532',
    '_ym_isad': '2',
    '_ct_ids': 'ac678915%3A2251%3A2588988696_e1983db8%3A1672%3A2588988697',
    'tmr_lvid': '4b64fb6237ba098a600cbcd8e1a5460d',
    'tmr_lvidTS': '1780219549143',
    'cted': 'modId%3De1983db8%3Bclient_id%3D95511097.1785250803%3Bya_client_id%3D1741087840470175198%7CmodId%3Dac678915%3Bclient_id%3D95511097.1785250803%3Bya_client_id%3D1741087840470175198%7CmodId%3D6d57e13c%3Bclient_id%3D95511097.1785250803',
    '_ym_visorc': 'w',
    '_ymab_param': 'IKOJV11vy3K8cAhz1iLOPCSImtArGH8Jgyzxckpiq7gZfM7VfJnYal5ojDhe6_8Q5WWn0xvAvJtwQp8ChleiZk3MGZY',
    '_gid': 'GA1.2.1295503259.1786523533',
    'mindboxDeviceUUID': 'd6b3597d-4b0b-4e45-8167-0b84971b36f7',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D',
    'domain_sid': 'f2TRaSI0-6ywHwlu0yBS3%3A1786523534055',
    'city': '1',
    'fav_session': 'eyJzZXNzaW9uX2lkIjogIl81WHlXUWo4Uzg0bldWbG1PcVV6Tlk2eHhZVUxGOXZoaG1ZaGNuUEo1aVUifQ==.anwvlw.VvPNtGioRNPqBuat4Uum3p_QJ74',
    '_ct_session_id': '2588988696',
    '_ct_site_id': '2251',
    'call_s': '___e1983db8.1786537944.2588988697.188513:1045263.511659:1459399|ac678915.1786537944.2588988696.511651:1460135|2___',
    'sma_session_id': '2804976504',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%2C%22fb99875eaaf8e4f260e4bfd2338ea7b5%22%5D',
    'SCBstart': '1786523546512',
    'tmr_detect': '0%7C1786523547223',
    'sma_postview_ready': '1',
    '_ga': 'GA1.2.95511097.1785250803',
    '_ga_G4C02PB2H3': 'GS2.1.s1786523533$o2$g1$t1786525034$j60$l0$h0',
    'cookies_is_accepted': 'true',
    '_dc_gtm_UA-18032895-2': '1',
    '_ga_3RRS9RT4P6': 'GS2.1.s1786523533$o2$g1$t1786525206$j60$l0$h0',
    'sma_index_activity': '9036',
    'SCBindexAct': '2286',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhMTEzNzYyMy01MzMxLTQ0MTEtOWEyOC04NWQxNzJmNTU0MTEiLCJpYXQiOjE3ODY1MjM1NDMsIm5iZiI6MTc4NjUyMzU0MywianRpIjoiYzg3ZGQ0YzUtNmI4ZC00MWM4LTk5ZDUtOGJmNTNjODdmZWRhIiwiZXhwIjoxNzg2NjA5OTQzLCJ0eXBlIjoiYWNjZXNzIiwiZnJlc2giOmZhbHNlfQ.Gre-j1rR-_iq7MGBk3E25z1nh6dd_DiVsIwLnPkzbd4',
    'baggage': 'sentry-environment=main,sentry-public_key=90be38a2820071f4263db07d0a07cab8,sentry-trace_id=a7ab1d900dc34c838b82769dee52cf0e,sentry-sampled=false,sentry-sample_rand=0.5480133089866642,sentry-sample_rate=0.1',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://a101.ru/commercial/pomeshheniya-i-uchastki/?commercial_type=commercial_premises&order=actual_price&deal=sell&limit=16',
    'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a7ab1d900dc34c838b82769dee52cf0e-b616b035fd392661-0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=16031261345; _gcl_au=1.1.431150181.1785250803; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ct=2000000003595950677; _ct_client_global_id=089407ce-d8b4-596e-88ef-eee2bfcb3172; c2d_widget_id={%22fa982595d3b0b3c67b7d153d59128b09%22:%22{%5C%22client_id%5C%22:%5C%22[chat]%20878a0f47f3c168127f6f%5C%22%2C%5C%22client_token%5C%22:%5C%22ba87cf51d31b8dfe4756a43228c33fd0%5C%22}%22}; _ym_uid=1741087840470175198; _ym_d=1786523532; _ym_isad=2; _ct_ids=ac678915%3A2251%3A2588988696_e1983db8%3A1672%3A2588988697; tmr_lvid=4b64fb6237ba098a600cbcd8e1a5460d; tmr_lvidTS=1780219549143; cted=modId%3De1983db8%3Bclient_id%3D95511097.1785250803%3Bya_client_id%3D1741087840470175198%7CmodId%3Dac678915%3Bclient_id%3D95511097.1785250803%3Bya_client_id%3D1741087840470175198%7CmodId%3D6d57e13c%3Bclient_id%3D95511097.1785250803; _ym_visorc=w; _ymab_param=IKOJV11vy3K8cAhz1iLOPCSImtArGH8Jgyzxckpiq7gZfM7VfJnYal5ojDhe6_8Q5WWn0xvAvJtwQp8ChleiZk3MGZY; _gid=GA1.2.1295503259.1786523533; mindboxDeviceUUID=d6b3597d-4b0b-4e45-8167-0b84971b36f7; directCrm-session=%7B%22deviceGuid%22%3A%22d6b3597d-4b0b-4e45-8167-0b84971b36f7%22%7D; domain_sid=f2TRaSI0-6ywHwlu0yBS3%3A1786523534055; city=1; fav_session=eyJzZXNzaW9uX2lkIjogIl81WHlXUWo4Uzg0bldWbG1PcVV6Tlk2eHhZVUxGOXZoaG1ZaGNuUEo1aVUifQ==.anwvlw.VvPNtGioRNPqBuat4Uum3p_QJ74; _ct_session_id=2588988696; _ct_site_id=2251; call_s=___e1983db8.1786537944.2588988697.188513:1045263.511659:1459399|ac678915.1786537944.2588988696.511651:1460135|2___; sma_session_id=2804976504; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%221760a41b46d1a0c018f5c6bd064f5ef3%22%2C%22fb99875eaaf8e4f260e4bfd2338ea7b5%22%5D; SCBstart=1786523546512; tmr_detect=0%7C1786523547223; sma_postview_ready=1; _ga=GA1.2.95511097.1785250803; _ga_G4C02PB2H3=GS2.1.s1786523533$o2$g1$t1786525034$j60$l0$h0; cookies_is_accepted=true; _dc_gtm_UA-18032895-2=1; _ga_3RRS9RT4P6=GS2.1.s1786523533$o2$g1$t1786525206$j60$l0$h0; sma_index_activity=9036; SCBindexAct=2286',
}

params = {
    'commercial_type': 'commercial_premises',
    'order': 'actual_price',
    'deal': 'sell',
    'limit': '18',
    'offset': '0',
}


while True:
    response = requests.get('https://a101.ru/api/commercial/', params=params, cookies=cookies, headers=headers)
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

            room_count = ''

            type = ''

            type = ''
            area = i["area"]
            old_price = i["price"]
            discount = ''
            price = i["actual_price"]
            section = ''
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
            finish_type = ''
            try:
                comment = i['recommended_business'][0]['name']

            except:
                comment = ''



            print(
                f"{count},{project}, тип: {type}, комнаты: {room_count}, площадь: {area}, цена: {price}, назначение: {comment}, срок сдачи: {srok_sdachi_old}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '', '', '', '', '', comment, developer, '',
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
