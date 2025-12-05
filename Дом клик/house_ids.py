import requests


cookies = {
    'ns_session': '5210b38b-2a77-4df9-a428-6405b3065d3d',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'logoSuffix': '',
    'RETENTION_COOKIES_NAME': 'd7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI',
    'sessionId': 'be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE',
    'UNIQ_SESSION_ID': '01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs',
    'adtech_uid': '5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru',
    'top100_id': 't1.7711713.1405137252.1743518288740',
    '_ym_uid': '1743518289666663600',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'tmr_lvid': '6b6b440680155a4ac17ccaf6a462f603',
    'tmr_lvidTS': '1743518291170',
    'regionAlert': '1',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING': 'true',
    'cookieAlert': '1',
    'iosAppLink': '',
    'COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING': 'true',
    '_ym_d': '1759300554',
    'adrdel': '1759300555210',
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'qrator_jsid2': 'v2.0.1764835075.735.5b6ce31fHMje9sFq|2sLXcB87EAsiDGsg|MGF+NlOgj+V89me7yNDwFvyknhWX8DilTa9SYD45IWPaMrXjx+NTB7uSihpQLhx2sFKNeDwi0gOchkfBdaoIZSZ1yI3oTWt03sYTC94FYWB5R/ssFI3hxLAvcchY23KzWHOtUB5xNYpyQs5pLhEKAcCC2aup8ffNJ6jePGeq8a8=-ALMyho13mg2IFAjn+qhQ5Vzq62o=',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1764835079',
    '_ym_isad': '2',
    '_visitId': '5d48994b-6899-4f9b-913c-b3f87f352e0f-f4f0dcc432ac8ba6',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1764835084',
    'currentRegionGuid': '1691f4a5-8e87-41ab-b0d3-05a0c7a07c76',
    'currentLocalityGuid': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'regionName': '857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0',
    'tmr_reqNum': '290',
    't3_sid_7711713': 's1.1185499917.1764835079664.1764835384659.29.15.2.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://ufa.domclick.ru',
    'Referer': 'https://ufa.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; logoSuffix=; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; iosAppLink=; COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING=true; _ym_d=1759300554; adrdel=1759300555210; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; qrator_jsid2=v2.0.1764835075.735.5b6ce31fHMje9sFq|2sLXcB87EAsiDGsg|MGF+NlOgj+V89me7yNDwFvyknhWX8DilTa9SYD45IWPaMrXjx+NTB7uSihpQLhx2sFKNeDwi0gOchkfBdaoIZSZ1yI3oTWt03sYTC94FYWB5R/ssFI3hxLAvcchY23KzWHOtUB5xNYpyQs5pLhEKAcCC2aup8ffNJ6jePGeq8a8=-ALMyho13mg2IFAjn+qhQ5Vzq62o=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1764835079; _ym_isad=2; _visitId=5d48994b-6899-4f9b-913c-b3f87f352e0f-f4f0dcc432ac8ba6; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1764835084; currentRegionGuid=1691f4a5-8e87-41ab-b0d3-05a0c7a07c76; currentLocalityGuid=857c0a08-7dc0-445e-a044-ed2f6d435a7b; regionName=857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0; tmr_reqNum=290; t3_sid_7711713=s1.1185499917.1764835079664.1764835384659.29.15.2.1..',
}

params = {
    'address': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'offset': '0',
    'limit': '20',
    'sort': 'qi',
    'sort_dir': 'desc',
    'deal_type': 'sale',
    'category': 'living',
    'offer_type': 'complex',
    'aids': '19186',
    'seo': '1',
}

all_items = []
ids = []
count = 0

url = "https://bff-search-web.domclick.ru/api/offers/v1"

while True:
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    if response.status_code != 200:
        print(f"Ошибка запроса: {response.status_code}")
        break

    data = response.json()
    items = data['result']['items']
    pagination = data['result']['pagination']

    all_items.extend(items)

    print(f"Получено: {len(all_items)} из {pagination['total']}")

    # Увеличиваем offset на размер страницы (limit)
    params['offset'] = str(int(params['offset']) + 20)

    # Если достигли или превысили total — выходим из цикла
    if int(params['offset']) >= pagination['total']:
        break

# Теперь в all_items у тебя все данные со всех страниц
for i in all_items:
    ids.append(i['id'])
    count += 1

print(count)
print(ids)
