import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_near

cookies = {
    'session': 'c3f6de04bd06ce5341077637deca39c54d4fe4fca53139685038960b1e542d97',
    '_ym_uid': '1743596627909000369',
    '_ym_d': '1743596627',
    '_ym_isad': '1',
    'scbsid_old': '2796070936',
    '_ym_visorc': 'w',
    'sma_session_id': '2247066203',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%227f5cf814e808057afe665b09ade31ada%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1743596627924',
    '_cmg_cssts_GL1': '1743596628',
    '_comagic_ids_GL1': '9248698762.13192365792.1743596628',
    'SCBFormsAlreadyPulled': 'true',
    'sma_postview_ready': '1',
    'sma_index_activity': '2321',
    'SCBindexAct': '1867',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://xn--g1aelco7ds.xn--p1ai/flats',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-host': 'xn--g1aelco7ds.xn--p1ai',
    # 'cookie': 'session=c3f6de04bd06ce5341077637deca39c54d4fe4fca53139685038960b1e542d97; _ym_uid=1743596627909000369; _ym_d=1743596627; _ym_isad=1; scbsid_old=2796070936; _ym_visorc=w; sma_session_id=2247066203; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%227f5cf814e808057afe665b09ade31ada%22%5D; SCBporogAct=5000; SCBstart=1743596627924; _cmg_cssts_GL1=1743596628; _comagic_ids_GL1=9248698762.13192365792.1743596628; SCBFormsAlreadyPulled=true; sma_postview_ready=1; sma_index_activity=2321; SCBindexAct=1867',
}

params = {
    'project_id': 'cc99fa8d-104e-4da7-b827-ed8783637e1c',
    'status': 'free',
    'offset': '0',
    'limit': '100',
}

flats = []
count = 0

try:
    response = requests.get('https://xn--g1aelco7ds.xn--p1ai/api/realty-filter/residential/real-estates',
                            params=params,
                            headers=headers,
                            cookies=cookies)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            try:
                count += 1
                date = datetime.date.today()
                project = 'Союзный'
                developer = "Вектор"
                korpus = i['building_int_number']
                room_count = i['rooms']

                if room_count == 0:
                    room_count = 'студия'

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
