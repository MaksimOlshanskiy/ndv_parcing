import json
from functions import classify_renovation, clean_filename, merge_and_clean, haversine
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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


cookies = {
    '_ym_uid': '1765012936500443323',
    '_ym_d': '1765012936',
    'adtech_uid': 'c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru',
    'ns_session': '6b7f0e11-9d39-4d9f-bde9-e0ea2b194184',
    'RETENTION_COOKIES_NAME': 'c4194f168c4b486394b9e0e579a6ad7c:rcdfFDfvr7s0pTQeRgykGrLqh8M',
    'sessionId': '47f88fa2f01a440f9154dfe2c16bc0ef:kumwnApx1cyy1eyhaY2VD01hj_U',
    'UNIQ_SESSION_ID': '8aebb9c1984c4fdbad9edaf6dc22d362:WPANcUW3wmpwW1wxsCc8-9CCjGk',
    'logoSuffix': '',
    'iosAppLink': '',
    '_sv': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688',
    'top100_id': 't1.7711713.1020003933.1779904305209',
    'tmr_lvid': '6509c7cbd63e89eea195eb14c34fbb17',
    'tmr_lvidTS': '1773855203088',
    'showDddIntro': 'false',
    'dddIntroOnline': 'false',
    'regionAlert': '1',
    'max-chat-settings-show': '%7B%22countOfEntry%22%3A4%2C%22lastStatus%22%3A%22NOT_CREATED%22%7D',
    '_ym_isad': '2',
    'cookieAlert': '1',
    'canary-bind-id-14320': 'next-2',
    'currentRegionGuid': '321b0daa-da95-4ce5-81b3-a7ab62d89d19',
    'currentLocalityGuid': '6369cbfc-1f06-4574-adba-82f4dc42c0f7',
    'regionName': '6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0',
    '_visitId': '272ca817-2835-4c7a-98b1-200325b90f07-6315121d1b510ace',
    'qrator_ssid2': 'v2.0.1780505330.747.5fa9bf1fTzzOGZv1|2Kl3rNsoNcwYfEVW|nZ4PD/GA4Nh4HkZsevPeC3EcVCqcZmAJLszRUQ96WystVJ7uZNIdwkAH+sJcRwSE46Cuy1ow71qizCQCSjPrd3h3LadpNY5V2/oC1SxLRLD3fTD0Wo0AIjh92uxdICeNcVaTO7ppcZA07KUnX58TtSwcv7bDA+rQALaLVMJkqNA=-dV7kJe7XDCNbwyIFH+IyIr2xIwg=',
    'qrator_jsid2': 'v2.0.1780505330.747.5fa9bf1fTzzOGZv1|tvNDw8edYsDLns7Z|V2NMDJD6Zubb+9xvZpnwYFj/dYU6DOBTJFSZSJIazh5DyrksUmDKi2JShNrgWPoHxCfhdCIXba9MNhCx00mweAO9UeECVSfvPwNp74/gDdFyHypiU1zBn+b1ob6YmG//vqF5Qld1lvZaao3PtE4JFomxl8KC9ffFyQrfgDGEZBM=-gKZ/0TveDwB5rr7eXlGyxFfZ6ME=',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%22321b0daa-da95-4ce5-81b3-a7ab62d89d19%22%2C%22localityGuid%22:%226369cbfc-1f06-4574-adba-82f4dc42c0f7%22%2C%22subdomain%22:%22%22}%2C%22isAutoResolved%22:true}',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780516982',
    '_sas': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780516982',
    't3_sid_7711713': 's1.160642329.1780471411515.1780516987585.7.58.6.1..',
    't3_sid_7731951': 's1.21260308.1780471411528.1780516987761.6.194.6.1..',
    'tmr_reqNum': '213',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://samara.domclick.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://samara.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1765012936500443323; _ym_d=1765012936; adtech_uid=c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru; ns_session=6b7f0e11-9d39-4d9f-bde9-e0ea2b194184; RETENTION_COOKIES_NAME=c4194f168c4b486394b9e0e579a6ad7c:rcdfFDfvr7s0pTQeRgykGrLqh8M; sessionId=47f88fa2f01a440f9154dfe2c16bc0ef:kumwnApx1cyy1eyhaY2VD01hj_U; UNIQ_SESSION_ID=8aebb9c1984c4fdbad9edaf6dc22d362:WPANcUW3wmpwW1wxsCc8-9CCjGk; logoSuffix=; iosAppLink=; _sv=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688; top100_id=t1.7711713.1020003933.1779904305209; tmr_lvid=6509c7cbd63e89eea195eb14c34fbb17; tmr_lvidTS=1773855203088; showDddIntro=false; dddIntroOnline=false; regionAlert=1; max-chat-settings-show=%7B%22countOfEntry%22%3A4%2C%22lastStatus%22%3A%22NOT_CREATED%22%7D; _ym_isad=2; cookieAlert=1; canary-bind-id-14320=next-2; currentRegionGuid=321b0daa-da95-4ce5-81b3-a7ab62d89d19; currentLocalityGuid=6369cbfc-1f06-4574-adba-82f4dc42c0f7; regionName=6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0; _visitId=272ca817-2835-4c7a-98b1-200325b90f07-6315121d1b510ace; qrator_ssid2=v2.0.1780505330.747.5fa9bf1fTzzOGZv1|2Kl3rNsoNcwYfEVW|nZ4PD/GA4Nh4HkZsevPeC3EcVCqcZmAJLszRUQ96WystVJ7uZNIdwkAH+sJcRwSE46Cuy1ow71qizCQCSjPrd3h3LadpNY5V2/oC1SxLRLD3fTD0Wo0AIjh92uxdICeNcVaTO7ppcZA07KUnX58TtSwcv7bDA+rQALaLVMJkqNA=-dV7kJe7XDCNbwyIFH+IyIr2xIwg=; qrator_jsid2=v2.0.1780505330.747.5fa9bf1fTzzOGZv1|tvNDw8edYsDLns7Z|V2NMDJD6Zubb+9xvZpnwYFj/dYU6DOBTJFSZSJIazh5DyrksUmDKi2JShNrgWPoHxCfhdCIXba9MNhCx00mweAO9UeECVSfvPwNp74/gDdFyHypiU1zBn+b1ob6YmG//vqF5Qld1lvZaao3PtE4JFomxl8KC9ffFyQrfgDGEZBM=-gKZ/0TveDwB5rr7eXlGyxFfZ6ME=; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%22321b0daa-da95-4ce5-81b3-a7ab62d89d19%22%2C%22localityGuid%22:%226369cbfc-1f06-4574-adba-82f4dc42c0f7%22%2C%22subdomain%22:%22%22}%2C%22isAutoResolved%22:true}; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780516982; _sas=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780516982; t3_sid_7711713=s1.160642329.1780471411515.1780516987585.7.58.6.1..; t3_sid_7731951=s1.21260308.1780471411528.1780516987761.6.194.6.1..; tmr_reqNum=213',
}


