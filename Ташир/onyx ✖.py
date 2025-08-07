import datetime
import time
from save_to_excel import save_flats_to_excel_old_new
import requests

cookies = {
    '_gcl_au': '1.1.885472664.1742558228',
    '_ga': 'GA1.2.1010669920.1742558228',
    '_gid': 'GA1.2.1678286042.1742558228',
    '_gat_UA-162478415-5': '1',
    '_ym_uid': '1742558228421767629',
    '_ym_isad': '1',
    '_ct_ids': 'zl24jou3%3A26799%3A2124279845',
    '_ct_session_id': '2124279845',
    '_ct_site_id': '26799',
    'call_s': '___zl24jou3.1742560022.2124279845.83579:660044|2___',
    '_ct': '800000000951513634',
    '_ym_visorc': 'w',
    '_ct_client_global_id': 'b7bf8ff5-0827-5c41-830e-bad9491c1c5e',
    '_ga_TQQ6Z19J81': 'GS1.2.1742558228.1.0.1742558228.60.0.0',
    'cted': 'modId%3Dzl24jou3%3Bclient_id%3D1010669920.1742558228%3Bya_client_id%3D1742558228421767629',
    '_ym_d': '1742558234',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://onyx-deluxe.com/filter',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-site': 'onyx-deluxe.com',
    # 'cookie': '_gcl_au=1.1.885472664.1742558228; _ga=GA1.2.1010669920.1742558228; _gid=GA1.2.1678286042.1742558228; _gat_UA-162478415-5=1; _ym_uid=1742558228421767629; _ym_isad=1; _ct_ids=zl24jou3%3A26799%3A2124279845; _ct_session_id=2124279845; _ct_site_id=26799; call_s=___zl24jou3.1742560022.2124279845.83579:660044|2___; _ct=800000000951513634; _ym_visorc=w; _ct_client_global_id=b7bf8ff5-0827-5c41-830e-bad9491c1c5e; _ga_TQQ6Z19J81=GS1.2.1742558228.1.0.1742558228.60.0.0; cted=modId%3Dzl24jou3%3Bclient_id%3D1010669920.1742558228%3Bya_client_id%3D1742558228421767629; _ym_d=1742558234',
}

params = {
    'offset': '0',
}


url = 'https://onyx-deluxe.com/api/flat/'

flats = []
count = 1


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
            project = "Onyx"
            developer = 'Ташир'
            room_count = i["rooms"]
            type = 'Квартира'
            finish_type = i["facing"]

            if finish_type == 0:
                finish_type = 'Без отделки'
            elif finish_type == 1:
                finish_type = 'Предчистовая'
            else:
                finish_type = 'С отделкой'

            area = i["area"]
            old_price = i["origin_price"]
            price = i["price"]
            section = i["section_number"]
            floor = i["floor_number"]
            price_per_metr_new = i["ppm"]

            print(
                f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

            result = [date, project, '', '', '', '', '', '', '', '', '', '',
                      '', '', '', '', '', developer, '', '', '', '', '1', '', '', '', '',
                      '', '', type, finish_type, room_count, area, '', old_price, '', price_per_metr_new, price,
                      section, floor, '']
            flats.append(result)
            count += 1
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

save_flats_to_excel_old_new(flats, project, developer)
