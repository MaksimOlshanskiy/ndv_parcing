import requests


cookies = {
    'ns_session': 'a9b0527d-1831-4051-9691-f2a4ff9f2eb1',
    '_ym_uid': '1754049701221173595',
    '_ym_d': '1754049701',
    'is-green-day-banner-hidden': 'true',
    'is-ddf-banner-hidden': 'true',
    'RETENTION_COOKIES_NAME': 'cf097f92a360491a94d2b23ea308902f:ztXlYHeFUoQ4EW8CGN8-8HaKM5o',
    'sessionId': 'b53dde4d6b3e41048c50269ef9a9a640:087ckq3ae0HFXc7RfxSMR6JZ4eE',
    'UNIQ_SESSION_ID': 'e3b5b2661819410dab5179919a9a5dbf:4X3jH9cQ0_NIooq_KXzwDcVRQfQ',
    'logoSuffix': '',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}',
    'adrcid': 'ATq4NGAhUq_h0PN1rcX56vw',
    'adtech_uid': '2529e064-13de-46d3-b559-557905b2c7ab%3Adomclick.ru',
    'top100_id': 't1.7711713.1875136519.1754049702923',
    'tmr_lvid': '591f79504a966df059c5d4755ee24cfd',
    'tmr_lvidTS': '1754049703045',
    'regionAlert': '1',
    'iosAppAvailable': 'true',
    'cookieAlert': '1',
    'iosAppLink': '',
    'auto-definition-region': 'false',
    'currentSubDomain': 'samara',
    '_sv': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664',
    'adrdel': '1759388033851',
    'qrator_jsr': 'v2.0.1759473042.011.59bc78366yAvg5Tp|drNsNYFMREeM3S5n|8tUhfFgWFJytULpM+oU+VkWXV+ZSyHyMxIm/+16QZOOp+1m1VhWWGFuI1MQzIQ/UT+kxYSNKCUoipp6CerClVQ==-F4M7/56Oeu5hBcQuu7f7MWbiDYI=-00',
    'qrator_jsid2': 'v2.0.1759473042.011.59bc78366yAvg5Tp|vaDq5x3IZFR8ySzc|uHxI/dcmbno3EK1MNh2Szg464g5qKhtTnKPdxujLxLUqkROV2/3tAQ/5iKHCj123a8CQ1UNiGRY5A2KoCTwssc28Jwi7VDoUJw5RQzv2fSfbavhpIlLfG134Hsh6cig0pj+Gu2xpzYI3KUnX1iCB3w==-7CkWf0POLc7RrUq+Ji5aqFezVbI=',
    '_ym_isad': '2',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473042',
    '_visitId': '6eb33d4f-caf5-4022-a04c-cb1cb64c9057-f4f0dcc432ac8ba6',
    '_sas': 'SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473048',
    'currentRegionGuid': '321b0daa-da95-4ce5-81b3-a7ab62d89d19',
    'currentLocalityGuid': '6369cbfc-1f06-4574-adba-82f4dc42c0f7',
    'regionName': '6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0',
    'tmr_reqNum': '361',
    't3_sid_7711713': 's1.350417262.1759473043176.1759473112563.6.11.2.1..',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://samara.domclick.ru',
    'Referer': 'https://samara.domclick.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=a9b0527d-1831-4051-9691-f2a4ff9f2eb1; _ym_uid=1754049701221173595; _ym_d=1754049701; is-green-day-banner-hidden=true; is-ddf-banner-hidden=true; RETENTION_COOKIES_NAME=cf097f92a360491a94d2b23ea308902f:ztXlYHeFUoQ4EW8CGN8-8HaKM5o; sessionId=b53dde4d6b3e41048c50269ef9a9a640:087ckq3ae0HFXc7RfxSMR6JZ4eE; UNIQ_SESSION_ID=e3b5b2661819410dab5179919a9a5dbf:4X3jH9cQ0_NIooq_KXzwDcVRQfQ; logoSuffix=; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%221d1463ae-c80f-4d19-9331-a1b68a85b553%22}%2C%22isAutoResolved%22:true}; adrcid=ATq4NGAhUq_h0PN1rcX56vw; adtech_uid=2529e064-13de-46d3-b559-557905b2c7ab%3Adomclick.ru; top100_id=t1.7711713.1875136519.1754049702923; tmr_lvid=591f79504a966df059c5d4755ee24cfd; tmr_lvidTS=1754049703045; regionAlert=1; iosAppAvailable=true; cookieAlert=1; iosAppLink=; auto-definition-region=false; currentSubDomain=samara; _sv=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664; adrdel=1759388033851; qrator_jsr=v2.0.1759473042.011.59bc78366yAvg5Tp|drNsNYFMREeM3S5n|8tUhfFgWFJytULpM+oU+VkWXV+ZSyHyMxIm/+16QZOOp+1m1VhWWGFuI1MQzIQ/UT+kxYSNKCUoipp6CerClVQ==-F4M7/56Oeu5hBcQuu7f7MWbiDYI=-00; qrator_jsid2=v2.0.1759473042.011.59bc78366yAvg5Tp|vaDq5x3IZFR8ySzc|uHxI/dcmbno3EK1MNh2Szg464g5qKhtTnKPdxujLxLUqkROV2/3tAQ/5iKHCj123a8CQ1UNiGRY5A2KoCTwssc28Jwi7VDoUJw5RQzv2fSfbavhpIlLfG134Hsh6cig0pj+Gu2xpzYI3KUnX1iCB3w==-7CkWf0POLc7RrUq+Ji5aqFezVbI=; _ym_isad=2; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473042; _visitId=6eb33d4f-caf5-4022-a04c-cb1cb64c9057-f4f0dcc432ac8ba6; _sas=SV1.11d5cae6-4212-4501-8b96-a68ac36bdb50.1754049664.1759473048; currentRegionGuid=321b0daa-da95-4ce5-81b3-a7ab62d89d19; currentLocalityGuid=6369cbfc-1f06-4574-adba-82f4dc42c0f7; regionName=6369cbfc-1f06-4574-adba-82f4dc42c0f7:%D0%A1%D0%B0%D0%BC%D0%B0%D1%80%D0%B0; tmr_reqNum=361; t3_sid_7711713=s1.350417262.1759473043176.1759473112563.6.11.2.1..',
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
    'enable_mixed_ranking': '1',
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
