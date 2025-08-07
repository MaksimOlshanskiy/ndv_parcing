import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    'scbsid_old': '2750244825',
    '_ym_uid': '1742572514349913483',
    '_ym_d': '1742572514',
    '_ym_isad': '1',
    'mindboxDeviceUUID': '47c7cae1-5c38-4490-9fcc-32906301e64b',
    'directCrm-session': '%7B%22deviceGuid%22%3A%2247c7cae1-5c38-4490-9fcc-32906301e64b%22%7D',
    '_gcl_au': '1.1.492021222.1742572515',
    '_ct_ids': '1kfi6z87%3A52402%3A2124389141',
    '_ct_session_id': '2124389141',
    '_ct_site_id': '52402',
    'call_s': '___1kfi6z87.1742574308.2124389141.250668:957449|2___',
    '_ct': '800000000951584427',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ga': 'GA1.2.413323595.1742572515',
    '_gid': 'GA1.2.1081103845.1742572515',
    '_dc_gtm_UA-233007445-1': '1',
    '_gat_UA-233007445-2': '1',
    '_ym_visorc': 'b',
    'sma_session_id': '2232697176',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D',
    'cted': 'modId%3D1kfi6z87%3Bya_client_id%3D1742572514349913483%3Bclient_id%3D413323595.1742572515',
    'SCBstart': '1742572515787',
    'PHPSESSID': 'elmcisva2gntcqhqdv9ampf9ip',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'cookieWarningAccepted': 'true',
    'sma_index_activity': '2749',
    'SCBindexAct': '2247',
    '_ga_3NMHD4HT7E': 'GS1.1.1742572514.1.1.1742572534.40.0.0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,he;q=0.6,ka;q=0.5',
    'if-modified-since': 'Fri, 21 Mar 2025 14:54:51 GMT',
    'if-none-match': 'W/"87772-195b93322be"',
    'priority': 'u=1, i',
    'referer': 'https://pride-home.ru/search',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    # 'cookie': 'scbsid_old=2750244825; _ym_uid=1742572514349913483; _ym_d=1742572514; _ym_isad=1; mindboxDeviceUUID=47c7cae1-5c38-4490-9fcc-32906301e64b; directCrm-session=%7B%22deviceGuid%22%3A%2247c7cae1-5c38-4490-9fcc-32906301e64b%22%7D; _gcl_au=1.1.492021222.1742572515; _ct_ids=1kfi6z87%3A52402%3A2124389141; _ct_session_id=2124389141; _ct_site_id=52402; call_s=___1kfi6z87.1742574308.2124389141.250668:957449|2___; _ct=800000000951584427; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; _ga=GA1.2.413323595.1742572515; _gid=GA1.2.1081103845.1742572515; _dc_gtm_UA-233007445-1=1; _gat_UA-233007445-2=1; _ym_visorc=b; sma_session_id=2232697176; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%2215384b6c442ed8de443d8f25933e9f26%22%5D; cted=modId%3D1kfi6z87%3Bya_client_id%3D1742572514349913483%3Bclient_id%3D413323595.1742572515; SCBstart=1742572515787; PHPSESSID=elmcisva2gntcqhqdv9ampf9ip; SCBFormsAlreadyPulled=true; sma_postview_ready=1; cookieWarningAccepted=true; sma_index_activity=2749; SCBindexAct=2247; _ga_3NMHD4HT7E=GS1.1.1742572514.1.1.1742572534.40.0.0',
}

url = 'https://pride-home.ru/hydra/json/data.json'

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
            project = 'Pride'
            developer = 'Pioneer'
            korpus = j.get('b', '')
            room_count = j.get('rc', '')
            finish_type = j.get("renovation", '')
            if finish_type == 0:
                finish_type = 'Без отделки'
            else:
                finish_type = 'С отделкой'

            type = 'Квартира'
            area = j.get("sq", '')
            old_price = j.get("tc", '')
            price = j.get("tcd", '')
            floor = j.get('f', '')

            if price == old_price or price == 0:
                price = None

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
