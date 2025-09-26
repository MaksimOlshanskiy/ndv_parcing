"""

глазами смотреть количество страниц и проставлять в коде, иначе будут дубли!!!!!!!!!!!!!!!

"""

import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
import requests

cookies = {
    'roistat_is_need_listen_requests': '0',
    'roistat_is_save_data_in_cookie': '1',
    'SCBFormsAlreadyPulled': 'true',
    'PHPSESSID': 'LsiULCoW5ByXvVF8YLpG0HulCq3wmmQI',
    '_ym_uid': '1743415929559311987',
    '_ym_d': '1758876784',
    'scbsid_old': '2746015342',
    'roistat_visit': '274388',
    'roistat_visit_cookie_expire': '1209600',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1758931140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '___dc': 'a754551e-265e-4d6b-9f95-8a533f4aa9bc',
    'roistat_call_tracking': '1',
    'roistat_emailtracking_email': 'null',
    'roistat_emailtracking_tracking_email': 'null',
    'roistat_emailtracking_emails': 'null',
    'roistat_cookies_to_resave': 'roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails',
    'sma_session_id': '2439137776',
    'SCBfrom': '',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%222488b0e958469f2da6c6193c8be92e7e%22%5D',
    'SCBporogAct': '5000',
    'SCBstart': '1758876789394',
    'sma_postview_ready': '1',
    'screen_width': '1416',
    'SCBindexAct': '4397',
    'sma_index_activity': '10850',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'bx-ajax': 'true',
    'priority': 'u=1, i',
    'referer': 'https://1-ng.ru/catalog/?catalogFilter_96_MIN=19.3&catalogFilter_96_MAX=69.5&catalogFilter_96_MIN=19267776&catalogFilter_96_MAX=69492597&catalogFilter_83_MIN=3&catalogFilter_83_MAX=28&catalogFilter_83_MIN=3&catalogFilter_83_MAX=28&catalogFilter_69_MIN=29&catalogFilter_69_MAX=113&catalogFilter_69_MIN=29.48&catalogFilter_69_MAX=113.48&catalogFilter_92_270784970=Y&set_filter=Y',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    # 'cookie': 'roistat_is_need_listen_requests=0; roistat_is_save_data_in_cookie=1; SCBFormsAlreadyPulled=true; PHPSESSID=LsiULCoW5ByXvVF8YLpG0HulCq3wmmQI; _ym_uid=1743415929559311987; _ym_d=1758876784; scbsid_old=2746015342; roistat_visit=274388; roistat_visit_cookie_expire=1209600; _ym_isad=2; _ym_visorc=w; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1758931140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; ___dc=a754551e-265e-4d6b-9f95-8a533f4aa9bc; roistat_call_tracking=1; roistat_emailtracking_email=null; roistat_emailtracking_tracking_email=null; roistat_emailtracking_emails=null; roistat_cookies_to_resave=roistat_ab%2Croistat_ab_submit%2Croistat_visit%2Croistat_call_tracking%2Croistat_emailtracking_email%2Croistat_emailtracking_tracking_email%2Croistat_emailtracking_emails; sma_session_id=2439137776; SCBfrom=; SCBnotShow=-1; smFpId_old_values=%5B%222488b0e958469f2da6c6193c8be92e7e%22%5D; SCBporogAct=5000; SCBstart=1758876789394; sma_postview_ready=1; screen_width=1416; SCBindexAct=4397; sma_index_activity=10850',
}

params = {
    'PAGEN_1': '1',
}
# catalogFilter_92=124380902



flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:


    response = requests.get('https://1-ng.ru/catalog/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.text
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('tr')
    counter = 1
    for i in flats_soup:
        if counter == 1:
            counter += 1
            continue
        if i.text.split() == []:
            continue
        # print(i.text.split())

        flats2 = i.find_all('td')


        url = ''

        date = datetime.date.today()
        project = "Первый Нагатинский"

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
        developer = "Прайм Лайф"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        try:
            korpus = '1'
        except ValueError:
            korpus = '1'
        konstruktiv = ''
        klass = ''
        finish_type = ''
        srok_sdachi = ''

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        if i.text.split()[0] == 'С':
            room_count = 0
        else:
            room_count = extract_digits_or_original(i.text.split()[0])
        area = extract_digits_or_original(i.text.split()[7])
        price_per_metr = ''
        try:
            old_price = int(i.find(class_= 'catalog__price_old').find(class_= 'catalog__price_max').text.replace('₽', '').replace(' ', ''))
        except:
            old_price = ''
        discount = ''
        price_per_metr_new = ''
        if len(i.text.split()) == 15:
            price = int(''.join(i.text.split()[11:14]).replace('₽', ''))
        else:
            price = int(''.join(i.text.split()[-4:-1]).replace('₽', ''))
        section = ''
        floor = int(i.text.split()[3])
        flat_number = int(extract_digits_or_original(i.text.split()[6]))

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
    params['PAGEN_1'] = str(int(params['PAGEN_1']) + 1)
    if params['PAGEN_1'] == '2':
        break
    if not flats_soup:
        break

    print('--------------------------------------------------------------------------------')

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

params = {
    'set_filter': 'y',
    'catalogFilter_92': '270784970',
    'PAGEN_1': '1',
}

flats_with_finishing = []
while True:
    params = {
        'PAGEN_1': '1',
    }
    response = requests.get('https://1-ng.ru/catalog/', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.text
    soup = BeautifulSoup(items, 'html.parser')
    flats_soup = soup.find_all('tr')
    counter = 1

    for i in flats_soup:
        if counter == 1:
            counter += 1
            continue
        if i.text.split() == []:
            continue
        # print(i.text.split())

        flats2 = i.find_all('td')

        flat_number = int(extract_digits_or_original(i.text.split()[6]))
        flats_with_finishing.append(flat_number)
    params['PAGEN_1'] = str(int(params['PAGEN_1']) + 1)
    if params['PAGEN_1'] == '1':
        break


def set_finish(df, список_номеров, значение_есть='Предчистовая', значение_нет='Без отделки'):
    """
    Обновляет столбец 'Отделка' в датафрейме df:
    - если 'номер' есть в списке_номеров — устанавливается значение_есть
    - если 'номер' нет в списке — устанавливается значение_нет

    Параметры:
        df (pd.DataFrame): исходный датафрейм
        список_номеров (list): список номеров квартир
        значение_есть (str): значение, если номер найден (по умолчанию 'Предчистовая')
        значение_нет (str): значение, если номер не найден (по умолчанию 'Без отделки')

    Возвращает:
        pd.DataFrame: обновлённый датафрейм
    """
    if 'номер' not in df.columns:
        raise ValueError("В датафрейме нет столбца 'номер'")

    # Убедимся, что столбец 'Отделка' существует
    if 'Отделка' not in df.columns:
        df['Отделка'] = None

    # Проставляем значения в зависимости от наличия номера в списке
    df['Отделка'] = df['номер'].apply(lambda x: значение_есть if x in список_номеров else значение_нет)

    return df

df = set_finish(df, flats_with_finishing)


current_date = datetime.date.today()

# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{project}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)