with open(r"C:\PycharmProjects\ndv_parcing\Cian\coordinates.json", "r", encoding="utf-8") as f:
    city_centers = json.load(f)

developer = ''
project = ''
area = ''
region = 'Самара'

coords = city_centers.get(region)

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=options)



ids =  [123711, 124413, 124740, 125388, 125444, 121779, 125706]




def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s


# Основной цикл по ID комплексов
for complex_id in ids:
    flats = []
    params = {
        'address': '25a8b02a-a308-4cb2-bbba-b31592b66046',
        'offset': '0',
        'limit': '20',
        'sort': 'qi',
        'sort_dir': 'desc',
        'deal_type': 'sale',
        'category': 'living',
        'offer_type': 'layout',
        'complex_ids': [complex_id],  # Используем текущий ID из списка
        'complex_name': 'ЖК Солнечный город',
        'sort_by_tariff_date': '1',
    }

    print(f"\nНачинаем обработку комплекса с ID: {complex_id}")

    while True:
        response = requests.get('https://bff-search-web.domclick.ru/api/offers/v1', params=params, cookies=cookies,
                                headers=headers)
        print(f"Статус код: {response.status_code}, offset: {params['offset']}")

        try:
            items = response.json()['result']['items']
        except (KeyError, ValueError) as e:
            print(f"Ошибка при обработке ответа: {e}")
            break

        if not items:
            print("Нет данных, завершаем обработку этого комплекса")
            break

        for i in items:
            url = ""
            date = datetime.date.today()
            try:
                project = i['complex']['name'].replace('"', '').replace('ЖК ', '')
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
            eskrou = ''
            korpus = ''
            konstruktiv = ''
            klass = ''
            try:
                quarter = i['complex']['building']['endBuildQuarter']
                year = i['complex']['building']['endBuildYear']
                srok_sdachi = f"{quarter} квартал {year} года"
            except:
                quarter = ''
                year = ''
                srok_sdachi = ''
            srok_sdachi_old = ''
            stadia = ''
            dogovor = ''
            type = 'Квартира' if not i['generalInfo']['isApartment'] else "Апартаменты"
            room_count = i['generalInfo']['rooms']
            area = i['generalInfo']['area']
            price_per_metr = ''
            discount = ''
            price_per_metr_new = ''
            price = int(i["price"])
            old_price = ''
            section = ''
            floor = int(i['generalInfo']['maxFloor'])
            flat_number = ''
            finish_type = ''
            added = ''
            try:
                lat_jk = i['location']['lat']
                lon_jk = i['location']['lon']
                lat_center = coords["lat_center"]
                lon_center = coords["lon_center"]
                distance = round(haversine(lat_jk, lon_jk, lat_center, lon_center), 2)
            except:
                distance = ''
            try:
                geo1 = i['address']['displayName'].split(',')[1].strip()
            except:
                geo1 = ''
            try:
                geo2 = i['address']['displayName'].split(',')[2].strip()
            except:
                geo2 = ''
            try:
                geo3 = i['address']['displayName'].split(',')[3].strip()
            except:
                geo3 = ''
            try:
                geo4 = i['address']['displayName'].split(',')[4].strip()
            except:
                geo4 = ''
            project_class = ''
            location = 'Республика Башкортостан'
            house = ''
            metro = ''
            okrug = ''

            kitchenArea = ''
            livingArea = ''
            parking = ''
            balconies_and_loggias_count = ''

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

                    for item in range(1, len(items2)):

                        y = items2[item]

                        url2 = web_url
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
                        eskrou2 = ''
                        korpus2 = ''
                        konstruktiv2 = ''
                        klass2 = ''
                        quarter2 = ''
                        year2 = ''
                        srok_sdachi_old2 = ''
                        stadia2 = ''
                        dogovor2 = ''
                        finish_type2 = y.find_all('div', class_='yzjlv')[2].get_text().strip()


                        area2 = area
                        price_per_metr2 = ''
                        discount2 = ''
                        price_per_metr_new2 = ''
                        try:
                            price2 = int(y.find(class_='VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', ''))
                        except:
                            price2 = y.find(class_='VkJXv').get_text(strip=True).replace(' ₽', '').replace(' ', '')
                        old_price2 = ''
                        section2 = ''
                        floor2 = int(y.get_text(separator='!').split('!')[1])
                        flat_number2 = ''
                        added2 = ''

                        print(
                            f"Вложенные лоты || {project2}, комнаты: {room_count}, площадь: {area2}, цена: {price2}, этаж: {floor2}, отделка: {finish_type2}")

                        result2 = [project, developer, project_class, location, geo1, okrug, geo2, geo3, metro, geo4,
                                  house, korpus, distance, srok_sdachi, type, finish_type2, room_count, area, '', '', price2, floor2, '', '', url2]

                        flats.append(result2)

                    try:
                        buttons = driver.find_elements(By.CLASS_NAME, "pgnt-control-eeb-4-1-2")
                        next_button = None

                        for btn in buttons:
                            try:
                                btn.find_element(By.CLASS_NAME, "pgnt-next-c9c-4-1-2")
                                next_button = btn
                                break
                            except NoSuchElementException:
                                continue

                        if not next_button:
                            print("Кнопка 'вперёд' не найдена")
                            break

                        if "pgnt-disabled-835-4-1-2" in next_button.get_attribute("class"):
                            print("Кнопка 'вперёд' неактивна, выходим из цикла")
                            break

                        # Попробуем закрыть всплывающее окно cookies, если оно есть
                        try:
                            cookie_alert = driver.find_element(By.CLASS_NAME, "tpln-CookieAlert-spoilerIntro--11-5-1")
                            close_button = cookie_alert.find_element(By.TAG_NAME,
                                                                     "button")  # Или уточни CSS селектор, если другой
                            close_button.click()
                            print("Всплывающее окно закрыто")
                            time.sleep(1)
                        except NoSuchElementException:
                            pass
                        except Exception as ce:
                            print(f"Не удалось закрыть всплывающее окно: {ce}")

                        try:
                            ActionChains(driver).move_to_element(next_button).perform()
                            next_button.click()
                        except ElementClickInterceptedException:
                            # Вдруг не получилось — пробуем через JS
                            print("Перекрыт элемент, пробуем кликнуть через JS")
                            driver.execute_script("arguments[0].click();", next_button)

                        print("Переход на следующую страницу")
                        time.sleep(2)

                    except Exception as e:
                        print(f"Ошибка при переходе на следующую страницу: {e}")
                        break
            try:
                finish_type = finish_type2
            except:
                finish_type = ''
            try:
                url = url2
            except:
                url = ''
            project_class = ''
            location = 'Республика Башкортостан'
            house = ''
            metro = ''
            okrug = ''

            print(
                f"{project}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, этаж: {floor}, отделка: {finish_type}")
            result = [project, developer, project_class, location, geo1, okrug, geo2, geo3, metro, geo4, house, korpus, distance, srok_sdachi, type,
                      finish_type, room_count, area, '', '', price, floor, '', '', url]
            flats.append(result)

        params["offset"] = str(int(params["offset"]) + 20)
        sleep_time = random.uniform(5, 10)
        time.sleep(sleep_time)

        # Сохраняем результаты в Excel
    df = pd.DataFrame(flats, columns=['Название проекта',
                                      'Девелопер',
                                      'Класс',
                                      'Локация',
                                      'Локация2',
                                      'Округ',
                                      'Район',
                                      'Микрорайон',
                                      'Метро',
                                      'Улица',
                                      'Дом',
                                      'Корпус',
                                      'Расстояние до центра, км',
                                      'Срок сдачи',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Площадь кухни, кв.м',
                                      'Жилая площадь, кв.м',
                                      'Цена лота, руб.',
                                      'Этаж',
                                      'Балконы/лоджии',
                                      'Паркинг',
                                      'Ссылка'])

    current_date = datetime.date.today()
    base_path = r""
    folder_path = os.path.join(base_path, str(current_date))

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{region}_{complex_id}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)

    print(f"\nВсе данные успешно сохранены в файл: {file_path}")

# Закрываем драйвер после обработки всех комплексов
driver.quit()
