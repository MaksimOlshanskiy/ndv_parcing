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
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3445525d5f4f58455e445a4a423660',
    'spjs': '1768285840218_3a2ed5f2_01350250_a90bc98a36f1963f16038812266246cb_60JjJnaaQV2scUgU9TRwni9c4fPod5/62v5XEfA+fTgIjESBYDWH18ZbE57/OlrHBalBjOdBKfT0+FGS6z6nc6L37srqL4mRwFUdmPkzRDEPo0uG7fuT/v7yW5x1qKENrOFFFEUYX1u68odDwuYOS6NdVLExtR1XWP/mX02wuHE1afENOCQvhtNqAm9qlq5yRcS5uH0sheHERS1P/6yFAAqk3BhpHgXsnADIdZXsxHhL59+mRmpzX6/z2xXwxKxtSf3AtAQljFGpT+egaiSdWVZ7oZ89kQlV5Vxxfo7SChZXboP6X6OU0LUkSSn5qOXRcvOuqg9rZ/Dg9E0X5BmATLikmcUlvBKL7ucKAtfL4y94udTAcERo/IkYEHLnpgl7K8qH4/OnmOTUaNUtfcTsdUb6su7uV2uisksjfb3c8TVGJs6YLisFwAklfZ1JGnCG2FVdUaEp8YxNcEiQky9nG9uH+pCBegzIqZxEoOfAGLlKvneW4lZOSqxrQxkp5v0BAkxV3J1hOqdGSiMeaAQNEPc1DZ2tqbCApgAYL19PF1UWc+puvm7wzOxBqBQFuGFcKMff83Ifki//Qzrw0NWvG6p/xlDC1o3I+X1NExFkjFgn+cOcT2Z8QEVJYb+tEd5ydi3lzUxnIIF2Uh46vOhkhlXU7b5ObCSG9paZQtabpQnK8s41droA/dgH3/KiT/dtiyuxZZVByIiuSME3F2Pc+azKQ7aW4pyBdtv3+BnwjkSh3ueLi3QolCRpQE5Lnwd1IvBv6VktVsKyZg5by/+XAwzQ6NQkKCH9vWFtFeIaEf0bc0v1RBtsmat95xHCw/jMz7sy5lKVb8s6n0b865NoRGXIIZyNQUpGN5pSj9gwjfRXsZit3Hnx2oJm+m8fS/OXcvBaflrUg8MvamsGZjUtVuXRmJZvGRDWDGFoltKXr9s73oYSczYcWGt9R5DrtJxaAMtjr38zC972SGN9/YGZdSTogNx8IBfDo1dvWsqeplHRx2z5aS0E4LB0TCfXi7NvLvL6llY6Ae2dcmgkZGmA3astxxHDpH35OV1lkmIm/vnoLMSQZDVb1694sp76ksxBcr81vSvX/jLwWAYMvPlzc2QQOHw4nGVeEVTNGsiMlEAtUwsXZjsDXqxySJXmuYJdL1CIFGU4C9uv/0IS0ZMe+Ol8lJFAtR7Z+v13H8wzj1cieseea5Je8vesZErstghTI/BOw2svDlKyf04J2L93cOBUGM8/GvTZ/Yed4dCMdS8N1u7ExUoiCurmPoShO0C01QE5bZ3J/coN7eTgaLR9U6d6S5+dO4pUB2yECwv2v2Mz/pJLaxaRBbRQ3juKNoajKuW8SWsz4JLwcErTpTODrCZySzbWu4DcLKFJHOdKgE4iH/O4QxYvugoYoXd38xtICP1k92YjPeGxuWMcbrMihjV54LwpR/4i0r4SH31ZtbEgciv+/nqRwzDQeQwMyEACLXcu8/N/lsxsdq9xcf0VTyiGnPKTHjmJrwoFEfG1vVgrfsISYjYP27w/Rw19t83AAKz13VpxGseiHnTvuUOKUyTCPM6YPcTW4UINCvsvpZRWougu/34GqflXP9RG3/QICUde1m0xAM8tdEf8E4WtXQytlaEREF6a2v4GM3aHj3uhrfAMPLBc5aBpxE77l9pHrTjTPOwgF8OzZ18K/psW8YB1xZFpJQzQuHVEFuf1Ay+Oc8uWxrrJ1a0+husbSPhcA//nG2s/BtorlkcQIT2NQSD87JDoNI/YWItyPs8yi/d16dGNfTEYxLR4QAvrv4dTIvbOmmo8BcUHBc8JybwMWCf7ypZp1qv+//kkTmWYoF2k+MCcZTkCVdX/1p4tv847iT1JWvyophjpcaj33rEOVAaaQo9uI4nGBStDHu62nFxzssBrfp+mUqN2T5nrvYfRJtRsRmKEd57/c0tSwDaNynj5pJntt9PpfHBMB6W16fst38MSNB1KHFt8z42jwcKgGOwQ==',
    'spsc': '1768292133244_c7269b2857ee846dbcede3c045a90814_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ',
    '_ym_visorc': 'b',
    'tmr_detect': '0%7C1768292137767',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%B5%D0%B4%D0%B8%D0%BD%D1%8B%D0%B9-%D1%80%D0%B5%D0%B5%D1%81%D1%82%D1%80-%D0%B7%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%89%D0%B8%D0%BA%D0%BE%D0%B2?regionHD=77',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; ___dmpkit___=a4186694-8f1a-4c72-a444-15171df726ff; _ym_d=1757920713; _ym_isad=2; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1768224153616; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3445525d5f4f58455e445a4a423660; spjs=1768285840218_3a2ed5f2_01350250_a90bc98a36f1963f16038812266246cb_60JjJnaaQV2scUgU9TRwni9c4fPod5/62v5XEfA+fTgIjESBYDWH18ZbE57/OlrHBalBjOdBKfT0+FGS6z6nc6L37srqL4mRwFUdmPkzRDEPo0uG7fuT/v7yW5x1qKENrOFFFEUYX1u68odDwuYOS6NdVLExtR1XWP/mX02wuHE1afENOCQvhtNqAm9qlq5yRcS5uH0sheHERS1P/6yFAAqk3BhpHgXsnADIdZXsxHhL59+mRmpzX6/z2xXwxKxtSf3AtAQljFGpT+egaiSdWVZ7oZ89kQlV5Vxxfo7SChZXboP6X6OU0LUkSSn5qOXRcvOuqg9rZ/Dg9E0X5BmATLikmcUlvBKL7ucKAtfL4y94udTAcERo/IkYEHLnpgl7K8qH4/OnmOTUaNUtfcTsdUb6su7uV2uisksjfb3c8TVGJs6YLisFwAklfZ1JGnCG2FVdUaEp8YxNcEiQky9nG9uH+pCBegzIqZxEoOfAGLlKvneW4lZOSqxrQxkp5v0BAkxV3J1hOqdGSiMeaAQNEPc1DZ2tqbCApgAYL19PF1UWc+puvm7wzOxBqBQFuGFcKMff83Ifki//Qzrw0NWvG6p/xlDC1o3I+X1NExFkjFgn+cOcT2Z8QEVJYb+tEd5ydi3lzUxnIIF2Uh46vOhkhlXU7b5ObCSG9paZQtabpQnK8s41droA/dgH3/KiT/dtiyuxZZVByIiuSME3F2Pc+azKQ7aW4pyBdtv3+BnwjkSh3ueLi3QolCRpQE5Lnwd1IvBv6VktVsKyZg5by/+XAwzQ6NQkKCH9vWFtFeIaEf0bc0v1RBtsmat95xHCw/jMz7sy5lKVb8s6n0b865NoRGXIIZyNQUpGN5pSj9gwjfRXsZit3Hnx2oJm+m8fS/OXcvBaflrUg8MvamsGZjUtVuXRmJZvGRDWDGFoltKXr9s73oYSczYcWGt9R5DrtJxaAMtjr38zC972SGN9/YGZdSTogNx8IBfDo1dvWsqeplHRx2z5aS0E4LB0TCfXi7NvLvL6llY6Ae2dcmgkZGmA3astxxHDpH35OV1lkmIm/vnoLMSQZDVb1694sp76ksxBcr81vSvX/jLwWAYMvPlzc2QQOHw4nGVeEVTNGsiMlEAtUwsXZjsDXqxySJXmuYJdL1CIFGU4C9uv/0IS0ZMe+Ol8lJFAtR7Z+v13H8wzj1cieseea5Je8vesZErstghTI/BOw2svDlKyf04J2L93cOBUGM8/GvTZ/Yed4dCMdS8N1u7ExUoiCurmPoShO0C01QE5bZ3J/coN7eTgaLR9U6d6S5+dO4pUB2yECwv2v2Mz/pJLaxaRBbRQ3juKNoajKuW8SWsz4JLwcErTpTODrCZySzbWu4DcLKFJHOdKgE4iH/O4QxYvugoYoXd38xtICP1k92YjPeGxuWMcbrMihjV54LwpR/4i0r4SH31ZtbEgciv+/nqRwzDQeQwMyEACLXcu8/N/lsxsdq9xcf0VTyiGnPKTHjmJrwoFEfG1vVgrfsISYjYP27w/Rw19t83AAKz13VpxGseiHnTvuUOKUyTCPM6YPcTW4UINCvsvpZRWougu/34GqflXP9RG3/QICUde1m0xAM8tdEf8E4WtXQytlaEREF6a2v4GM3aHj3uhrfAMPLBc5aBpxE77l9pHrTjTPOwgF8OzZ18K/psW8YB1xZFpJQzQuHVEFuf1Ay+Oc8uWxrrJ1a0+husbSPhcA//nG2s/BtorlkcQIT2NQSD87JDoNI/YWItyPs8yi/d16dGNfTEYxLR4QAvrv4dTIvbOmmo8BcUHBc8JybwMWCf7ypZp1qv+//kkTmWYoF2k+MCcZTkCVdX/1p4tv847iT1JWvyophjpcaj33rEOVAaaQo9uI4nGBStDHu62nFxzssBrfp+mUqN2T5nrvYfRJtRsRmKEd57/c0tSwDaNynj5pJntt9PpfHBMB6W16fst38MSNB1KHFt8z42jwcKgGOwQ==; spsc=1768292133244_c7269b2857ee846dbcede3c045a90814_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ; _ym_visorc=b; tmr_detect=0%7C1768292137767',
}

