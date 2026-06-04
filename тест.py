import random
import time
import pandas as pd

import requests

cookies = {
    '_ym_uid': '1704875117707080734',
    'uwyii': 'e7496b0f-f18c-d8e6-b005-a9a1e737ef5d',
    'mos_id': 'Cg+IAmkwfnkjTAz8NB2xAgA=',
    '_ym_d': '1764785786',
    'das_d_tag2': '26ed268a-fded-407b-baa9-45253674a3bf',
    'das_d_tag2_legacy': '26ed268a-fded-407b-baa9-45253674a3bf',
    'sbp_sid': '000000000000000000000000000000000000',
    'yabm': 'k5mre1v8ajqk2s1u92q9ujfjc5',
    'Ltpatoken2': 'bb2/8m6YSxgYNbRnW/YBFOfRAjBuNvVs0ad8PfdLpKT1vVnPUp/uH3m8fIgqPD5uBj8r79eM3AvTD499qzksn5TWAImhjF/u5gZdJcMI6tR6gScWnsHNjxQlrqHV8mtydRhmHHVko2qgTIP/GjDf/rTIuqfAMHKZrwd2AMYaaKLg444aH5KaGwwOHEo5lR0bIasjiFkGFNeFC5h7yLHlYbL+D6dTsnbI8UzpUy76Ih2ShAispd5oBlj9q7lc8K/Kguu2AUACct3IwL28k8cw3eSb5VoHNb64faFGxNzPJ7V65tV/D5TXQketdZfZuLp5SVZ7IiI7tK8VqKr4W45dJg==',
    'ghur': '-vFN77CtZecxsc82IDN3yaX8Zimlkd-5H1XeqT2yVtU|',
    'at': '1',
    'SESSION': 'MTYzMjI2MGYtMzg5Ni00ZmE4LTlkMDktMWQ0MmMyN2VmOTRm',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://gisogd.mos.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://gisogd.mos.ru/objects',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': '_ym_uid=1704875117707080734; uwyii=e7496b0f-f18c-d8e6-b005-a9a1e737ef5d; mos_id=Cg+IAmkwfnkjTAz8NB2xAgA=; _ym_d=1764785786; das_d_tag2=26ed268a-fded-407b-baa9-45253674a3bf; das_d_tag2_legacy=26ed268a-fded-407b-baa9-45253674a3bf; sbp_sid=000000000000000000000000000000000000; yabm=k5mre1v8ajqk2s1u92q9ujfjc5; Ltpatoken2=bb2/8m6YSxgYNbRnW/YBFOfRAjBuNvVs0ad8PfdLpKT1vVnPUp/uH3m8fIgqPD5uBj8r79eM3AvTD499qzksn5TWAImhjF/u5gZdJcMI6tR6gScWnsHNjxQlrqHV8mtydRhmHHVko2qgTIP/GjDf/rTIuqfAMHKZrwd2AMYaaKLg444aH5KaGwwOHEo5lR0bIasjiFkGFNeFC5h7yLHlYbL+D6dTsnbI8UzpUy76Ih2ShAispd5oBlj9q7lc8K/Kguu2AUACct3IwL28k8cw3eSb5VoHNb64faFGxNzPJ7V65tV/D5TXQketdZfZuLp5SVZ7IiI7tK8VqKr4W45dJg==; ghur=-vFN77CtZecxsc82IDN3yaX8Zimlkd-5H1XeqT2yVtU|; at=1; SESSION=MTYzMjI2MGYtMzg5Ni00ZmE4LTlkMDktMWQ0MmMyN2VmOTRm',
}

json_data = {
    'destination': 'административно-деловые объекты',
    'pagination': {
        'size': 10,
        'page': 311,
        'total': 8257,
    },
}

result = []
counter = 0
while counter < json_data['pagination']['total']:

    print(json_data['pagination']['page'])
    response = requests.post(
        'https://gisogd.mos.ru/isogd/front/api/gisogd/objects/search',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    print(response.status_code)
    items = response.json()['data']

    for i in items:

        counter += 1
        address = i.get('address', None)
        casesForLandPlots = i.get('casesForLandPlots', None)
        destination = i.get('destination', None)
        guid = i.get('guid', None)
        name = i.get('name', None)
        permissionFoFacility = i.get('permissionFoFacility', None)
        permissionForBuilding = i.get('permissionForBuilding', None)
        status = i.get('status', None)
        urbanPlanningPlans = i.get('urbanPlanningPlans', None)
        try:
            cadastralNumbers = i['terrains'][0]['cadastralNumbers'][0]['cadastralNumber']
        except:
            cadastralNumbers = ''
        try:
            district = i['terrains'][0]['district']['title']
        except:
            district = ''
        try:
            region = i['terrains'][0]['region']['title']
        except:
            region = ''
        print([address, casesForLandPlots, destination, guid, name, permissionFoFacility, permissionForBuilding, status, urbanPlanningPlans, cadastralNumbers, district, region])
        result.append([address, casesForLandPlots, destination, guid, name, permissionFoFacility, permissionForBuilding, status, urbanPlanningPlans, cadastralNumbers, district, region])
    json_data['pagination']['page'] += 1

    time.sleep(random.uniform(0, 2))

    df = pd.DataFrame(result, columns=['address', 'casesForLandPlots', 'destination', 'guid', 'name', 'permissionFoFacility', 'permissionForBuilding', 'status', 'urbanPlanningPlans', 'cadastralNumbers', 'district', 'region'])

    df.to_excel('offices310.xlsx', index=False)


