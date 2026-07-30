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

month = '01'



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
    'sortField': 'default',
    'sortType': 'desc',
    'objClass': '2',
    'place': '77',
    'fromQuarter': '2025-01-01',
    'toQuarter': '2025-30-06',
    'objStatus': '0',
}





flats = []
date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/portal-analytics/api/launch/areas/rnv?calculationType=SQUARE&repYear=2025&repMonth={month}&objClassCd=2&size=1000'  # status=0 - строящиеся. status=0:2 строящиеся и сданные


driver.get(url=url)
page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
data = json.loads(json_text)['values']


for i in data:
    print(i)
    month = f'01.01.2025'
    name = i['name']
    value = i['value']



    print(
        f"{month}, {name}, {value}")
    result = [month, name, value]
    flats.append(result)



df = pd.DataFrame(flats)



# Базовый путь для сохранения
base_path = r"C:\PycharmProjects\ndv_parcing\НашДомРФ"

folder_path = os.path.join(base_path, str(date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"{month}_{date}.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

# Сохранение файла в папку
df.to_excel(file_path, index=False)

