import datetime
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

cookies = {
    'scbsid_old': '2796070936',
    '_ym_uid': '1745314305680051478',
    '_ym_d': '1745314305',
    '_ga': 'GA1.1.127828893.1745314305',
    'tmr_lvid': 'b0a294b78f5b0355378aa80b0f3f464d',
    'tmr_lvidTS': '1745314356904',
    '_ga_E78QE2T33G': 'GS1.1.1745413749.2.1.1745414600.0.0.0',
    'session': 'b5a52b280ed713dcd3f39a63a1f5f8b2aa7a10d4e303146a480d35b0ebe5c7a5',
    'smFpId_old_values': '%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%2C%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%2214661064101748ef143791c1ac1e56c6%22%2C%22a932251185d3bf41fcd7e2656de279f5%22%5D',
    '_ym_isad': '1',
    '_cmg_cssta5xp1': '1753359840',
    '_comagic_ida5xp1': '10871550301.15179554346.1753359839',
    '_ym_visorc': 'w',
    'sma_session_id': '2368953027',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'SCBstart': '1753359851494',
    'SCBFormsAlreadyPulled': 'true',
    'SCBporogAct': '5000',
    'SCBindexAct': '2687',
    'sma_index_activity': '3389',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://detali-dom.ru/flats?montarage=31739&montarage=107369&offset=13&limit=16',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-host': 'detali-dom.ru',
    # 'cookie': 'scbsid_old=2796070936; _ym_uid=1745314305680051478; _ym_d=1745314305; _ga=GA1.1.127828893.1745314305; tmr_lvid=b0a294b78f5b0355378aa80b0f3f464d; tmr_lvidTS=1745314356904; _ga_E78QE2T33G=GS1.1.1745413749.2.1.1745414600.0.0.0; session=b5a52b280ed713dcd3f39a63a1f5f8b2aa7a10d4e303146a480d35b0ebe5c7a5; smFpId_old_values=%5B%2204b0ffbac42ccceb635ec5bff5b15618%22%2C%22408b57183b182c79d2b9a0b3fa0d260b%22%2C%2214661064101748ef143791c1ac1e56c6%22%2C%22a932251185d3bf41fcd7e2656de279f5%22%5D; _ym_isad=1; _cmg_cssta5xp1=1753359840; _comagic_ida5xp1=10871550301.15179554346.1753359839; _ym_visorc=w; sma_session_id=2368953027; SCBfrom=; SCBnotShow=-1; SCBstart=1753359851494; SCBFormsAlreadyPulled=true; SCBporogAct=5000; SCBindexAct=2687; sma_index_activity=3389',
}

limit = 100  # максимальный лимит, который принимает сервер
offset = 0
flats = []
count = 0

while True:
    params = {
        'project_id': 'c6d39b6a-68b6-4a90-b85f-a995a93e0889',
        'status': 'free',
        'montarage': ['31739', '107369'],
        'offset': str(offset),
        'limit': str(limit),
        'order_by': 'price',
    }
    try:
        response = requests.get('https://detali-dom.ru/api/realty-filter/residential/real-estates',
                                params=params,
                                headers=headers,
                                cookies=cookies,
                                timeout=10)

        if response.status_code == 200:
            data = response.json()

            if not data:  # если пустой ответ, значит данные кончились
                print("Данных больше нет, выходим из цикла")
                break

            for i in data:
                try:
                    count += 1
                    date = datetime.date.today()
                    project = 'Детали'
                    developer = "Плюс девелопмент"
                    korpus = i['building_int_number']
                    room_count = i.get('rooms', 0)

                    if room_count == 0:
                        room_count = 'студия'

                    type_ = "Квартира"
                    area = i.get('total_area', 0)
                    price_per_metr = i.get('old_ppm', 0)
                    old_price = int(round(i.get('old_price', 0), 0))
                    price = int(round(i.get('price', 0), 0))
                    section = i.get('section_number', 0)
                    floor = i.get('floor_number', 0)

                    if old_price == price:
                        price = None

                    print(
                        f"{count} | {project}, комнаты: {room_count}, площадь: {area}, цена: {price}, стар. цена: {old_price}, корпус: {korpus}, этаж: {floor}")

                    result = [
                        date, project, '', '', '', '', '', '', '', '', '', '', '', '',
                        '', '', '', developer, '', '', '', '', float(korpus) if korpus else '',
                        '', '', '', '', '', '', type_, 'Без отделки', room_count, area,
                        '', old_price, '', '', price,
                        int(section) if section else 0, int(floor) if floor else 0, ''
                    ]
                    flats.append(result)

                except Exception as e:
                    print(f"Ошибка при обработке квартиры: {e}")
                    continue

            offset += limit  # сдвигаем смещение для следующей страницы

        else:
            print(f'Ошибка запроса: {response.status_code}, {response.text}')
            break  # прерываем цикл при ошибке

    except Exception as e:
        print(f"Общая ошибка: {e}")
        break

if flats:
    save_flats_to_excel(flats, project, developer)
else:
    print("Нет данных для сохранения")
