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
    'ns_session': '5210b38b-2a77-4df9-a428-6405b3065d3d',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'RETENTION_COOKIES_NAME': 'd7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI',
    'sessionId': 'be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE',
    'UNIQ_SESSION_ID': '01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs',
    'adtech_uid': '5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru',
    'top100_id': 't1.7711713.1405137252.1743518288740',
    '_ym_uid': '1743518289666663600',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '6b6b440680155a4ac17ccaf6a462f603',
    'tmr_lvidTS': '1743518291170',
    'regionAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING': 'true',
    'cookieAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING': 'true',
    '_ym_d': '1759300554',
    'adrdel': '1759300555210',
    'logoSuffix': '',
    'iosAppLink': '',
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'currentRegionGuid': '1691f4a5-8e87-41ab-b0d3-05a0c7a07c76',
    'currentLocalityGuid': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'regionName': '857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0',
    'favoriteHintShowed': 'true',
    'qrator_ssid2': 'v2.0.1773844449.834.96f16094TbVtmlBo|hnqZYolOmgMdf602|TrX67NCXAoDBf9QTJ31+0Pb3lVb5kFh6w+oHfN2X2+ju3wj8VNuqIC5g0cj8qhYuEkHQ/YSLcytPuUyLUQakaur8ZcBuqo3JIIoRx9WbFn8=-VOEv2bvcKQs7ILfZ1pR6fGgi9Es=',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1773844455',
    '_ym_isad': '2',
    '_visitId': '5e6ccc41-d711-48fb-b72d-9e6c1210e007-f4f0dcc432ac8ba6',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1773844462',
    'qrator_jsr': 'v2.0.1773844446.577.96f16094YkjzUH30|dZDGLQ2SULDujN5v|x5GhC5aSWOX6NGDwVCE5WBDFWnFCat+a+eRcfagyxyjtSQaMttTBO7WCsirctDNrUPjVJZJ7rHGbcnbhaQeLk4B/bH3903t/jB0KMc6INRjDZfNe2zK+zF1JPJ/KiPttwE0hAHfXo7JHYsbvqCTa1qt5NCpBUE30ynlzzBEKOMDqFZ6d4HyzY6DVR1c8Riwf-nRQZ7IwUg9AZPotZ3CKHi2iL94o=-00',
    'qrator_jsid2': 'v2.0.1773844446.577.96f16094YkjzUH30|jdRagcM4Ziok6aLA|FUx1+9bRrJNte4xpB8r5xtFgF2l46CIUxiHsWFlquZLfpgS8ivj9VTnCXNSfcOCcyidnv17xOsUBx5CSwODBXo4R2kXv5ogGoG+RrbU7OBJBqV1dtYlMgE5H2SqJxHh5vBSOjsMsEFkUKxDn3dr+BDEKdDphDvYx+yELABXDRVlFXZy8AFFIbqNH33EBtwS6-BY8pTek43YJmWOZR2sk7Vd4pcR8=',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22%2C%22subdomain%22:%22%22}%2C%22isAutoResolved%22:true}',
    'tmr_reqNum': '296',
    't3_sid_7711713': 's1.1969432551.1773844455874.1773845150031.62.43.6.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://ufa.domclick.ru',
    'Referer': 'https://ufa.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING=true; _ym_d=1759300554; adrdel=1759300555210; logoSuffix=; iosAppLink=; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; currentRegionGuid=1691f4a5-8e87-41ab-b0d3-05a0c7a07c76; currentLocalityGuid=857c0a08-7dc0-445e-a044-ed2f6d435a7b; regionName=857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0; favoriteHintShowed=true; qrator_ssid2=v2.0.1773844449.834.96f16094TbVtmlBo|hnqZYolOmgMdf602|TrX67NCXAoDBf9QTJ31+0Pb3lVb5kFh6w+oHfN2X2+ju3wj8VNuqIC5g0cj8qhYuEkHQ/YSLcytPuUyLUQakaur8ZcBuqo3JIIoRx9WbFn8=-VOEv2bvcKQs7ILfZ1pR6fGgi9Es=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1773844455; _ym_isad=2; _visitId=5e6ccc41-d711-48fb-b72d-9e6c1210e007-f4f0dcc432ac8ba6; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1773844462; qrator_jsr=v2.0.1773844446.577.96f16094YkjzUH30|dZDGLQ2SULDujN5v|x5GhC5aSWOX6NGDwVCE5WBDFWnFCat+a+eRcfagyxyjtSQaMttTBO7WCsirctDNrUPjVJZJ7rHGbcnbhaQeLk4B/bH3903t/jB0KMc6INRjDZfNe2zK+zF1JPJ/KiPttwE0hAHfXo7JHYsbvqCTa1qt5NCpBUE30ynlzzBEKOMDqFZ6d4HyzY6DVR1c8Riwf-nRQZ7IwUg9AZPotZ3CKHi2iL94o=-00; qrator_jsid2=v2.0.1773844446.577.96f16094YkjzUH30|jdRagcM4Ziok6aLA|FUx1+9bRrJNte4xpB8r5xtFgF2l46CIUxiHsWFlquZLfpgS8ivj9VTnCXNSfcOCcyidnv17xOsUBx5CSwODBXo4R2kXv5ogGoG+RrbU7OBJBqV1dtYlMgE5H2SqJxHh5vBSOjsMsEFkUKxDn3dr+BDEKdDphDvYx+yELABXDRVlFXZy8AFFIbqNH33EBtwS6-BY8pTek43YJmWOZR2sk7Vd4pcR8=; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22%2C%22subdomain%22:%22%22}%2C%22isAutoResolved%22:true}; tmr_reqNum=296; t3_sid_7711713=s1.1969432551.1773844455874.1773845150031.62.43.6.1..',
}

params = {
    'address': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'offset': '0',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'layout',
    'complex_ids': '122606',
    'complex_name': 'ЖК "Большевик"',
    'from_developer': '1',
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
        project = i['complex']['name']
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
                items2 = soup.find_all(class_='tHj6o')

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
                        korpus2 = soup.find('span', class_= 'Is5nd').text.replace('Корпус: ', '').replace('Корпус ', '').replace('№', '').strip()
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
                    old_price2 = int(y.find(class_= 'VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', '').replace('Новое', ''))
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
                    buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-4-0-1")
                    next_button = None

                    for btn in buttons:
                        try:
                            # Проверяем, есть ли у кнопки div с нужным вложенным классом
                            btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-4-0-1")
                            next_button = btn
                            break  # нашли нужную кнопку — дальше не ищем
                        except NoSuchElementException:
                            continue

                    if not next_button:
                        print("Кнопка 'вперёд' не найдена")
                        break

                    # Проверяем, не отключена ли она
                    if "pgnt-disabled-835-4-0-1" in next_button.get_attribute("class"):
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
