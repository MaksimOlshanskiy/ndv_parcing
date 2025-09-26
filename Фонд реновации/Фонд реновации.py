import re

import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions import save_flats_to_excel

cookies = {
    '_ym_uid': '1741704527208317206',
    '_ym_d': '1741704527',
    '_gcl_au': '1.1.1245713787.1741704527',
    'first_page': 'https://moskva.brusnika.ru/',
    'mindboxDeviceUUID': 'b8b42419-45ee-4a92-8e84-640b5c64455a',
    'directCrm-session': '%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D',
    '_ym_isad': '2',
    'tmr_lvid': 'b5f477cfd95ff112adb7c4909fd8b842',
    'tmr_lvidTS': '1741704526810',
    '_ym_visorc': 'w',
    '_sp_ses.bc95': '*',
    'carrotquest_device_guid': 'a675fcfe-592f-49ed-9de5-0444babef649',
    'carrotquest_uid': '1925995266536636982',
    'carrotquest_auth_token': 'user.1925995266536636982.51753-776395ac10b7ee9e1ccd2b8213.e4e438f0ab4b1165cdf7c4ab4a45ee3457f9a3f8b6b963ee',
    'adrdel': '1741704527622',
    'adrdel': '1741704527622',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'carrotquest_jwt_access': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDE3MDgxMjcsImlhdCI6MTc0MTcwNDUyNywianRpIjoiM2Q0NGRhZjc4NzIwNDA1YTk2MGVkN2U0NDA4NjRkZjUiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0MTcwNDUyNywicm9sZXMiOlsidXNlci4kYXBwX2lkOjUxNzUzLiR1c2VyX2lkOjE5MjU5OTUyNjY1MzY2MzY5ODIiXSwiYXBwX2lkIjo1MTc1MywidXNlcl9pZCI6MTkyNTk5NTI2NjUzNjYzNjk4Mn0.VmtMgmL_jImucOugN4N4eNGU7eqzUwFoo66hZzB3FgE',
    'carrotquest_realtime_services_transport': 'wss',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741790927646%2C%22sl%22%3A%7B%22224%22%3A1741704527646%2C%221228%22%3A1741704527646%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741790927646%2C%22sl%22%3A%7B%22224%22%3A1741704527646%2C%221228%22%3A1741704527646%7D%7D',
    'domain_sid': 'dKkPpB82TTD5_qPO2ZCdd%3A1741704527879',
    '_cmg_csstGarz8': '1741704528',
    '_comagic_idGarz8': '10382395014.14492551284.1741704527',
    'undefined': '11.208',
    'csrftoken': 'hNW6L0c65Yc7AY61h8n0Xc8AM12kcehD',
    'pageviewCount': '2',
    'carrotquest_session': 'rx1jc418b7865q8yzbd6vy9oz2jxxedx',
    '_sp_id.bc95': '2d9f8250-dd73-4b6a-94b5-3862570cea74.1741704527.1.1741704540..2dc897f5-4201-466c-9e68-77e5ee5d8d0b..34fe220c-92e6-4ddc-9886-2e5f8e8886d6.1741704526962.2',
    'sessionid': 'o6k7cgtpz74xgrs6wijt56mwmbsd59qy',
    'carrotquest_session_started': '1',
    'tmr_detect': '0%7C1741704542715',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://moskva.brusnika.ru/flat/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1741704527208317206; _ym_d=1741704527; _gcl_au=1.1.1245713787.1741704527; first_page=https://moskva.brusnika.ru/; mindboxDeviceUUID=b8b42419-45ee-4a92-8e84-640b5c64455a; directCrm-session=%7B%22deviceGuid%22%3A%22b8b42419-45ee-4a92-8e84-640b5c64455a%22%7D; _ym_isad=2; tmr_lvid=b5f477cfd95ff112adb7c4909fd8b842; tmr_lvidTS=1741704526810; _ym_visorc=w; _sp_ses.bc95=*; carrotquest_device_guid=a675fcfe-592f-49ed-9de5-0444babef649; carrotquest_uid=1925995266536636982; carrotquest_auth_token=user.1925995266536636982.51753-776395ac10b7ee9e1ccd2b8213.e4e438f0ab4b1165cdf7c4ab4a45ee3457f9a3f8b6b963ee; adrdel=1741704527622; adrdel=1741704527622; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NDE3MDgxMjcsImlhdCI6MTc0MTcwNDUyNywianRpIjoiM2Q0NGRhZjc4NzIwNDA1YTk2MGVkN2U0NDA4NjRkZjUiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTc0MTcwNDUyNywicm9sZXMiOlsidXNlci4kYXBwX2lkOjUxNzUzLiR1c2VyX2lkOjE5MjU5OTUyNjY1MzY2MzY5ODIiXSwiYXBwX2lkIjo1MTc1MywidXNlcl9pZCI6MTkyNTk5NTI2NjUzNjYzNjk4Mn0.VmtMgmL_jImucOugN4N4eNGU7eqzUwFoo66hZzB3FgE; carrotquest_realtime_services_transport=wss; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741790927646%2C%22sl%22%3A%7B%22224%22%3A1741704527646%2C%221228%22%3A1741704527646%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1741790927646%2C%22sl%22%3A%7B%22224%22%3A1741704527646%2C%221228%22%3A1741704527646%7D%7D; domain_sid=dKkPpB82TTD5_qPO2ZCdd%3A1741704527879; _cmg_csstGarz8=1741704528; _comagic_idGarz8=10382395014.14492551284.1741704527; undefined=11.208; csrftoken=hNW6L0c65Yc7AY61h8n0Xc8AM12kcehD; pageviewCount=2; carrotquest_session=rx1jc418b7865q8yzbd6vy9oz2jxxedx; _sp_id.bc95=2d9f8250-dd73-4b6a-94b5-3862570cea74.1741704527.1.1741704540..2dc897f5-4201-466c-9e68-77e5ee5d8d0b..34fe220c-92e6-4ddc-9886-2e5f8e8886d6.1741704526962.2; sessionid=o6k7cgtpz74xgrs6wijt56mwmbsd59qy; carrotquest_session_started=1; tmr_detect=0%7C1741704542715',
}

