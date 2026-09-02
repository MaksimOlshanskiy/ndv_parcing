"""
Сначала обновляем куки
Затем меняем в params - complex_ids на нужный
Его можно найти в адресной строке нужного ЖК

Обращать внимание на код кнопки вперёд. Он иногда меняется.
"""



import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from functions import save_flats_to_excel

developer = ''
project = ''
area = ''

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

cookies = {
    'ns_session': '8d885eed-c151-4167-9919-8657ec697ffe',
    '_ym_uid': '1765012936500443323',
    '_ym_d': '1782939022',
    'logoSuffix': '',
    'iosAppLink': '',
    'showDddWidgets': 'true',
    'RETENTION_COOKIES_NAME': '73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc',
    'sessionId': '12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70',
    'UNIQ_SESSION_ID': 'd58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8',
    'adtech_uid': 'c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru',
    'top100_id': 't1.7711713.584217383.1782939023617',
    'tmr_lvid': '6509c7cbd63e89eea195eb14c34fbb17',
    'tmr_lvidTS': '1773855203088',
    'regionAlert': '1',
    'auto-definition-region': 'false',
    'cookieAlert': '1',
    '_sa': 'SA1.5921084b-375c-4426-927c-9703572e4456.1785766215',
    'favoriteHintShowed': 'true',
    'showDddIntro': 'false',
    'dddIntroOnline': 'false',
    'canary-bind-id-17692': 'next-1',
    'canary-bind-id-17501': 'next-2',
    'currentRegionGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'currentLocalityGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'regionName': '1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    '_sv': 'SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008',
    't3_sid_7711713': 's1.1990022496.1787784108050.1787785750606.8.10.1.1...1',
    't3_sid_7731951': 's1.1174137006.1787784108296.1787785750609.7.20.1.1...1',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22%2C%22localityGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    '_ym_isad': '2',
    'qrator_jsr': 'v2.0.1787907266.547.05e47254I8PCmkiz|31OYRReNagFdOxd1|VnRBQMXhkdakmhe735tgnrxGDz0SLoPLz4uxEOCNURJe0wVaWsstiSLwSWwMFm+DHILpH5pJSPGQkvOjkYfcig==-2NhtxYZFV6M3xjsRNI4YhSJ/bVk=-00',
    'qrator_jsid2': 'v2.0.1787907266.547.05e47254I8PCmkiz|u33uLwqqwZan7Evv|65HQ6Qp4UcaRiugoMoDFZFqs7PANtx8J0bfyqkzwo5bGyWpMZFe4wyhQnBJzoNytCprBrL+jaXL3VsGo3pUQA8NDjxjoqYNME/L394hpSERGzgNl1cfTjQel/JLxhauKU3DB4D/4uqoSyMLRpqMfWySrRMYuF4Ki0lrxUEVi2+E=-2DHSnjxZAq40xI6Y573mAAKNQPo=',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008.1787907269',
    '_sas': 'SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008.1787907269',
    'tmr_reqNum': '615',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=8d885eed-c151-4167-9919-8657ec697ffe; _ym_uid=1765012936500443323; _ym_d=1782939022; logoSuffix=; iosAppLink=; showDddWidgets=true; RETENTION_COOKIES_NAME=73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc; sessionId=12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70; UNIQ_SESSION_ID=d58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8; adtech_uid=c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru; top100_id=t1.7711713.584217383.1782939023617; tmr_lvid=6509c7cbd63e89eea195eb14c34fbb17; tmr_lvidTS=1773855203088; regionAlert=1; auto-definition-region=false; cookieAlert=1; _sa=SA1.5921084b-375c-4426-927c-9703572e4456.1785766215; favoriteHintShowed=true; showDddIntro=false; dddIntroOnline=false; canary-bind-id-17692=next-1; canary-bind-id-17501=next-2; currentRegionGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; currentLocalityGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; regionName=1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; _sv=SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008; t3_sid_7711713=s1.1990022496.1787784108050.1787785750606.8.10.1.1...1; t3_sid_7731951=s1.1174137006.1787784108296.1787785750609.7.20.1.1...1; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22%2C%22localityGuid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; _ym_isad=2; qrator_jsr=v2.0.1787907266.547.05e47254I8PCmkiz|31OYRReNagFdOxd1|VnRBQMXhkdakmhe735tgnrxGDz0SLoPLz4uxEOCNURJe0wVaWsstiSLwSWwMFm+DHILpH5pJSPGQkvOjkYfcig==-2NhtxYZFV6M3xjsRNI4YhSJ/bVk=-00; qrator_jsid2=v2.0.1787907266.547.05e47254I8PCmkiz|u33uLwqqwZan7Evv|65HQ6Qp4UcaRiugoMoDFZFqs7PANtx8J0bfyqkzwo5bGyWpMZFe4wyhQnBJzoNytCprBrL+jaXL3VsGo3pUQA8NDjxjoqYNME/L394hpSERGzgNl1cfTjQel/JLxhauKU3DB4D/4uqoSyMLRpqMfWySrRMYuF4Ki0lrxUEVi2+E=-2DHSnjxZAq40xI6Y573mAAKNQPo=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008.1787907269; _sas=SV1.0674628e-5915-4077-9240-71884d0582cb.1782939008.1787907269; tmr_reqNum=615',
}


