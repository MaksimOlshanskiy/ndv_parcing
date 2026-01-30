from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from selenium import webdriver
import requests
import json

driver = webdriver.Chrome()



cookies = {
    'spid': '1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3',
    '_ym_uid': '1741679472430329696',
    '_ym_d': '1741679472',
    'tmr_lvid': '21dd9990a0516763e1af5efdddfe2ece',
    'tmr_lvidTS': '1741679492626',
    '_ym_isad': '2',
    'domain_sid': 'p9NEOoC7wfYKTfSohYE69%3A1743597502986',
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3745525d5f4f58455e445a4a423660',
    'tmr_detect': '0%7C1743599371818',
    'spsc': '1743603129300_0cb4a77edd3a2899c0fb9888c1ef36d6_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic MTpxd2U=',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?place=0-1156&sortName=objReady100PercDt&sortDirection=desc',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; _ym_d=1741679472; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; _ym_isad=2; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1743597502986; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3745525d5f4f58455e445a4a423660; tmr_detect=0%7C1743599371818; spsc=1743603129300_0cb4a77edd3a2899c0fb9888c1ef36d6_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
}

params = {
    'offset': '0',
    'limit': '20',
    'sortField': 'obj_publ_dt',
    'sortType': 'desc',
    'place': '0-40',
    'objStatus': '0',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

while True:

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={offset_counter}&limit=20&sortField=obj_publ_dt&sortType=desc&residentialBuildings=1&place=0-40&objStatus=0:2'


    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
    data = json.loads(json_text)['data']['list']


    for i in data:

        try:
            is_living = i['buildType']
        except:
            is_living = ''

        try:
            if 'город' in i['objAddr'].lower() or 'г.' in i['objAddr'].lower():
                city = i['objAddr'].split()[1].replace(',', '').capitalize()
            else:
                if 'город' in i['shortAddr'].lower() or 'г.' in i['shortAddr'].lower():
                    city = i['shortAddr'].split()[1].replace(',', '').capitalize()
                else:
                    city = i['shortAddr']
        except:
            city = ''

        try:
            declaration_number = i['rpdNum']
        except:
            declaration_number = ''

        try:
            status = i['siteStatus']
        except:
            status = ''

        try:
            if i['problemFlag'] == 'NONE':
                is_problem = 'Нет'
            else:
                is_problem = 'Да'
        except:
            is_problem = ''

        try:
            adress = i['objAddr']
        except:
            adress = ''

        try:
            id = i['objId']
        except:
            id = ''

        try:
            group = i['developer']['groupName']
        except:
            group = ''

        try:
            floor_max = i['objFloorMax']
        except:
            floor_max = ''

        try:
            floor_min = i['objFloorMin']
        except:
            floor_min = ''

        try:
            price_avg = i['objPriceAVG']
        except:
            price_avg = ''

        try:
            square_living = i['objSquareLiving']
        except:
            square_living = ''

        try:
            developer = i['developer']['fullName'].title()
        except:
            developer = ''

        try:
            project = i['objCommercNm'].title()
        except:
            project = 'Без названия'

        try:
            flats_count = i['objElemLivingCnt']
        except:
            flats_count = ''

        try:
            publish_date = i['objPublDt']
        except:
            publish_date = ''

        try:
            ready_date = i['objReady100PercDt']
        except:
            ready_date = ''
        try:
            metro = i['metro']['name']
            line = i['metro']['line']
            time_to_metro = round(i['metro']['time'])
            if i['metro']['isWalk']:
                is_walk = 'Да'
            else:
                is_walk = 'Нет'

        except:
            metro = ''
            line = ''
            time_to_metro = ''
            is_walk = ''

        try:
            url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/{id}'
        except:
            url = ''


        print(
            f":Город: {city} !! АДРЕС: {adress} !! ЖК: {project} !! ID {id} !! застройщик {developer}, {url}")
        result = [date, city, adress, developer, group, project, id, is_living, status, flats_count, publish_date, ready_date, declaration_number, is_problem, floor_max, floor_min, price_avg, square_living, metro, line, time_to_metro, is_walk, url]
        flats.append(result)

    if not data:
        break
    offset_counter += 20
    print('--------------------------------------------------------------')
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    print(f'Загружено: {len(flats)}')

df = pd.DataFrame(flats, columns=['Дата обновления',
                                  'Город',
                                  'Адрес',
                                  'Застройщик',
                                  'Группа',
                                  'Название проекта',
                                  'id',
                                  'Тип',
                                  'Статус',
                                  'Количество квартир',
                                  'Дата публикации проекта',
                                  'Дата готовности',
                                  'Проектная декларация',
                                  'Есть проблемы',
                                  'Этажность max',
                                  'Этажность min',
                                  'Средняя цена',
                                  'Площадь',
                                  'Станция метро',
                                  'Линия метро',
                                  'Время до метро',
                                  'Пешком или нет',
                                  'Ссылка'
 ])



# Базовый путь для сохранения
base_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\НашДомРФ"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Мо_НашДомРФ_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

список_id = df['id'].tolist()
print(список_id)

