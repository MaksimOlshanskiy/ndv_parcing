import requests


cookies = {
    '_ym_uid': '1765012936500443323',
    '_ym_d': '1765012936',
    'adtech_uid': 'c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru',
    'ns_session': '6b7f0e11-9d39-4d9f-bde9-e0ea2b194184',
    'RETENTION_COOKIES_NAME': 'c4194f168c4b486394b9e0e579a6ad7c:rcdfFDfvr7s0pTQeRgykGrLqh8M',
    'sessionId': '47f88fa2f01a440f9154dfe2c16bc0ef:kumwnApx1cyy1eyhaY2VD01hj_U',
    'UNIQ_SESSION_ID': '8aebb9c1984c4fdbad9edaf6dc22d362:WPANcUW3wmpwW1wxsCc8-9CCjGk',
    'logoSuffix': '',
    'iosAppLink': '',
    '_sv': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688',
    'top100_id': 't1.7711713.1020003933.1779904305209',
    'tmr_lvid': '6509c7cbd63e89eea195eb14c34fbb17',
    'tmr_lvidTS': '1773855203088',
    'showDddIntro': 'false',
    'dddIntroOnline': 'false',
    'regionAlert': '1',
    'max-chat-settings-show': '%7B%22countOfEntry%22%3A4%2C%22lastStatus%22%3A%22NOT_CREATED%22%7D',
    '_ym_isad': '2',
    'cookieAlert': '1',
    'currentRegionGuid': '1691f4a5-8e87-41ab-b0d3-05a0c7a07c76',
    'currentLocalityGuid': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'regionName': '857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22}%2C%22isAutoResolved%22:true}',
    'canary-bind-id-14320': 'next-2',
    'qrator_jsid2': 'v2.0.1780505330.747.5fa9bf1fTzzOGZv1|MuRdtsnG0clUjtXK|zgG8yfa5RvJM9buUPmkQprHXpxmk4K+nWaabSleprs3WdqLyKiyfFbhUTLNwsod/ke/1Dg0PdlmXuJvfs+LrcffRK9ovQ+6WXuqybFESjvK/D7kappAjlRIcZWffjFC60tVciNJh8mHSahv6KrDaDdQ4x8a7WHzSfxiAUmcguiU=-gilOTd250JF5gkDc/0VdiTKNwX0=',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780512903',
    '_sas': 'SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780512903',
    't3_sid_7711713': 's1.160642329.1780471411515.1780512904865.7.74.10.1..',
    'tmr_reqNum': '224',
    '_visitId': '72328566-6e23-4a01-a948-c54a11d34be1-6315121d1b510ace',
    't3_sid_7731951': 's1.21260308.1780471411528.1780512908310.6.199.10.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://ufa.domclick.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://ufa.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1765012936500443323; _ym_d=1765012936; adtech_uid=c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru; ns_session=6b7f0e11-9d39-4d9f-bde9-e0ea2b194184; RETENTION_COOKIES_NAME=c4194f168c4b486394b9e0e579a6ad7c:rcdfFDfvr7s0pTQeRgykGrLqh8M; sessionId=47f88fa2f01a440f9154dfe2c16bc0ef:kumwnApx1cyy1eyhaY2VD01hj_U; UNIQ_SESSION_ID=8aebb9c1984c4fdbad9edaf6dc22d362:WPANcUW3wmpwW1wxsCc8-9CCjGk; logoSuffix=; iosAppLink=; _sv=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688; top100_id=t1.7711713.1020003933.1779904305209; tmr_lvid=6509c7cbd63e89eea195eb14c34fbb17; tmr_lvidTS=1773855203088; showDddIntro=false; dddIntroOnline=false; regionAlert=1; max-chat-settings-show=%7B%22countOfEntry%22%3A4%2C%22lastStatus%22%3A%22NOT_CREATED%22%7D; _ym_isad=2; cookieAlert=1; currentRegionGuid=1691f4a5-8e87-41ab-b0d3-05a0c7a07c76; currentLocalityGuid=857c0a08-7dc0-445e-a044-ed2f6d435a7b; regionName=857c0a08-7dc0-445e-a044-ed2f6d435a7b:%D0%A3%D1%84%D0%B0; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22}%2C%22isAutoResolved%22:true}; canary-bind-id-14320=next-2; qrator_jsid2=v2.0.1780505330.747.5fa9bf1fTzzOGZv1|MuRdtsnG0clUjtXK|zgG8yfa5RvJM9buUPmkQprHXpxmk4K+nWaabSleprs3WdqLyKiyfFbhUTLNwsod/ke/1Dg0PdlmXuJvfs+LrcffRK9ovQ+6WXuqybFESjvK/D7kappAjlRIcZWffjFC60tVciNJh8mHSahv6KrDaDdQ4x8a7WHzSfxiAUmcguiU=-gilOTd250JF5gkDc/0VdiTKNwX0=; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780512903; _sas=SV1.ac0fd74b-ce4b-4462-a8b3-8e03416e7213.1728322688.1780512903; t3_sid_7711713=s1.160642329.1780471411515.1780512904865.7.74.10.1..; tmr_reqNum=224; _visitId=72328566-6e23-4a01-a948-c54a11d34be1-6315121d1b510ace; t3_sid_7731951=s1.21260308.1780471411528.1780512908310.6.199.10.1..',
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
    'aids': '5007',
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
