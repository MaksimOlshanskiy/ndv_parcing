import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

cookies = {
    'SCBFormsAlreadyPulled': 'true',
    'PHPSESSID': 'P0x6UkI61PTRUL3FZB3ggzj9HDpG5l0W',
    'BX_USER_ID': '15016e9404744ee3cb1a5dfed786822b',
    'session_timer_104054': '1',
    'session_timer_104055': '1',
    'session_timer_104056': '1',
    'session_timer_104057': '1',
    'session_timer_104058': '1',
    'scbsid_old': '2746015342',
    '_gcl_au': '1.1.1336949076.1743752809',
    '_ct_ids': 't6xj36r8%3A44212%3A568796021',
    '_ct_session_id': '568796021',
    '_ct_site_id': '44212',
    '_ct': '1700000000373738504',
    '_ct_client_global_id': 'ac7bc830-33a7-54d1-b90e-949b89f995ae',
    '_gid': 'GA1.2.856025241.1743752809',
    'sma_session_id': '2249087758',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1743752810731',
    '_ym_uid': '1743752813572686734',
    '_ym_d': '1743752813',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cted': 'modId%3Dt6xj36r8%3Bclient_id%3D633920870.1743752809%3Bya_client_id%3D1743752813572686734',
    '_gat_gtag_UA_81922846_6': '1',
    'SCBFormsAlreadyPulled': 'true',
    'seconds_on_page_104054': '91',
    'seconds_on_page_104055': '91',
    'seconds_on_page_104056': '91',
    'seconds_on_page_104057': '91',
    'seconds_on_page_104058': '91',
    '_ga': 'GA1.2.633920870.1743752809',
    'call_s': '___t6xj36r8.1743754700.568796021.193685:592575.281015:831755|2___',
    '_ga_D6VNBFBRX6': 'GS1.1.1743752808.1.1.1743752919.34.0.0',
    'SCBindexAct': '1396',
    'sma_index_activity': '8503',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'ajaxdynamic': 'y',
    'bx-ajax': 'true',
    'container': 'catalog-container-OQ3k9P-pagination',
    'priority': 'u=1, i',
    'referer': 'https://skolkovoone.ru/catalog/filter/clear/apply/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'SCBFormsAlreadyPulled=true; PHPSESSID=P0x6UkI61PTRUL3FZB3ggzj9HDpG5l0W; BX_USER_ID=15016e9404744ee3cb1a5dfed786822b; session_timer_104054=1; session_timer_104055=1; session_timer_104056=1; session_timer_104057=1; session_timer_104058=1; scbsid_old=2746015342; _gcl_au=1.1.1336949076.1743752809; _ct_ids=t6xj36r8%3A44212%3A568796021; _ct_session_id=568796021; _ct_site_id=44212; _ct=1700000000373738504; _ct_client_global_id=ac7bc830-33a7-54d1-b90e-949b89f995ae; _gid=GA1.2.856025241.1743752809; sma_session_id=2249087758; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%5D; SCBporogAct=5000; SCBstart=1743752810731; _ym_uid=1743752813572686734; _ym_d=1743752813; _ym_isad=2; _ym_visorc=w; cted=modId%3Dt6xj36r8%3Bclient_id%3D633920870.1743752809%3Bya_client_id%3D1743752813572686734; _gat_gtag_UA_81922846_6=1; SCBFormsAlreadyPulled=true; seconds_on_page_104054=91; seconds_on_page_104055=91; seconds_on_page_104056=91; seconds_on_page_104057=91; seconds_on_page_104058=91; _ga=GA1.2.633920870.1743752809; call_s=___t6xj36r8.1743754700.568796021.193685:592575.281015:831755|2___; _ga_D6VNBFBRX6=GS1.1.1743752808.1.1.1743752919.34.0.0; SCBindexAct=1396; sma_index_activity=8503',
}

params = {
    'PAGEN_1': '1',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while params['PAGEN_1'] != '20':


    response = requests.get('https://skolkovoone.ru/catalog/filter/clear/apply/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    flats_soup = soup.find_all('div', class_="item-catalog")
    for i in flats_soup:


        url = ''
        date = datetime.date.today()
        project = 'Skolkovo one'
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
        developer = "Айкон"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        all_tags = ''
        korpus = int(i.find('div', class_= 'params-room').text.split()[1].replace(',',''))
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''

        finish_type = 'Без отделки'
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        if i.find('div', class_='tit-room').text.split()[0] == 'Студия,':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.find('div', class_='tit-room').text.split()[0])
        area = float(i.find('div', class_='square-room').text.replace('м2', '').strip().replace(',','.'))
        price_per_metr = ''
        try:
            old_price = int(''.join(i.find('div', class_= 'price-stock').text.split()[0:3]))
        except:
            old_price = ''

        discount = ''
        price_per_metr_new = ''
        try:
            price_element = i.find('div', class_="price-room action-pr")
            if price_element:
                for stock in price_element.find_all(class_="price-stock"):
                    stock.extract()
                price = int(price_element.get_text(strip=True).replace('i','').replace(' ', ''))

        except:
            price = ''
        section = int(i.find('div', class_= 'params-room').text.split()[3].replace(',',''))
        floor = int(i.find('div', class_= 'params-room').text.split()[-1].replace(',','').split('/')[0])
        flat_number = ''

        print(
            f"{project}, квартира {flat_number}, отделка: {finish_type}, количество комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)



    print('--------------------------------------------------------------------------------')
    if not flats_soup:
        break

    params['PAGEN_1'] = str(int(params['PAGEN_1']) + 1)
    sleep_time = random.uniform(1, 4)
    time.sleep(sleep_time)


df = pd.DataFrame(flats, columns=['Дата обновления',
                              'Название проекта',
                              'на англ',
                              'промзона',
                              'Местоположение',
                              'Метро',
                              'Расстояние до метро, км',
                              'Время до метро, мин',
                              'МЦК/МЦД/БКЛ',
                              'Расстояние до МЦК/МЦД, км',
                              'Время до МЦК/МЦД, мин',
                              'БКЛ',
                              'Расстояние до БКЛ, км',
                              'Время до БКЛ, мин',
                              'статус',
                              'старт',
                              'Комментарий',
                              'Девелопер',
                              'Округ',
                              'Район',
                              'Адрес',
                              'Эскроу',
                              'Корпус',
                              'Конструктив',
                              'Класс',
                              'Срок сдачи',
                              'Старый срок сдачи',
                              'Стадия строительной готовности',
                              'Договор',
                              'Тип помещения',
                              'Отделка',
                              'Кол-во комнат',
                              'Площадь, кв.м',
                              'Цена кв.м, руб.',
                              'Цена лота, руб.',
                              'Скидка,%',
                              'Цена кв.м со ск, руб.',
                              'Цена лота со ск, руб.',
                              'секция',
                              'этаж',
                              'номер'])

current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Айкон"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)