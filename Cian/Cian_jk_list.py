import numpy
import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, clean_filename

json_data = {
    'jsonQuery': {
        'region': {
            'type': 'terms',
            'value': [
                4593,
            ],
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'newbuilding_class': {
            'type': 'terms',
            'value': [
                'comfort',
            ],
        },
    },
    'uri': '/newobjects/list?class%5B0%5D=4104&deal_type=sale&engine_version=2&from_developer=1&offer_type=newobject&region=4593&p=2',
    'subdomain': 'www',
    'offset': 0,
    'count': 25,
    'userCanUseHiddenBase': False,
}

def list_of_ids_maker(region, cookies, headers, json_data):


    building_classes_dict = {}
    building_classes = ['comfort', 'economy', 'premium', 'business']
    ids = []

    cookies = cookies
    headers = headers
    json_data = json_data

    json_data['jsonQuery']['region']['value'] = region

    json_data['offset'] = 0

    for building_class in building_classes:
        print(len(ids))
        print(len(building_classes_dict))
        print(f"Текущий building_class: {building_class}")
        json_data['jsonQuery']['newbuilding_class']['value'] = building_class
        json_data['offset'] = 0

        while True:


            response = requests.post(
                'https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/',
                cookies=cookies,
                headers=headers,
                json=json_data,
            )

            items = response.json()['newbuildings']

            for i in items:
                if i['fromDeveloperPropsCount'] < 1:
                    continue
                id = i['id']
                building_classes_dict[id] = building_class
                ids.append(id)
            if not items:
                print(building_classes_dict)
                break

            json_data['offset'] += 25

    city_in_work = response.json()['breadcrumbs'][0]['title']

    return ids, building_classes_dict


