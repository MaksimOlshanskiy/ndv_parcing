import datetime
import time

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_middle
import requests

cookies = {
    'session': 'aa51c0a817ca2ddf676b5c3107d541d5da32f60f31ca6a4999dbbd50f54f166b',
    '_ga': 'GA1.1.1313715207.1753688326',
    '_ym_uid': '1744027341243641216',
    '_ym_d': '1753688326',
    '_ym_isad': '1',
    'roistat_visit': '668135',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    '_ym_visorc': 'w',
    'nfCpwHashId': '47265bf9785fbaea1ce68aefaa674a8d30f2540ffcc6afc45f9e4f243d739329',
    '_cmg_csstIbdzG': '1753688327',
    '_comagic_idIbdzG': '10893347831.15204330676.1753688330',
    'scbsid_old': '2796070936',
    'sma_session_id': '2373021597',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D',
    '_ga_F8P0RH67MV': 'GS2.1.s1753688325$o1$g1$t1753688333$j52$l0$h0',
    'SCBporogAct': '5000',
    'SCBstart': '1753688333794',
    'SCBFormsAlreadyPulled': 'true',
    'SCBindexAct': '1637',
    'sma_index_activity': '2637',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://legendakorenevo.ru/flats',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'legendakorenevo.ru',
    # 'cookie': 'session=aa51c0a817ca2ddf676b5c3107d541d5da32f60f31ca6a4999dbbd50f54f166b; _ga=GA1.1.1313715207.1753688326; _ym_uid=1744027341243641216; _ym_d=1753688326; _ym_isad=1; roistat_visit=668135; roistat_visit_cookie_expire=1209600; roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; _ym_visorc=w; nfCpwHashId=47265bf9785fbaea1ce68aefaa674a8d30f2540ffcc6afc45f9e4f243d739329; _cmg_csstIbdzG=1753688327; _comagic_idIbdzG=10893347831.15204330676.1753688330; scbsid_old=2796070936; sma_session_id=2373021597; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D; _ga_F8P0RH67MV=GS2.1.s1753688325$o1$g1$t1753688333$j52$l0$h0; SCBporogAct=5000; SCBstart=1753688333794; SCBFormsAlreadyPulled=true; SCBindexAct=1637; sma_index_activity=2637',
}

params = {
        'project_id': "61b193a5-aa22-4f3a-bf22-216ebc5648b1",
        'status': 'free',
        'offset': 0,
        'limit': 100,
        'order_by': 'price',
    }

flats = []
limit = 100
total_flats = 0
processed_flats = 0
project_ids = ["61b193a5-aa22-4f3a-bf22-216ebc5648b1", "a5f9b6b9-037d-4cd8-981c-cbd55e93a5c0"]
project_dict = {"61b193a5-aa22-4f3a-bf22-216ebc5648b1" : 'Легенда Коренево', "a5f9b6b9-037d-4cd8-981c-cbd55e93a5c0" : 'Легенда Марусино'}

for project_id in project_ids:

    params['project_id'] = project_id
    params['offset'] = 0

    try:


        while True:



            response = requests.get('https://legendakorenevo.ru/api/realty-filter/residential/real-estates',
                                    params=params,
                                    headers=headers,
                                    cookies=cookies)

            if response.status_code == 200:
                data = response.json()
                current_batch = len(data)
                processed_flats += current_batch

                for i in data:
                    try:
                        date = datetime.date.today()
                        project = project_dict.get(project_id, project_id)
                        developer = "Некрасовка Девелопмент"
                        korpus = i['building_number'].replace('Корпус ', '')
                        room_count = i['rooms']

                        if room_count == 0:
                            room_count = 'студия'

                        type_ = "Квартира"

                        if i['finishing_type'] == 'no':
                            finish_type = 'Без отделки'
                        else:
                            finish_type = "С отделкой"

                        area = i['total_area']
                        old_price = i['old_price']
                        price = i['price']
                        section = i['section_number']
                        floor = i['floor_number']

                        if old_price == price:
                            price = None

                        print(
                            f"{project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                        result = [
                            date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                            '', '', '', developer, '', '', '', '', korpus, '', '', '', '',
                            '', '', type_, finish_type, room_count, area, '', old_price, '',
                            '', price, section, int(str(floor)), ''
                        ]
                        flats.append(result)

                    except Exception as e:
                        print(f"Ошибка при обработке квартиры: {e}")
                        continue

                if not data:
                    break

                params['offset'] += params['limit']
                print(f"Обработано {processed_flats} квартир")

                time.sleep(1)
            else:
                print(f'Ошибка запроса: {response.status_code}, {response.text}')
                break


    except Exception as e:
        print(f"Общая ошибка: {e}")

if flats:
    save_flats_to_excel(flats, 'all', 'Некрасовка Девелопмент')
else:
    print("Нет данных для сохранения")
