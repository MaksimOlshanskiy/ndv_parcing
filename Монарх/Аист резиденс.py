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
    '_ym_uid': '174358513932310668',
    '_ym_d': '1769438650',
    'XSRF-TOKEN': 'eyJpdiI6ImNHWWtEOWMwRFFna2dTdXlPU2FxM2c9PSIsInZhbHVlIjoiRmErbXgwaEh2Nm01alJRc1RkK1hHNWh1RWQrY3RyNnY0ZGdUZTZoRGhYS05ncjkveEdWQ2FSeFpEaEFXeUJkRkhWTUtLYUcvZVNuRWNROGFwUFQrK2pteVhLK25WWUpnMEFaUUZ5eVlIbFpHS29XS3FleWR1YlhIam1mekJjUGkiLCJtYWMiOiIzZGZhNTY2ODIzNDgzMmM0ZDQyZTRjYWJmMzM5MDgzOTc1NGQ4NTMwYWYwYTAxZjhkNDRlMWY4OGEwMmJiZTBjIiwidGFnIjoiIn0%3D',
    'aist_session': 'eyJpdiI6InJXT2NvMWpLYVcxNFZpdThTMlIrZHc9PSIsInZhbHVlIjoiMTkxZVA2eklkdktaLzJKSHdISDJHcnRTeno3QXV0M2ZzUzdCYlNSZ0c4SUpMNThVRXJrNnl3SkIxL2pVc1Y2ZVlLTHNXWHkzenBZbnVVSjUyanVYVXM2U2FpWlBlOVI3VnExcmRVc1VGbHM1NzM0OHpVRVZGc3l6d0pkOXJzMWgiLCJtYWMiOiJmNWYwNDZiZjVkNzRmODE5MzljNGQ3M2ZkMTkxOTRhYWI0NzI0NjQwZDkyM2IxZGEzYTFlOWY3ZGNkYzJkNWEwIiwidGFnIjoiIn0%3D',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    # 'content-length': '0',
    'origin': 'https://aist-residence.com',
    'priority': 'u=1, i',
    'referer': 'https://aist-residence.com/ceni-i-planirovki?group_type%5B0%5D=1&group_type%5B1%5D=2&group_type%5B2%5D=3&group_type%5B3%5D=4&page=2',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'x-csrf-token': 'lGqeHb4n3IW8J7qxkI5m7YgCYIxf78loE4lUAWq9',
    # 'cookie': '_ym_uid=174358513932310668; _ym_d=1769438650; XSRF-TOKEN=eyJpdiI6ImNHWWtEOWMwRFFna2dTdXlPU2FxM2c9PSIsInZhbHVlIjoiRmErbXgwaEh2Nm01alJRc1RkK1hHNWh1RWQrY3RyNnY0ZGdUZTZoRGhYS05ncjkveEdWQ2FSeFpEaEFXeUJkRkhWTUtLYUcvZVNuRWNROGFwUFQrK2pteVhLK25WWUpnMEFaUUZ5eVlIbFpHS29XS3FleWR1YlhIam1mekJjUGkiLCJtYWMiOiIzZGZhNTY2ODIzNDgzMmM0ZDQyZTRjYWJmMzM5MDgzOTc1NGQ4NTMwYWYwYTAxZjhkNDRlMWY4OGEwMmJiZTBjIiwidGFnIjoiIn0%3D; aist_session=eyJpdiI6InJXT2NvMWpLYVcxNFZpdThTMlIrZHc9PSIsInZhbHVlIjoiMTkxZVA2eklkdktaLzJKSHdISDJHcnRTeno3QXV0M2ZzUzdCYlNSZ0c4SUpMNThVRXJrNnl3SkIxL2pVc1Y2ZVlLTHNXWHkzenBZbnVVSjUyanVYVXM2U2FpWlBlOVI3VnExcmRVc1VGbHM1NzM0OHpVRVZGc3l6d0pkOXJzMWgiLCJtYWMiOiJmNWYwNDZiZjVkNzRmODE5MzljNGQ3M2ZkMTkxOTRhYWI0NzI0NjQwZDkyM2IxZGEzYTFlOWY3ZGNkYzJkNWEwIiwidGFnIjoiIn0%3D; _ym_isad=2; _ym_visorc=w',
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