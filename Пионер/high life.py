import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '_ym_uid': '1742568900473435868',
    '_ym_d': '1742568900',
    'scbsid_old': '2750244825',
    '_gcl_au': '1.1.725266481.1742568900',
    'PHPSESSID': 'kh9vhb62afb9djnld4j76abrk2',
    '_ym_isad': '1',
    'mindboxDeviceUUID': '47c7cae1-5c38-4490-9fcc-32906301e64b',
    'directCrm-session': '%7B%22deviceGuid%22%3A%2247c7cae1-5c38-4490-9fcc-32906301e64b%22%7D',
    '_ym_visorc': 'w',
    '_ct_ids': 'n5ovc6d9%3A42226%3A756658106',
    '_ct_session_id': '756658106',
    '_ct_site_id': '42226',
    'call_s': '___n5ovc6d9.1742570694.756658106.181953:625510|2___',
    '_ct': '1600000000502855377',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    'cted': 'modId%3Dn5ovc6d9%3Bya_client_id%3D1742568900473435868%3Bclient_id%3D1627482242.1742568900',
    'lp_pageview_1942': '1',
    'lp_vid_1942': 'b5053523-039f-414c-8aea-a6a6d7f5687c',
    'lp_session_start_1942': '1742568901044',
    'lp_session_1942': '723913',
    'lp_abtests_1942': '[]',
    'sessionId': '17425689017952471797',
    '_ga': 'GA1.2.1627482242.1742568900',
    '_gid': 'GA1.2.1693660697.1742568902',
    '_dc_gtm_UA-191014586-1': '1',
    'sma_session_id': '2232625485',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D',
    'SCBstart': '1742568902248',
    'SCBporogAct': '5000',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'sma_index_activity': '381',
    'SCBindexAct': '381',
    '_ga_6XPFZP5TGR': 'GS1.1.1742568900.1.0.1742568915.45.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://highlife.ru/search',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1742568900473435868; _ym_d=1742568900; scbsid_old=2750244825; _gcl_au=1.1.725266481.1742568900; PHPSESSID=kh9vhb62afb9djnld4j76abrk2; _ym_isad=1; mindboxDeviceUUID=47c7cae1-5c38-4490-9fcc-32906301e64b; directCrm-session=%7B%22deviceGuid%22%3A%2247c7cae1-5c38-4490-9fcc-32906301e64b%22%7D; _ym_visorc=w; _ct_ids=n5ovc6d9%3A42226%3A756658106; _ct_session_id=756658106; _ct_site_id=42226; call_s=___n5ovc6d9.1742570694.756658106.181953:625510|2___; _ct=1600000000502855377; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; cted=modId%3Dn5ovc6d9%3Bya_client_id%3D1742568900473435868%3Bclient_id%3D1627482242.1742568900; lp_pageview_1942=1; lp_vid_1942=b5053523-039f-414c-8aea-a6a6d7f5687c; lp_session_start_1942=1742568901044; lp_session_1942=723913; lp_abtests_1942=[]; sessionId=17425689017952471797; _ga=GA1.2.1627482242.1742568900; _gid=GA1.2.1693660697.1742568902; _dc_gtm_UA-191014586-1=1; sma_session_id=2232625485; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D; SCBstart=1742568902248; SCBporogAct=5000; SCBFormsAlreadyPulled=true; sma_postview_ready=1; sma_index_activity=381; SCBindexAct=381; _ga_6XPFZP5TGR=GS1.1.1742568900.1.0.1742568915.45.0.0',
}

url = 'https://highlife.ru/hydra/json/data.json'

flats = []
count = 1

response = requests.get(url, cookies=cookies, headers=headers)

if response.status_code == 200:
    data = response.json()
    items = data.get('apartments', {})

    for i, j in items.items():
        st = j.get('st', '')
        if st == 1:
            date = datetime.date.today()
            project = 'High Life'
            developer = 'Pioneer'
            korpus = j.get('b', '')
            room_count = j.get('rc', '')
            finish_type = j.get("d", '')

            if finish_type == 'Квартиры без отделки':
                finish_type = 'Без отделки'
            elif finish_type == 'Квартиры с отделкой':
                finish_type = 'С отделкой'
            else:
                finish_type='Предчистовая'

            type = 'Квартира'
            area = j.get("sq", '')
            old_price = j.get("tc", '')

            price = j.get("tcd", '')
            floor = j.get('f', '')

            if old_price==price:
                price=None

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', '', price,
                      '', floor, '']
            flats.append(result)
            count += 1
        else:
            continue
else:
    print(f'Ошибка: {response.status_code}')


time.sleep(0.05)

save_flats_to_excel(flats, project, developer)
