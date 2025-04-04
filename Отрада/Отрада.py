import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup


import requests

cookies = {
    'PHPSESSID': '9cr22ji8hqfo3hq52l9uglegip',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2025-04-03%2015%3A33%3A53%7C%7C%7Cep%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fprojects%2Fnk%2Fflat%2Fsearch-by-parameters%3Ffilter%255BdealStatuses%255D%255B%255D%3Ddeveloper%26filter%255Btrim%255D%3D3%26viewMode%3Drow%26sort%3Dcost%26direction%3Dasc%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
    'sbjs_first_add': 'fd%3D2025-04-03%2015%3A33%3A53%7C%7C%7Cep%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fprojects%2Fnk%2Fflat%2Fsearch-by-parameters%3Ffilter%255BdealStatuses%255D%255B%255D%3Ddeveloper%26filter%255Btrim%255D%3D3%26viewMode%3Drow%26sort%3Dcost%26direction%3Dasc%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
    'sbjs_current': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_first': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Safari%2F537.36',
    'RFB_SESSION': 'uav2t7hmc1efdv7m59b0sgverm',
    'tmr_lvid': 'b936993bad02ecb0a996703ecd6dde2a',
    'tmr_lvidTS': '1743683633569',
    '_ym_uid': '1743683634614672601',
    '_ym_d': '1743683634',
    'scbsid_old': '2746015342',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    '_cmg_csstOBSxq': '1743683635',
    '_comagic_idOBSxq': '9252605382.13197045532.1743683635',
    'domain_sid': 'Fvr9jiN311CH4r3TKwhYe%3A1743683635360',
    'sma_session_id': '2248247076',
    'SCBfrom': 'https%3A%2F%2Fwww.google.com%2F',
    'SCBnotShow': '-1',
    'smFpId_old_values': '%5B%22b0d44eece823d71c253568fc397e79de%22%5D',
    'SCBstart': '1743683637871',
    'SCBporogAct': '5000',
    'sma_postview_ready': '1',
    'SCBFormsAlreadyPulled': 'true',
    'sbjs_session': 'pgs%3D6%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fflats',
    'kvartaly3NpageChangeCounter': '3',
    'kvartaly3NlastVisitedPage': 'https://kvartaly-otrada.ru/flats',
    'tmr_detect': '0%7C1743683649818',
    'SCBindexAct': '3623',
    'sma_index_activity': '11065',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://kvartaly-otrada.ru/flats?filter%5Bavailable%5D=1&viewMode=tile&sort=cost&direction=asc',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'PHPSESSID=9cr22ji8hqfo3hq52l9uglegip; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-04-03%2015%3A33%3A53%7C%7C%7Cep%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fprojects%2Fnk%2Fflat%2Fsearch-by-parameters%3Ffilter%255BdealStatuses%255D%255B%255D%3Ddeveloper%26filter%255Btrim%255D%3D3%26viewMode%3Drow%26sort%3Dcost%26direction%3Dasc%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_first_add=fd%3D2025-04-03%2015%3A33%3A53%7C%7C%7Cep%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fprojects%2Fnk%2Fflat%2Fsearch-by-parameters%3Ffilter%255BdealStatuses%255D%255B%255D%3Ddeveloper%26filter%255Btrim%255D%3D3%26viewMode%3Drow%26sort%3Dcost%26direction%3Dasc%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F; sbjs_current=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Safari%2F537.36; RFB_SESSION=uav2t7hmc1efdv7m59b0sgverm; tmr_lvid=b936993bad02ecb0a996703ecd6dde2a; tmr_lvidTS=1743683633569; _ym_uid=1743683634614672601; _ym_d=1743683634; scbsid_old=2746015342; _ym_isad=2; _ym_visorc=w; _cmg_csstOBSxq=1743683635; _comagic_idOBSxq=9252605382.13197045532.1743683635; domain_sid=Fvr9jiN311CH4r3TKwhYe%3A1743683635360; sma_session_id=2248247076; SCBfrom=https%3A%2F%2Fwww.google.com%2F; SCBnotShow=-1; smFpId_old_values=%5B%22b0d44eece823d71c253568fc397e79de%22%5D; SCBstart=1743683637871; SCBporogAct=5000; sma_postview_ready=1; SCBFormsAlreadyPulled=true; sbjs_session=pgs%3D6%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fkvartaly-otrada.ru%2Fflats; kvartaly3NpageChangeCounter=3; kvartaly3NlastVisitedPage=https://kvartaly-otrada.ru/flats; tmr_detect=0%7C1743683649818; SCBindexAct=3623; sma_index_activity=11065',
}

params = {
    'filter[available]': '1',
    'viewMode': 'tile',
    'page': '1',
    'sort': 'cost',
    'direction': 'asc',
}




flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


while True:

    flats_start = len(flats)
    response = requests.get('https://kvartaly-otrada.ru/flats', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    flats_soup = soup.find_all('div', class_="flat-tile__wrapper")
    for i in flats_soup:

        if i.find('div', class_='banner-card swiper-container'):
            continue  # Пропускаем итерацию, если такой элемент найден
        elif i.find('span', class_= 'flat-tile__seller').text == 'От физ. лица':
            flats_start -= 1
            continue  # Пропускаем итерацию, если такой элемент найден
        flat_params = i.find('div', class_= 'flat-tile__additional').find_all('div', class_= 'flat-tile__info-part')

        url = ''

        date = datetime.date.today()
        project = i.find('span', class_= 'flat-tile__project').text.strip()

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
        developer = "Отрада Девелопмент"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        all_tags = ''
        korpus = flat_params[2].text.replace('Корпус', '').strip()
        konstruktiv = ''
        klass = ''
        srok_sdachi = flat_params[3].text.replace('Корпус', '').strip()

        try:
            if i.find('a', {'data-info': 'Квартира без отделки'}):
                finish_type = 'Без отделки'
            elif i.find('a', {'data-info': 'Отделка White Box'}):
                finish_type = 'Предчистовая отделка'
        except:
            finish_type = ''

        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Квартиры'
        if i.find('div', class_='flat-tile__type').text.split()[1] == 'Студия':
            room_count = 0
        elif i.find('div', class_='flat-tile__type').text.split()[1] == 'Комнат':
            room_count = i.find('div', class_='flat-tile__type').text.split()[2]
        area = float(flat_params[0].text.replace(' м2', '').replace('Площадь', '').replace(',','.').strip())
        price_per_metr = ''
        try:
            old_price = int(i.find('span', class_= 'flat-tile__cost-old').text.replace(' ₽', '').replace(' ', '').replace('от', '').strip())
        except:
            old_price = ''

        discount = ''
        price_per_metr_new = ''
        price = int(i.find('span', class_= 'flat-tile__cost').text.replace(' ₽', '').replace(' ', '').replace('от', '').strip())
        section = ''
        floor = int(flat_params[1].text.replace('Этаж', '').strip())
        flat_number = i.find('div', class_='flat-tile__type').text.split()[0].replace('№', '').replace(',', '')

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
    if len(flats)-flats_start != 15:
        break


    print('--------------------------------------------------------------------------------')

    params['page'] = str(int(params['page']) + 1)
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
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Отрада"

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{developer}_{current_date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)