params = {
    'offset': '0',
    'limit': '10',
    'sortField': 'devShortNm',
    'sortType': 'asc',
    'regionHd': '77',
    'objStatus': '0',
}




flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

while True:

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/erz/main/filter?offset={offset_counter}&limit=10&sortField=devShortNm&sortType=asc&regionHd=77&objStatus=0'

    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
    data = json.loads(json_text)['data']['developers']


    for i in data:
        devId = i['devId']
        try:
            companyGroupId = i['companyGroupId']
        except:
            companyGroupId = ''
        try:
            devEmail = i['devEmail']
        except:
            devEmail = ''
        try:
            devEmplMainFullNm = i['devEmplMainFullNm']
        except:
            devEmplMainFullNm = ''
        try:
            devFactAddr = i['devFactAddr']
        except:
            devFactAddr = ''
        try:
            devFullCleanNm = i['devFullCleanNm']
        except:
            devFullCleanNm = ''
        try:
            devInn = i['devInn']
        except:
            devInn = ''
        try:
            devKpp = i['devKpp']
        except:
            devKpp = ''
        try:
            devLegalAddr = i['devLegalAddr']
        except:
            devLegalAddr = ''
        try:
            devOgrn = i['devOgrn']
        except:
            devOgrn = ''
        try:
            devPhoneNum = i['devPhoneNum']
        except:
            devPhoneNum = ''
        try:
            devSite = i['devSite']
        except:
            devSite = ''
        try:
            regRegionDesc = i['regRegionDesc']
        except:
            regRegionDesc = ''








        print(            f":id: {devId} !! АДРЕС: {devFactAddr} !! Тел: {devPhoneNum}")
        result = [devId, companyGroupId, devEmail, devEmplMainFullNm, devFactAddr, devFullCleanNm, devInn, devKpp, devLegalAddr, devOgrn, devPhoneNum, devSite, regRegionDesc]
        flats.append(result)

    if not data:
        break
    offset_counter += 10
    print('--------------------------------------------------------------')
    sleep_time = random.uniform(1, 3)
    time.sleep(sleep_time)
    print(f'Загружено: {len(flats)}')



df = pd.DataFrame(flats, columns=['id',
                                  'companyGroupId',
                                  'devEmail',
                                  'devEmplMainFullNm',
                                  'devFactAddr',
                                  'devFullCleanNm',
                                  'devInn',
                                  'devKpp',
                                  'devLegalAddr',
                                  'devOgrn',
                                  'devPhoneNum',
                                  'devSite',
                                  'regRegionDesc'
 ])

# Базовый путь для сохранения
base_path = r"/НашДомРФ"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"Мо_НашДомРФ_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)