params = {
    'address': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'layout',
    'complex_ids': '78930',
    'complex_name': 'ЖК Радость',
    'from_developer': '1',
    'offset': '0'
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.json()['result']['items']

    for i in items:

        url = ""
        date = datetime.date.today()
        try:
            project = i['complex']['name']
        except:
            continue
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
        developer = i['developerName']
        okrug = ''
        district = ''
        adress = i['address']['displayName']
        eskrou = ''
        korpus = ''
        konstruktiv = ''
        klass = ''
        try:
            quarter = i['complex']['building']['endBuildQuarter']
            year = i['complex']['building']['endBuildYear']
        except:
            quarter = ''
            year = ''
        srok_sdachi = f"{quarter} квартал {year} года"
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        if i['generalInfo']['isApartment'] == False:
            type = 'Квартиры'
        else:
            type = "Апартаменты"
        room_count = i['generalInfo']['rooms']
        area = i['generalInfo']['area']
        price_per_metr = ''
        discount = ''
        price_per_metr_new = ''
        price = ''
        old_price = int(i["price"])
        section = ''
        floor = int(i['generalInfo']['maxFloor'])
        flat_number = ''



        if i['developerOffersCount'] > 1:

            web_url = i['path']
            print(web_url)

            driver.get(web_url)
            for name, value in cookies.items():
                cookie_dict = {
                    'name': name,
                    'value': value
                }
                driver.add_cookie(cookie_dict)

            driver.get(web_url)
            time.sleep(4)
            while True:

                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')
                items2 = soup.find_all(class_='rYs9s')

                for item in range(1,len(items2)):

                    y = items2[item]


                    url2 = ""
                    date2 = datetime.date.today()
                    project2 = project
                    english2 = ''
                    promzona2 = ''
                    mestopolozhenie2 = ''
                    subway2 = ''
                    distance_to_subway2 = ''
                    time_to_subway2 = ''
                    mck2 = ''
                    distance_to_mck2 = ''
                    time_to_mck2 = ''
                    bkl2 = ''
                    distance_to_bkl2 = ''
                    time_to_bkl2 = ''
                    status2 = ''
                    start2 = ''
                    comment2 = ''
                    developer2 = developer
                    okrug2 = ''
                    district2 = ''
                    adress2 = adress
                    eskrou2 = ''
                    try:
                        korpus2 = soup.find('span', class_= 'dUBJV').text.replace('Корпус: ', '').replace('Корпус ', '').replace('№', '').strip()
                    except:
                        korpus2 = ''
                    konstruktiv2 = ''
                    klass2 = ''
                    quarter2 = ''
                    year2 = ''
                    srok_sdachi2 = srok_sdachi
                    srok_sdachi_old2 = ''
                    stadia2 = ''
                    dogovor2 = ''
                    type2 = type
                    finish_type2 = y.get_text(separator='!').split('!')[4]
                    room_count2 = room_count
                    area2 = area
                    price_per_metr2 = ''
                    discount2 = ''
                    price_per_metr_new2 = ''
                    price2 = ''
                    old_price2 = int(y.find(class_= 'GC1lx').get_text(strip=True).replace(' ₽', '').replace(' ', '').replace('Новое', ''))
                    section2 = ''
                    floor2 = int(y.get_text(separator='!').split('!')[1])
                    flat_number2 = '' # y.find(class_= 'T8vBE').get_text(strip=True)

                    print(
                        f"{developer}, {project2}, {url2}, дата: {date2}, комнаты: {room_count2}, площадь: {area2}, цена: {price2}, старая цена: {old_price2}, корпус: {korpus2}, этаж: {floor2}")
                    result2 = [date2, project2, english2, promzona2, mestopolozhenie2, subway2, distance_to_subway2, time_to_subway2,
                              mck2,
                              distance_to_mck2, time_to_mck2, distance_to_bkl2,
                              time_to_bkl2, bkl2, status2, start2, comment2, developer2, okrug2, district2, adress2, eskrou2, korpus2,
                              konstruktiv2, klass2, srok_sdachi2, srok_sdachi_old2,
                              stadia2, dogovor2, type2, finish_type2, room_count2, area2, price_per_metr2, old_price2, discount2,
                              price_per_metr_new2, price2, section2, floor2, flat_number2]
                    flats.append(result2)

                try:
                    # Получаем все кнопки с нужным классом
                    buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-4-1-2")
                    next_button = None

                    for btn in buttons:
                        try:
                            # Проверяем, есть ли у кнопки div с нужным вложенным классом
                            btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-4-1-2")
                            next_button = btn
                            break  # нашли нужную кнопку — дальше не ищем
                        except NoSuchElementException:
                            continue

                    if not next_button:
                        print("Кнопка 'вперёд' не найдена")
                        break

                    # Проверяем, не отключена ли она
                    if "pgnt-disabled-835-4-1-2" in next_button.get_attribute("class"):
                        print("Кнопка 'вперёд' неактивна, выходим из цикла")
                        break

                    ActionChains(driver).move_to_element(next_button).perform()
                    next_button.click()
                    print("Переход на следующую страницу")
                    time.sleep(2)

                except Exception as e:
                    print(f"Ошибка при переходе на следующую страницу: {e}")
                    break

        try:
            finish_type = finish_type2
        except:
            finish_type = ''

        print(
            f"{developer}, {project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus,
                  konstruktiv, klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)








    params["offset"] = str(int(params["offset"]) + 20)
    sleep_time = random.uniform(5, 10)
    time.sleep(sleep_time)
    if not items:
        print("Всё скачано. Переходим к загрузке в файл")
        driver.quit()
        break



save_flats_to_excel(flats, project, developer)
