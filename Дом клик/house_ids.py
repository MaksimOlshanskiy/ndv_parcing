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
    'COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING': 'true',
    '_ym_d': '1759300554',
    'adrdel': '1759300555210',
    '_sv': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000',
    'currentRegionGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'currentLocalityGuid': '1d1463ae-c80f-4d19-9331-a1b68a85b553',
    'regionName': '1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0',
    'favoriteHintShowed': 'true',
    'qrator_jsr': 'v2.0.1765175668.335.5b6ce31f82wfMzAJ|FGQ4eHaiSeVn2MYZ|wdHcIMSmbbdOV62Sb2cn0EV1ZksWBZcaRiYlalOk0s75R4GxR9JCIozy5FtjjMKqFVT7eUcb1ZgecgVWsK4GWQ==-hYWzzG/NDc+IzFDWYdR4tFOQGlM=-00',
    'qrator_ssid2': 'v2.0.1765175669.020.5b6ce31fuj39Qjst|ZKjOKXpnYfh2ZsFq|Ao2Wt2ogG2912gqlPQU9e8VzshPYJxhhaISNbkjtu+sd7kUo54eOjDqKAMtwtS05T6GBX6rwvKkno1GU4rNRGQ==-6vdA/6/yUz457q77rft+iw8pwxw=',
    'qrator_jsid2': 'v2.0.1765175668.335.5b6ce31f82wfMzAJ|hDmC8XEOs2qhZLh2|vAeSD78iq9bVVWVgbpv7T8XZ8P4tGGybI9ThcvN35t1aM9a79dAFXRT67Dl7ZLEA02xwqgx0glS/dxwvlMonT+isq6HGkiYeHsIresYtMbVUjt5C0C+zFz0Ai2pERQBAuwrxRVXRjKlBtEoO9hwHVxV8taEOuvWvJsGhriUpoDc=-DnEgu67TDaII/bjYuo4Z3GkBe/8=',
    'iosAppLink': '',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175674',
    '_ym_isad': '2',
    '_visitId': '9ec75f4a-da8b-4e97-a6b1-226f4918f4bf-f4f0dcc432ac8ba6',
    '_sas': 'SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175676',
    't3_sid_7711713': 's1.1313865512.1765175675052.1765175690493.32.4.1.1..',
    'tmr_reqNum': '286',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://domclick.ru',
    'Referer': 'https://domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=5210b38b-2a77-4df9-a428-6405b3065d3d; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; logoSuffix=; RETENTION_COOKIES_NAME=d7cf7088ab814dde8d8f546c98c6f8c4:nBa67XQBjdIGZ8ctm6VUWFBZvuI; sessionId=be29cf2aa31349c5b9526a8908556af9:qLh2pQi0C902c_qNAP6M4MB1TKE; UNIQ_SESSION_ID=01e8c70898c34d438fc9eefa59f4b03e:1_zXQ6IYGeCp9PiCY8T9XGEuXgs; adtech_uid=5b955382-d038-40cf-a271-c67f8cd94af8%3Adomclick.ru; top100_id=t1.7711713.1405137252.1743518288740; _ym_uid=1743518289666663600; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; tmr_lvid=6b6b440680155a4ac17ccaf6a462f603; tmr_lvidTS=1743518291170; regionAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_ONBOARDING=true; cookieAlert=1; COOKIE_IS_HIDDEN_EASY_SEARCH_COUNTRY_ONBOARDING=true; _ym_d=1759300554; adrdel=1759300555210; _sv=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000; currentRegionGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; currentLocalityGuid=1d1463ae-c80f-4d19-9331-a1b68a85b553; regionName=1d1463ae-c80f-4d19-9331-a1b68a85b553:%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0; favoriteHintShowed=true; qrator_jsr=v2.0.1765175668.335.5b6ce31f82wfMzAJ|FGQ4eHaiSeVn2MYZ|wdHcIMSmbbdOV62Sb2cn0EV1ZksWBZcaRiYlalOk0s75R4GxR9JCIozy5FtjjMKqFVT7eUcb1ZgecgVWsK4GWQ==-hYWzzG/NDc+IzFDWYdR4tFOQGlM=-00; qrator_ssid2=v2.0.1765175669.020.5b6ce31fuj39Qjst|ZKjOKXpnYfh2ZsFq|Ao2Wt2ogG2912gqlPQU9e8VzshPYJxhhaISNbkjtu+sd7kUo54eOjDqKAMtwtS05T6GBX6rwvKkno1GU4rNRGQ==-6vdA/6/yUz457q77rft+iw8pwxw=; qrator_jsid2=v2.0.1765175668.335.5b6ce31f82wfMzAJ|hDmC8XEOs2qhZLh2|vAeSD78iq9bVVWVgbpv7T8XZ8P4tGGybI9ThcvN35t1aM9a79dAFXRT67Dl7ZLEA02xwqgx0glS/dxwvlMonT+isq6HGkiYeHsIresYtMbVUjt5C0C+zFz0Ai2pERQBAuwrxRVXRjKlBtEoO9hwHVxV8taEOuvWvJsGhriUpoDc=-DnEgu67TDaII/bjYuo4Z3GkBe/8=; iosAppLink=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175674; _ym_isad=2; _visitId=9ec75f4a-da8b-4e97-a6b1-226f4918f4bf-f4f0dcc432ac8ba6; _sas=SV1.f1a08dc7-e850-4782-91b9-9a68b87e7bf1.1741776000.1765175676; t3_sid_7711713=s1.1313865512.1765175675052.1765175690493.32.4.1.1..; tmr_reqNum=286',
}

params = {
    'address': '6369cbfc-1f06-4574-adba-82f4dc42c0f7',
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
