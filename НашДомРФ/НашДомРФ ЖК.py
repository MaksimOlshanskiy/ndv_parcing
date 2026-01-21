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
    'tmr_lvid': '21dd9990a0516763e1af5efdddfe2ece',
    'tmr_lvidTS': '1741679492626',
    '___dmpkit___': 'a4186694-8f1a-4c72-a444-15171df726ff',
    '_ym_d': '1757920713',
    '_ym_isad': '2',
    'domain_sid': 'p9NEOoC7wfYKTfSohYE69%3A1768224153616',
    '_ym_visorc': 'b',
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3445525d5f4f58455e445a4a423660',
    'spjs': '1768285840218_3a2ed5f2_01350250_a90bc98a36f1963f16038812266246cb_60JjJnaaQV2scUgU9TRwni9c4fPod5/62v5XEfA+fTgIjESBYDWH18ZbE57/OlrHBalBjOdBKfT0+FGS6z6nc6L37srqL4mRwFUdmPkzRDEPo0uG7fuT/v7yW5x1qKENrOFFFEUYX1u68odDwuYOS6NdVLExtR1XWP/mX02wuHE1afENOCQvhtNqAm9qlq5yRcS5uH0sheHERS1P/6yFAAqk3BhpHgXsnADIdZXsxHhL59+mRmpzX6/z2xXwxKxtSf3AtAQljFGpT+egaiSdWVZ7oZ89kQlV5Vxxfo7SChZXboP6X6OU0LUkSSn5qOXRcvOuqg9rZ/Dg9E0X5BmATLikmcUlvBKL7ucKAtfL4y94udTAcERo/IkYEHLnpgl7K8qH4/OnmOTUaNUtfcTsdUb6su7uV2uisksjfb3c8TVGJs6YLisFwAklfZ1JGnCG2FVdUaEp8YxNcEiQky9nG9uH+pCBegzIqZxEoOfAGLlKvneW4lZOSqxrQxkp5v0BAkxV3J1hOqdGSiMeaAQNEPc1DZ2tqbCApgAYL19PF1UWc+puvm7wzOxBqBQFuGFcKMff83Ifki//Qzrw0NWvG6p/xlDC1o3I+X1NExFkjFgn+cOcT2Z8QEVJYb+tEd5ydi3lzUxnIIF2Uh46vOhkhlXU7b5ObCSG9paZQtabpQnK8s41droA/dgH3/KiT/dtiyuxZZVByIiuSME3F2Pc+azKQ7aW4pyBdtv3+BnwjkSh3ueLi3QolCRpQE5Lnwd1IvBv6VktVsKyZg5by/+XAwzQ6NQkKCH9vWFtFeIaEf0bc0v1RBtsmat95xHCw/jMz7sy5lKVb8s6n0b865NoRGXIIZyNQUpGN5pSj9gwjfRXsZit3Hnx2oJm+m8fS/OXcvBaflrUg8MvamsGZjUtVuXRmJZvGRDWDGFoltKXr9s73oYSczYcWGt9R5DrtJxaAMtjr38zC972SGN9/YGZdSTogNx8IBfDo1dvWsqeplHRx2z5aS0E4LB0TCfXi7NvLvL6llY6Ae2dcmgkZGmA3astxxHDpH35OV1lkmIm/vnoLMSQZDVb1694sp76ksxBcr81vSvX/jLwWAYMvPlzc2QQOHw4nGVeEVTNGsiMlEAtUwsXZjsDXqxySJXmuYJdL1CIFGU4C9uv/0IS0ZMe+Ol8lJFAtR7Z+v13H8wzj1cieseea5Je8vesZErstghTI/BOw2svDlKyf04J2L93cOBUGM8/GvTZ/Yed4dCMdS8N1u7ExUoiCurmPoShO0C01QE5bZ3J/coN7eTgaLR9U6d6S5+dO4pUB2yECwv2v2Mz/pJLaxaRBbRQ3juKNoajKuW8SWsz4JLwcErTpTODrCZySzbWu4DcLKFJHOdKgE4iH/O4QxYvugoYoXd38xtICP1k92YjPeGxuWMcbrMihjV54LwpR/4i0r4SH31ZtbEgciv+/nqRwzDQeQwMyEACLXcu8/N/lsxsdq9xcf0VTyiGnPKTHjmJrwoFEfG1vVgrfsISYjYP27w/Rw19t83AAKz13VpxGseiHnTvuUOKUyTCPM6YPcTW4UINCvsvpZRWougu/34GqflXP9RG3/QICUde1m0xAM8tdEf8E4WtXQytlaEREF6a2v4GM3aHj3uhrfAMPLBc5aBpxE77l9pHrTjTPOwgF8OzZ18K/psW8YB1xZFpJQzQuHVEFuf1Ay+Oc8uWxrrJ1a0+husbSPhcA//nG2s/BtorlkcQIT2NQSD87JDoNI/YWItyPs8yi/d16dGNfTEYxLR4QAvrv4dTIvbOmmo8BcUHBc8JybwMWCf7ypZp1qv+//kkTmWYoF2k+MCcZTkCVdX/1p4tv847iT1JWvyophjpcaj33rEOVAaaQo9uI4nGBStDHu62nFxzssBrfp+mUqN2T5nrvYfRJtRsRmKEd57/c0tSwDaNynj5pJntt9PpfHBMB6W16fst38MSNB1KHFt8z42jwcKgGOwQ==',
    'spsc': '1768286904257_e72e5e4d2346d243180736df6d7c34f9_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ',
    'tmr_detect': '0%7C1768286908922',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic MTpxd2U=',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8/%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81-%D0%BA%D0%BB%D0%B0%D1%81%D1%81%D0%B0/%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0/?objClass=0%3A2%3A3%3A4',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; ___dmpkit___=a4186694-8f1a-4c72-a444-15171df726ff; _ym_d=1757920713; _ym_isad=2; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1768224153616; _ym_visorc=b; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3445525d5f4f58455e445a4a423660; spjs=1768285840218_3a2ed5f2_01350250_a90bc98a36f1963f16038812266246cb_60JjJnaaQV2scUgU9TRwni9c4fPod5/62v5XEfA+fTgIjESBYDWH18ZbE57/OlrHBalBjOdBKfT0+FGS6z6nc6L37srqL4mRwFUdmPkzRDEPo0uG7fuT/v7yW5x1qKENrOFFFEUYX1u68odDwuYOS6NdVLExtR1XWP/mX02wuHE1afENOCQvhtNqAm9qlq5yRcS5uH0sheHERS1P/6yFAAqk3BhpHgXsnADIdZXsxHhL59+mRmpzX6/z2xXwxKxtSf3AtAQljFGpT+egaiSdWVZ7oZ89kQlV5Vxxfo7SChZXboP6X6OU0LUkSSn5qOXRcvOuqg9rZ/Dg9E0X5BmATLikmcUlvBKL7ucKAtfL4y94udTAcERo/IkYEHLnpgl7K8qH4/OnmOTUaNUtfcTsdUb6su7uV2uisksjfb3c8TVGJs6YLisFwAklfZ1JGnCG2FVdUaEp8YxNcEiQky9nG9uH+pCBegzIqZxEoOfAGLlKvneW4lZOSqxrQxkp5v0BAkxV3J1hOqdGSiMeaAQNEPc1DZ2tqbCApgAYL19PF1UWc+puvm7wzOxBqBQFuGFcKMff83Ifki//Qzrw0NWvG6p/xlDC1o3I+X1NExFkjFgn+cOcT2Z8QEVJYb+tEd5ydi3lzUxnIIF2Uh46vOhkhlXU7b5ObCSG9paZQtabpQnK8s41droA/dgH3/KiT/dtiyuxZZVByIiuSME3F2Pc+azKQ7aW4pyBdtv3+BnwjkSh3ueLi3QolCRpQE5Lnwd1IvBv6VktVsKyZg5by/+XAwzQ6NQkKCH9vWFtFeIaEf0bc0v1RBtsmat95xHCw/jMz7sy5lKVb8s6n0b865NoRGXIIZyNQUpGN5pSj9gwjfRXsZit3Hnx2oJm+m8fS/OXcvBaflrUg8MvamsGZjUtVuXRmJZvGRDWDGFoltKXr9s73oYSczYcWGt9R5DrtJxaAMtjr38zC972SGN9/YGZdSTogNx8IBfDo1dvWsqeplHRx2z5aS0E4LB0TCfXi7NvLvL6llY6Ae2dcmgkZGmA3astxxHDpH35OV1lkmIm/vnoLMSQZDVb1694sp76ksxBcr81vSvX/jLwWAYMvPlzc2QQOHw4nGVeEVTNGsiMlEAtUwsXZjsDXqxySJXmuYJdL1CIFGU4C9uv/0IS0ZMe+Ol8lJFAtR7Z+v13H8wzj1cieseea5Je8vesZErstghTI/BOw2svDlKyf04J2L93cOBUGM8/GvTZ/Yed4dCMdS8N1u7ExUoiCurmPoShO0C01QE5bZ3J/coN7eTgaLR9U6d6S5+dO4pUB2yECwv2v2Mz/pJLaxaRBbRQ3juKNoajKuW8SWsz4JLwcErTpTODrCZySzbWu4DcLKFJHOdKgE4iH/O4QxYvugoYoXd38xtICP1k92YjPeGxuWMcbrMihjV54LwpR/4i0r4SH31ZtbEgciv+/nqRwzDQeQwMyEACLXcu8/N/lsxsdq9xcf0VTyiGnPKTHjmJrwoFEfG1vVgrfsISYjYP27w/Rw19t83AAKz13VpxGseiHnTvuUOKUyTCPM6YPcTW4UINCvsvpZRWougu/34GqflXP9RG3/QICUde1m0xAM8tdEf8E4WtXQytlaEREF6a2v4GM3aHj3uhrfAMPLBc5aBpxE77l9pHrTjTPOwgF8OzZ18K/psW8YB1xZFpJQzQuHVEFuf1Ay+Oc8uWxrrJ1a0+husbSPhcA//nG2s/BtorlkcQIT2NQSD87JDoNI/YWItyPs8yi/d16dGNfTEYxLR4QAvrv4dTIvbOmmo8BcUHBc8JybwMWCf7ypZp1qv+//kkTmWYoF2k+MCcZTkCVdX/1p4tv847iT1JWvyophjpcaj33rEOVAaaQo9uI4nGBStDHu62nFxzssBrfp+mUqN2T5nrvYfRJtRsRmKEd57/c0tSwDaNynj5pJntt9PpfHBMB6W16fst38MSNB1KHFt8z42jwcKgGOwQ==; spsc=1768286904257_e72e5e4d2346d243180736df6d7c34f9_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ; tmr_detect=0%7C1768286908922',
}

params = {
    'offset': '0',
    'limit': '20',
    'sortField': 'obj_publ_dt',
    'sortType': 'desc',
    'objClass': '4',
    'place': '0-1',
}




flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

while True:

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={offset_counter}&limit=20&sortField=obj_publ_dt&sortType=desc&place=0-1&objClass=3'


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
            id = i['developer']['devId']
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


