import requests
import pandas as pd

cookies = {
    '_ym_uid': '1704875117707080734',
    'uwyii': 'e7496b0f-f18c-d8e6-b005-a9a1e737ef5d',
    'mos_id': 'Cg+IAmkwfnkjTAz8NB2xAgA=',
    '_ym_d': '1764785786',
    'das_d_tag2': '26ed268a-fded-407b-baa9-45253674a3bf',
    'das_d_tag2_legacy': '26ed268a-fded-407b-baa9-45253674a3bf',
    'PHPSESSID': 'lig13tl7wSdsz5u6Wc7vQU7nEnt75ZG6',
    'BITRIX_SM_PK': 'page',
    'BITRIX_CONVERSION_CONTEXT_s1': '%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1780531140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'cookie': '1',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://fr.mos.ru/?ysclid=mpy4afpnx4165744817',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ym_uid=1704875117707080734; uwyii=e7496b0f-f18c-d8e6-b005-a9a1e737ef5d; mos_id=Cg+IAmkwfnkjTAz8NB2xAgA=; _ym_d=1764785786; das_d_tag2=26ed268a-fded-407b-baa9-45253674a3bf; das_d_tag2_legacy=26ed268a-fded-407b-baa9-45253674a3bf; PHPSESSID=lig13tl7wSdsz5u6Wc7vQU7nEnt75ZG6; BITRIX_SM_PK=page; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1780531140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; _ym_isad=2; _ym_visorc=w; cookie=1',
}

county_dict = {}
district_dict = {}



params = {
    'cmd': 'filters',
}

response = requests.get(
    'https://fr.mos.ru/pokupka-nedvizhimosti-dlya-vseh/ajax.php',
    params=params,
    cookies=cookies,
    headers=headers,
)

data = response.json()

print(response.status_code)

for county_id, county_data in data['filters']['county'].items():

    county_dict[int(county_id)] = county_data['full_name']

    for district_id, district_data in county_data['district'].items():
        district_dict[int(district_id)] = district_data['name']


response = requests.get(
    'https://fr.mos.ru/pokupka-nedvizhimosti-dlya-vseh/ajax.php?category[]=ALL&map=ren',
    cookies=cookies,
    headers=headers,
)
result = []
print(response.status_code)

items = response.json()['objects']['items']
for i in items:
    project_id = i['id']
    adress = i['name']
    code = i['code']
    district = district_dict.get(i['district'])
    county = county_dict.get(i['county'])
    status_code = i['status_code'].replace('FINISHED', 'Введены в эксплуатацию').replace('OLD', 'Дома, включенные в программу реновации').replace('PROCESSING', 'Строится').replace('START', 'Стартовые площадки')
    result.append([project_id, adress, code, district, county, status_code])








df = pd.DataFrame(result)

print(df.info())
print(df.head())

df.to_excel(r'C:\PycharmProjects\ndv_parcing\Фонд_реновации.xlsx')






