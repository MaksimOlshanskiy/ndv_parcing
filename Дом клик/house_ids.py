import requests


cookies = {
    'ns_session': '8d885eed-c151-4167-9919-8657ec697ffe',
    '_ym_uid': '1765012936500443323',
    '_ym_d': '1782939022',
    'logoSuffix': '',
    'iosAppLink': '',
    'showDddWidgets': 'true',
    'RETENTION_COOKIES_NAME': '73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc',
    'sessionId': '12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70',
    'UNIQ_SESSION_ID': 'd58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8',
    'adtech_uid': 'c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru',
    'top100_id': 't1.7711713.584217383.1782939023617',
    'tmr_lvid': '6509c7cbd63e89eea195eb14c34fbb17',
    'tmr_lvidTS': '1773855203088',
    'regionAlert': '1',
    'favoriteHintShowed': 'true',
    't3_sid_7731951': 's1.270570886.1785337030781.1785363618239.6.13.1.1..',
    't3_sid_7711713': 's1.1016988686.1785337030788.1785363618245.7.7.1.1..',
    'auto-definition-region': 'false',
    'cookieAlert': '1',
    'currentRegionGuid': '1691f4a5-8e87-41ab-b0d3-05a0c7a07c76',
    'currentLocalityGuid': '857c0a08-7dc0-445e-a044-ed2f6d435a7b',
    'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22}%2C%22isAutoResolved%22:true}',
    'qrator_jsr': 'v2.0.1785766211.157.05e47254IXz1AIS3|mXIsp8lYTRbaMgne|4zQrCIx4tVv7IME0KaGC6O/fbyxboFkbAjX3pHKcvYNOd8o4Exn8+1Gwxqi6gYWPRQnkuYAipZhEOghKFVFZYQ==-CtFypS3fRkpRYtdkQRdw2O7zMUU=-00',
    'qrator_jsid2': 'v2.0.1785766211.157.05e47254IXz1AIS3|WjAiWXgIHwEiet9I|7XWeIf2Nii4TYnQqJ1kHuqdxRgmRhlAMrDQglmV3OIU8kgLERhaaaED4f8tWqROr5BCzH8ByaITr/LefoPbSQXviHHPVBtRbOmvTmXdOuerdMa+IC2NUr7yLkgX8v0my9xzRoPicoscuE0LuURrGC3YGGhh6bdAvKsdEWP3mjEs=-Xhg3FpEZVrpSwIm6rJH61MNLox0=',
    '_sa': 'SA1.5921084b-375c-4426-927c-9703572e4456.1785766215',
    '_sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9': 'SA1.5921084b-375c-4426-927c-9703572e4456.1785766215.1785766215',
    '_sas': 'SA1.5921084b-375c-4426-927c-9703572e4456.1785766215.1785766216',
    'tmr_reqNum': '498',
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'ns_session=8d885eed-c151-4167-9919-8657ec697ffe; _ym_uid=1765012936500443323; _ym_d=1782939022; logoSuffix=; iosAppLink=; showDddWidgets=true; RETENTION_COOKIES_NAME=73a09f72fd964582843061b4531b1749:PzMXzDiTZwMDclesDmpsDzCazRc; sessionId=12791819e59a41f69051746fca5dad7a:kEQkdePJp_BacogdDvlAn091-70; UNIQ_SESSION_ID=d58e9846198b4c0289a92ac3432ed3b7:UMgljoWSM32ON1aIaU9IGAv1Sq8; adtech_uid=c9082c41-db22-46c2-ad5a-794db0f6fa39%3Adomclick.ru; top100_id=t1.7711713.584217383.1782939023617; tmr_lvid=6509c7cbd63e89eea195eb14c34fbb17; tmr_lvidTS=1773855203088; regionAlert=1; favoriteHintShowed=true; t3_sid_7731951=s1.270570886.1785337030781.1785363618239.6.13.1.1..; t3_sid_7711713=s1.1016988686.1785337030788.1785363618245.7.7.1.1..; auto-definition-region=false; cookieAlert=1; currentRegionGuid=1691f4a5-8e87-41ab-b0d3-05a0c7a07c76; currentLocalityGuid=857c0a08-7dc0-445e-a044-ed2f6d435a7b; region={%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22regionGuid%22:%221691f4a5-8e87-41ab-b0d3-05a0c7a07c76%22%2C%22localityGuid%22:%22857c0a08-7dc0-445e-a044-ed2f6d435a7b%22}%2C%22isAutoResolved%22:true}; qrator_jsr=v2.0.1785766211.157.05e47254IXz1AIS3|mXIsp8lYTRbaMgne|4zQrCIx4tVv7IME0KaGC6O/fbyxboFkbAjX3pHKcvYNOd8o4Exn8+1Gwxqi6gYWPRQnkuYAipZhEOghKFVFZYQ==-CtFypS3fRkpRYtdkQRdw2O7zMUU=-00; qrator_jsid2=v2.0.1785766211.157.05e47254IXz1AIS3|WjAiWXgIHwEiet9I|7XWeIf2Nii4TYnQqJ1kHuqdxRgmRhlAMrDQglmV3OIU8kgLERhaaaED4f8tWqROr5BCzH8ByaITr/LefoPbSQXviHHPVBtRbOmvTmXdOuerdMa+IC2NUr7yLkgX8v0my9xzRoPicoscuE0LuURrGC3YGGhh6bdAvKsdEWP3mjEs=-Xhg3FpEZVrpSwIm6rJH61MNLox0=; _sa=SA1.5921084b-375c-4426-927c-9703572e4456.1785766215; _sas.2c534172f17069dd8844643bb4eb639294cd4a7a61de799648e70dc86bc442b9=SA1.5921084b-375c-4426-927c-9703572e4456.1785766215.1785766215; _sas=SA1.5921084b-375c-4426-927c-9703572e4456.1785766215.1785766216; tmr_reqNum=498',
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