flats = []
date = datetime.now().date()
driver = webdriver.Chrome()
page_counter = 1

def extract_korpus(address):
    match = re.search(r'к\.\s*[\w\d,\s]+', address)
    return match.group(0) if match else None

def remove_korpus(address):
    return re.sub(r',?\s*к\.\s*[\w\d,\s]+', '', address).strip()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

url = 'https://xn--80aae5aibotfo5h.xn--p1ai/kvartiry/'

driver.get(url=url)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[4]/div[5]/div[2]/div/div[2]/span/span'))  # Или другой локатор
)
button.click()
time.sleep(5)


page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
soup = BeautifulSoup(page_content, 'html.parser')
flats_soup = soup.select('div.bf_list_in>div.bf_list_r')


for i in flats_soup:

    url = ''
    developer = "Фонд реновации"
    project = remove_korpus(i.select_one('.bf_list_info > div.-name a').text.strip())
    korpus = extract_korpus(i.select_one('.bf_list_info > div.-name a').text.strip())
    if korpus is None:
        korpus = '1'
    else:
        korpus = korpus.replace('к.', '')

    type = 'Квартиры'
    try:
        finish_type = i.select_one('div.bf_list_tags > div > div:nth-of-type(2)').text
    except AttributeError:
        finish_type = ''
    room_count = extract_digits_or_original(i.select_one('div.-params span').text)

    area = float(i.select_one('div.-params > span:nth-of-type(2)').text.replace(' м2', ''))
    old_price = int(i.select_one('div.bf_list_price > div.-price').text.replace(' ', '').replace('₽', ''))
    price = ''
    section = ''
    floor = ''
    flat_number = ''
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
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    price_per_metr = ''
    discount = ''
    price_per_metr_new = ''



    print(
        f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, отделка: {finish_type} ")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
              time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
              stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)


save_flats_to_excel(flats, project, developer)

