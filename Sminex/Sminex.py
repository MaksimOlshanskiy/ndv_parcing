import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random

from functions import save_flats_to_excel

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.sminex.com',
    'priority': 'u=1, i',
    'referer': 'https://www.sminex.com/',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
}


json_data = {
    'query': 'query{pick(filter:{project:[],building:[],floor:[],flat:[{field:"ТипНедвижимости", oneOf:["Жилая"]}{field:"СостояниеПродажи",oneOf:["Забронировано","Экспонирование"]}]}order:{fields:[{entity:"flat",field:"ЦенаЭкспонированияСоСкидкой",desc:true}]}pagination:{after:""first:2000}){quantity,connection{pageInfo{endCursor,hasNextPage,hasPreviousPage}nodes{project{attributes(fields:["Наименование"]){name,value}},building{attributes(fields:["Наименование","Стадия","НомерСтроения"]){name,value}},flat{flatId,attributes(fields:["Наименование","ПрофильСайт","КоличествоКомнат","Типоразмер","ОсновнойЭтаж","Площадь","Цена*","СостояниеПродажи","КоличествоУровней","НомерСекции","ТипКухни","ВыходОкон","СтороныСвета","Код","КодыСвязанныхПомещений"]){name,value},planes{link,level,bedrooms,planOrder,planType}}}}}}',
}



flats = []

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s



response = requests.post('https://apikey.sminex.com/', headers=headers, json=json_data)
print(response.status_code)

items = response.json()['data']['pick']['connection']['nodes']

for i in items:

    attributes = i['flat']['attributes']
    attrs_dict = {item['name']: item['value'] for item in attributes}
    building = i['building']['attributes']
    build_dict = {item['name']: item['value'] for item in building}

    url = ""

    date = datetime.date.today()
    project = i['project']['attributes'][0]['value']
    english = ''
    promzona = ''
    mestopolozhenie = ''
    subway = ''
    distance_to_subway = ''
    time_to_subway = ''
    finish_type = 'Без отделки'
    mck = ''
    distance_to_mck = ''
    time_to_mck = ''
    bkl = ''
    distance_to_bkl = ''
    time_to_bkl = ''
    status = ''
    start = ''
    comment = ''
    developer = "Sminex"
    okrug = ''
    district = ''
    adress = ''
    eskrou = ''
    try:
        korpus = build_dict.get('Наименование').lower().capitalize()
        if 'Sky' in korpus:
            project = 'RiverSky'
    except:
        korpus = ''
    if project == 'Достижение':
        korpus = '1'
    if project == 'Тишинский бульвар':
        korpus = build_dict.get('НомерСтроения')

    konstruktiv = ''
    klass = ''
    srok_sdachi = ''
    srok_sdachi_old = ''
    stadia = ''
    dogovor = ''
    type = attrs_dict.get('ПрофильСайт')
    room_count = attrs_dict.get('КоличествоКомнат')
    area = float(attrs_dict.get('Площадь'))
    price_per_metr = ''
    old_price = float(attrs_dict.get('ЦенаЭкспонированияСоСкидкой'))
    discount = ''
    price_per_metr_new = ''
    price = float(attrs_dict.get('ЦенаЭкспонированияСоСкидкой'))
    section = ''
    floor = attrs_dict.get('ОсновнойЭтаж')
    flat_number = ''


    print(
        f"{project}, {url}, дата: {date}, комнаты: {room_count}, площадь: {area}, цена: {price}, старая цена: {old_price}, корпус: {korpus}, этаж: {floor}, {finish_type}")
    result = [date, project, english, promzona, mestopolozhenie, subway, distance_to_subway, time_to_subway, mck, distance_to_mck, time_to_mck, distance_to_bkl,
          time_to_bkl, bkl, status, start, comment, developer, okrug, district, adress, eskrou, korpus, konstruktiv, klass, srok_sdachi, srok_sdachi_old,
          stadia, dogovor, type, finish_type, room_count, area, price_per_metr, old_price, discount, price_per_metr_new, price, section, floor, flat_number]
    flats.append(result)


save_flats_to_excel(flats, project, developer)