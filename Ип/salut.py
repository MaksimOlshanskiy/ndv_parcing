import requests
import datetime

from functions import save_flats_to_excel
from save_to_excel import save_flats_to_excel_old_new

cookies = {
    'PHPSESSID': '3BmNKzi8RMsn4EnbfhnSsNUf4nbyUHWt',
    'roistat_visit': '684257',
    'roistat_first_visit': '684257',
    'roistat_visit_cookie_expire': '1209600',
    'roistat_marker': 'seo_google_',
    'roistat_marker_old': 'seo_google_',
    'roistat_phone': '%2B7%20(495)%20308-47-52',
    'roistat_raw_phone': '74953084752',
    'roistat_call_tracking': '1',
    'roistat_phone_replacement': 'null',
    'roistat_phone_script_data': '%5B%7B%22phone%22%3A%22%2B7%20(495)%20308-47-52%22%2C%22css_selectors%22%3A%5B%22.podmena%22%5D%2C%22replaceable_numbers%22%3A%5B%5D%2C%22raw_phone%22%3A%2274953084752%22%7D%5D',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data',
    '___dc': '51700512-cb58-46e2-befc-30700e3efe10',
    '_ym_uid': '1745936414437602624',
    '_ym_d': '1745936414',
    '_ym_isad': '1',
    '_ym_visorc': 'w',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://allinsalute.ru/flats/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=3BmNKzi8RMsn4EnbfhnSsNUf4nbyUHWt; roistat_visit=684257; roistat_first_visit=684257; roistat_visit_cookie_expire=1209600; roistat_marker=seo_google_; roistat_marker_old=seo_google_; roistat_phone=%2B7%20(495)%20308-47-52; roistat_raw_phone=74953084752; roistat_call_tracking=1; roistat_phone_replacement=null; roistat_phone_script_data=%5B%7B%22phone%22%3A%22%2B7%20(495)%20308-47-52%22%2C%22css_selectors%22%3A%5B%22.podmena%22%5D%2C%22replaceable_numbers%22%3A%5B%5D%2C%22raw_phone%22%3A%2274953084752%22%7D%5D; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_marker%2Croistat_marker_old%2Croistat_phone%2Croistat_raw_phone%2Croistat_call_tracking%2Croistat_phone_replacement%2Croistat_phone_script_data; ___dc=51700512-cb58-46e2-befc-30700e3efe10; _ym_uid=1745936414437602624; _ym_d=1745936414; _ym_isad=1; _ym_visorc=w',
}

response = requests.get('https://allinsalute.ru/ajax/getFlatList.php', cookies=cookies, headers=headers)

item = response.json()

flats=[]
count=1

for i in item:
    try:
        date = datetime.date.today()
        project = "Salut"
        developer = 'ИП'
        room_count = 0
        type_ = 'Апартаменты'
        area = i['square']
        price = i['price']
        floor = i["floors"][0]

        print(
            f"{count},{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}")

        result = [date, project, '', '', '', '', '', '', '', '', '', '',
                  '', '', '', '', '', developer, '', '', '', '', '', '', '', '', '',
                  '', '', type_, 'С отделкой', room_count, area, '', price, '', '', price,
                  '', floor, '']
        flats.append(result)
        count += 1
    except KeyError as e:
        print(f"Ключ {e} не найден. Завершаем программу.")
        break

save_flats_to_excel(flats, project, developer)
