import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'session': '6d13ea4dbd4411cfcfaedcf7cc46a53ca29e3e561b930d0adf79e7c6377f7531',
    '_ym_uid': '1743595496684033293',
    '_ym_d': '1743595496',
    '_ym_isad': '1',
    'scbsid_old': '2796070936',
    '_ym_visorc': 'w',
    'sma_session_id': '2247043271',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBporogAct': '5000',
    'smFpId_old_values': '%5B%227f5cf814e808057afe665b09ade31ada%22%5D',
    'SCBstart': '1743595498164',
    '_cmg_cssts_GL1': '1743595498',
    '_comagic_ids_GL1': '9248627332.13192277732.1743595500',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'SCBindexAct': '4790',
    'sma_index_activity': '5240',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://xn----8sbafbjiwbtdpqld4bj0a8d8f.xn--p1ai/flats',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 'xn----8sbafbjiwbtdpqld4bj0a8d8f.xn--p1ai',
    # 'cookie': 'session=6d13ea4dbd4411cfcfaedcf7cc46a53ca29e3e561b930d0adf79e7c6377f7531; _ym_uid=1743595496684033293; _ym_d=1743595496; _ym_isad=1; scbsid_old=2796070936; _ym_visorc=w; sma_session_id=2247043271; SCBfrom=; SCBnotShow=-1; SCBporogAct=5000; smFpId_old_values=%5B%227f5cf814e808057afe665b09ade31ada%22%5D; SCBstart=1743595498164; _cmg_cssts_GL1=1743595498; _comagic_ids_GL1=9248627332.13192277732.1743595500; SCBFormsAlreadyPulled=true; sma_postview_ready=1; SCBindexAct=4790; sma_index_activity=5240',
}

params = {
    'project_id': '40dfce3d-813a-4ab1-884c-edb988934e45',
    'status': 'free',
    'limit': '100',
    'order_by': '-discount_value',
}

flats = []
count = 0

try:
    response = requests.get(
        'https://xn----8sbafbjiwbtdpqld4bj0a8d8f.xn--p1ai/api/realty-filter/residential/real-estates',
        params=params,
        headers=headers,
        cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Одинцовские кварталы'
                developer = "Стройтек"
                korpus = i['building_int_number']
                room_count = i['rooms']
                type_ = "Квартира"
                area = i['total_area']
                old_price = i['old_price']
                price = i['price']
                section = i['section_number']
                floor = i['floor_number']

                if old_price == price:
                    price = None

                print(
                    f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                result = [
                    date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                    '', '', '', developer, '', '', '', '', float(str(korpus)), '', '', '', '',
                    '', '', type_, 'Без отделки', room_count, area, '', old_price, '',
                    '', price, int(section), int(str(floor)), ''
                ]
                flats.append(result)

            except Exception as e:
                print(f"Ошибка при обработке квартиры: {e}")
                continue

    else:
        print(f'Ошибка запроса: {response.status_code}, {response.text}')

except Exception as e:
    print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
