import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

'''
Обновляем куки
'''

cookies = {
    '_ym_uid': '1779879851910342352',
    '_ym_d': '1779879851',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'XSRF-TOKEN': 'eyJpdiI6ImxjZ1B6Vmowc3lUd1RYaDNLT2RtaWc9PSIsInZhbHVlIjoiMEVTTm1meGhMM3ZHN09LUmFtNzBUOFplVGs4TFA1Z3VXOFBWSTEvZHFvU0FCbE1UaFk0THhsZTRnU2F4eG50UUVNNlNqWkhMenRCKzdKSCtEZFhIU2V3NEtZMFRVaDRpdlR1Y2NZc09EQ0FoeGJCekhKUkNYblV5SjlmM3hGU1QiLCJtYWMiOiJkMDQyN2Q3MTE5ZGEyYTk1OTU4ZWRlZjAzMDkwOTllN2FhNmI5YTc2OGIwZDhiYzNlNGNjMGY4OGY2YjRlYTU5IiwidGFnIjoiIn0%3D',
    'aist_session': 'eyJpdiI6IlNKZVpuZWI0WjRTRlI0VmxUNUJoN1E9PSIsInZhbHVlIjoibDZSZ05qNHJDQWVxR1NMdDhHQURnd1FZV0QvWGpKK3lqbTYwSUJhS1krMXh1NGErMkZOL005SGdCUXBwL05tYnN1VlhUWlQ2eHhuOU0rSzVJZEQ1d3NTcnhucS9FUkh5cXdnOW4rR1RWZHlJUXl5MXNHdnl5WlhVNmpOSEtVOSsiLCJtYWMiOiJiODNjMWFkNDYzMjA5YjQ3ODE5YTgxNjA5MGI3ZTQ3MGIyOTljYjNjMTY5NGU3NzAwNWI1OGVlYjA0YzcwOTA2IiwidGFnIjoiIn0%3D',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    # 'content-length': '0',
    'origin': 'https://aist-residence.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://aist-residence.com/ceni-i-planirovki?group_type%5B0%5D=1&group_type%5B1%5D=2&group_type%5B2%5D=3&group_type%5B3%5D=4&page=2',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-csrf-token': 'ogQj13lS5OgCzkOWs7ytkpbTxLVJG13ZP69wMP1x',
    # 'cookie': '_ym_uid=1779879851910342352; _ym_d=1779879851; _ym_isad=2; _ym_visorc=w; XSRF-TOKEN=eyJpdiI6ImxjZ1B6Vmowc3lUd1RYaDNLT2RtaWc9PSIsInZhbHVlIjoiMEVTTm1meGhMM3ZHN09LUmFtNzBUOFplVGs4TFA1Z3VXOFBWSTEvZHFvU0FCbE1UaFk0THhsZTRnU2F4eG50UUVNNlNqWkhMenRCKzdKSCtEZFhIU2V3NEtZMFRVaDRpdlR1Y2NZc09EQ0FoeGJCekhKUkNYblV5SjlmM3hGU1QiLCJtYWMiOiJkMDQyN2Q3MTE5ZGEyYTk1OTU4ZWRlZjAzMDkwOTllN2FhNmI5YTc2OGIwZDhiYzNlNGNjMGY4OGY2YjRlYTU5IiwidGFnIjoiIn0%3D; aist_session=eyJpdiI6IlNKZVpuZWI0WjRTRlI0VmxUNUJoN1E9PSIsInZhbHVlIjoibDZSZ05qNHJDQWVxR1NMdDhHQURnd1FZV0QvWGpKK3lqbTYwSUJhS1krMXh1NGErMkZOL005SGdCUXBwL05tYnN1VlhUWlQ2eHhuOU0rSzVJZEQ1d3NTcnhucS9FUkh5cXdnOW4rR1RWZHlJUXl5MXNHdnl5WlhVNmpOSEtVOSsiLCJtYWMiOiJiODNjMWFkNDYzMjA5YjQ3ODE5YTgxNjA5MGI3ZTQ3MGIyOTljYjNjMTY5NGU3NzAwNWI1OGVlYjA0YzcwOTA2IiwidGFnIjoiIn0%3D',
}

params = {
    'group_type[0]': '1',
    'group_type[1]': '2',
    'group_type[2]': '3',
    'group_type[3]': '4',
    'page': '1',
}

flats = []


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

while True:

    response = requests.post('https://aist-residence.com/api/v1/flats/kvartiry', params=params, cookies=cookies, headers=headers)
    print(response.status_code)
    items = response.json()['data']


    for i in items:

        url = i['link']
        date = datetime.date.today()
        project = "Аист резиденс"
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
        developer = "Монарх"
        okrug = ''
        district = ''
        adress = ''
        eskrou = ''
        korpus = '1'
        konstruktiv = ''
        klass = ''
        srok_sdachi = ''
        srok_sdachi_old = ''
        stadia = ''
        dogovor = ''
        type = 'Апартаменты'
        finish_type = 'Без отделки'
        room_count = i['flat_type']
        area = i["area_total"]
        price_per_metr = ''
        old_price = float(i["price"])
        discount = ''
        price_per_metr_new = ''
        price = ''
        section = ''
        floor = i["floor"]
        flat_number = i['number']

        print(
            f"{project}, {url}, отделка: {finish_type}, тип: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}")
        result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck,
                  distance_to_mck, time_to_mck, distance_to_bkl,
                  time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv,
                  klass, srok_sdachi, srok_sdachi_old,
                  stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount,
                  price_per_metr_new, price, section, floor, flat_number]
        flats.append(result)

    params['page'] = str(int(params['page']) + 1)
    if not items:
        break


save_flats_to_excel(flats, project, developer)