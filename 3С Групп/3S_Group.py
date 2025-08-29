import datetime
import time
import requests

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new_all

cookies = {
    'city': 'moskva',
    'scbsid_old': '2796070936',
    'carrotquest_device_guid': '8b3dd8bb-452c-4938-acc8-4796ca16d0f1',
    'carrotquest_uid': '2023598170235209814',
    'carrotquest_auth_token': 'user.2023598170235209814.44572-9828800291977227bbc661e3f4.d7a898ad4cd738842bfca4f4f9d2117091f238200eca2792',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NTMzNDMzMDAsImlhdCI6MTc1MzMzOTcwMCwianRpIjoiZGNjMzA1YWE4ZmY5NGY5NDk2ZTIxMzI3NWE5N2ZiNmUiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo0NDU3Mi4kdXNlcl9pZDoyMDIzNTk4MTcwMjM1MjA5ODE0Il0sImFwcF9pZCI6NDQ1NzIsInVzZXJfaWQiOjIwMjM1OTgxNzAyMzUyMDk4MTR9.yVy_pU1Y8ZQeyfFlr0SQ3dlWd7bE2RbcnXJnZCPPG6Q',
    'carrotquest_realtime_services_transport': 'wss',
    '_ym_uid': '1753339701823155509',
    '_ym_d': '1753339701',
    '_ym_isad': '1',
    'sma_session_id': '2368572420',
    '_ym_visorc': 'w',
    'SCBnotShow': '-1',
    '_cmg_cssteBI3b': '1753339703',
    '_comagic_ideBI3b': '9646827742.13660695482.1753339703',
    'smFpId_old_values': '%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D',
    'carrotquest_closed_part_id': '2023598340674947846',
    'carrotquest_session': 'xjb1gjxm3r9trv3uxp9j3dr96axpei0h',
    'carrotquest_session_started': '1',
    'SCBporogAct': '5000',
    'sma_index_activity': '14182',
    'SCBindexAct': '2723',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://3s.group/selections/flat?area_min=20&area_max=73&price_min=6535280&price_max=30939220&order=-status,price&limit=9&city=moskva',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'city=moskva; scbsid_old=2796070936; carrotquest_device_guid=8b3dd8bb-452c-4938-acc8-4796ca16d0f1; carrotquest_uid=2023598170235209814; carrotquest_auth_token=user.2023598170235209814.44572-9828800291977227bbc661e3f4.d7a898ad4cd738842bfca4f4f9d2117091f238200eca2792; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NTMzNDMzMDAsImlhdCI6MTc1MzMzOTcwMCwianRpIjoiZGNjMzA1YWE4ZmY5NGY5NDk2ZTIxMzI3NWE5N2ZiNmUiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDo0NDU3Mi4kdXNlcl9pZDoyMDIzNTk4MTcwMjM1MjA5ODE0Il0sImFwcF9pZCI6NDQ1NzIsInVzZXJfaWQiOjIwMjM1OTgxNzAyMzUyMDk4MTR9.yVy_pU1Y8ZQeyfFlr0SQ3dlWd7bE2RbcnXJnZCPPG6Q; carrotquest_realtime_services_transport=wss; _ym_uid=1753339701823155509; _ym_d=1753339701; _ym_isad=1; sma_session_id=2368572420; _ym_visorc=w; SCBnotShow=-1; _cmg_cssteBI3b=1753339703; _comagic_ideBI3b=9646827742.13660695482.1753339703; smFpId_old_values=%5B%22a932251185d3bf41fcd7e2656de279f5%22%5D; carrotquest_closed_part_id=2023598340674947846; carrotquest_session=xjb1gjxm3r9trv3uxp9j3dr96axpei0h; carrotquest_session_started=1; SCBporogAct=5000; sma_index_activity=14182; SCBindexAct=2723',
}


params = {
    'area_min': '1',
    'area_max': '999',
    'price_min': '653520',
    'price_max': '3093922099',
    'order': '-status,price',
    'limit': '9',
    'city': 'moskva',
}

url = 'https://3s.group/api/flats/'

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while url:
    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        item = response.json()

        items = item.get("results", [])

        for i in items:
            date = datetime.date.today()
            project = i["project_name"]
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
            developer = "3S Group"
            okrug = ''
            district = ''
            adress = ''
            eskrou = ''
            korpus = i["building"].replace('Дом ', '')
            konstruktiv = ''
            klass = ''
            srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира'
            finish_type = 'Без отделки'
            room_count = i["rooms"]

            if room_count == 0:
                room_count = 'студия'

            area = float(i["area"])
            price_per_metr = ''

            try:
                old_price = round(float(i["original_price"]))
            except:
                old_price = round(float(i["price"]))

            discount = ''
            price_per_metr_new = ''
            price = round(float(i["price"]))
            section = ''
            floor = i["floor"]
            flat_number = ''

            if price == old_price:
                price = None

            print(
                f"{project},комнаты: {room_count}, площадь: {area}, цена: {price}, корпус: {korpus}, этаж: {floor}, тип: {type}")
            result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway,
                      mck,
                      distance_to_mck, time_to_mck, distance_to_bkl,
                      time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                      konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                      stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                      price_per_metr_new, price, section, floor, flat_number]
            flats.append(result)

        # Проверяем, есть ли следующая страница
        next_url = item.get("next")
        if next_url:
            url = next_url  # Переходим на следующую страницу
            params = {}  # Очищаем параметры, так как URL следующей страницы уже содержит их
        else:
            break  # Если следующей страницы нет, выходим из цикла
    else:
        print(f'Ошибка: {response.status_code}')
        break

    time.sleep(0.05)

save_flats_to_excel(flats, 'all', developer)
