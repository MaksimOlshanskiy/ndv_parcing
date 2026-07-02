import random
import time
import pandas as pd
import requests



proxies = {
    "http": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270",
"https": "http://xDNa7kBu1c:lyUDim3VtZ@pool.proxy.market:10270"
}


cookies = {
    'srv_id': '2dnESOo22eCGPdM3._chqovxdeOGTz9UjzQMiIzrn8MyW-6IUdyzb-V_Oei8Ss8-ofypac4siLzEU6JA=.3tq9c31xQbaRA9OEi6tmRSxyg2qxHEDU38xPbX1xEK8=.web',
    'u': '3brjague.pc23wr.1wjj8jh2v2q0',
    'h_u': 'c3845c3f3b2ac21b:1782982680',
    'selected_locale': 'ru-RU',
    '_gcl_au': '1.1.943401564.1782982713',
    '_ga': 'GA1.1.911765094.1782982714',
    'luri': 'moskva',
    'buyer_location_id': '637640',
    'cookie_consent_shown': '1',
    'SEARCH_HISTORY_IDS': '1%2C4%2C%2C3',
    'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
    'f': '5.b5dcd0bea8d6cb0db75ecc2c69e0e99847e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9c99dece94c5a563168e2978c700f15b6831064c92d93c3903815369ae2d1a81d4e0d8a280d6b65f00df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f6421a43c89527accb13a8f8bc44c0f353f1a9afb448c9611b8c080393b6e127dbba00594a1bd53a660e6233a985e80aa28afb04ec07e43a120cfb0fb526bb39450a46b8ae4e81acb9fa46b8ae4e81acb9fadc0d86d9e44006d8313ab77de0efbe16aa061a6227ce656d2da10fb74cac1eab2da10fb74cac1eaba5d9b37818eab7b0a1a4f6d22df17006a44a72275ee79654',
    'ft': '"yyd7ilFMCSvPmVhenHG7f3zgG9y/aA5LmbOZdDSwABktB0XYWMxemeAmXKWOK9kYevRiqnnv08nn5Whoy1gX7Ia2dvzdmZNyWTlUfkq271vXhElRv92xoFgb+2Rbo4RPdlrM/ynOgh9APxpnUTVZ/w=="',
    'v': '1782985296',
    'cssid': '28805c82-b692-471a-b123-08c787cc66ce',
    'cssid_exp': '1782987099574',
    'buyer_from_page': 'catalog',
    'sx': 'H4sIAAAAAAAC%2F1TMMa6CQBAG4LtMTbHLz84A7XuJNhobGztmd8YCNNEYISHc3crCC3wrcZICi1qAVhQl5wytRaOlZGiF%2BpXe1FPa%2Fc3H8rT59LiM7i%2BqyKiP0iJI5I63igxuDM%2FuEaqo89CZqw7WBIZI%2BFIH7abrfrFxuf%2Bfp%2Bb2Q0ngbfsEAAD%2F%2F3HUibWXAAAA',
    'tmr_lvid': 'f18e0a65305840b8206b3f0ae143af8a',
    'tmr_lvidTS': '1704448814427',
    'domain_sid': 'xjgx3fJR1R3syH_6fe10Q%3A1782985616308',
    '_ym_uid': '1704448817787041633',
    '_ym_d': '1782985624',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    '_avisc': '3t95wUSidDkUNBQ4L3dO+tmvvJ1VoAGF+L/zDKy0Isc=',
    'pageviewCount': '5',
    '_ga_M29JC28873': 'GS2.1.s1782985298$o2$g1$t1782985663$j3$l0$h0',
    'tmr_detect': '0%7C1782985675403',
    '_adcc': '2.ntWQoKgamyW81ZVkS4xg72z0DJmMpOLGeT3hkfgJTM8dw1Qt34rF/rGvcTqLaPqnfGaCMDOQqZzwoLTgsySiTJnxh1OXXOq9qMQuyWBUZ73bWXjN/gdAoxbGc9Y+SQa4pp2OHmTvKzIAvRT0C2JQYBnEzcma',
    'csprefid': 'b4e9018b-f76b-48ba-80bf-78141a56e5e6',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.avito.ru/moskva/kvartiry/prodam/vtorichka-ASgBAgICAkSSA8YQ5geMUg?f=ASgBAgICA0SSA8YQ5geMUpC~DZauNQ&i=1',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-source': 'client-browser',
    # 'cookie': 'srv_id=2dnESOo22eCGPdM3._chqovxdeOGTz9UjzQMiIzrn8MyW-6IUdyzb-V_Oei8Ss8-ofypac4siLzEU6JA=.3tq9c31xQbaRA9OEi6tmRSxyg2qxHEDU38xPbX1xEK8=.web; u=3brjague.pc23wr.1wjj8jh2v2q0; h_u=c3845c3f3b2ac21b:1782982680; selected_locale=ru-RU; _gcl_au=1.1.943401564.1782982713; _ga=GA1.1.911765094.1782982714; luri=moskva; buyer_location_id=637640; cookie_consent_shown=1; SEARCH_HISTORY_IDS=1%2C4%2C%2C3; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; f=5.b5dcd0bea8d6cb0db75ecc2c69e0e99847e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9c99dece94c5a563168e2978c700f15b6831064c92d93c3903815369ae2d1a81d4e0d8a280d6b65f00df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f6421a43c89527accb13a8f8bc44c0f353f1a9afb448c9611b8c080393b6e127dbba00594a1bd53a660e6233a985e80aa28afb04ec07e43a120cfb0fb526bb39450a46b8ae4e81acb9fa46b8ae4e81acb9fadc0d86d9e44006d8313ab77de0efbe16aa061a6227ce656d2da10fb74cac1eab2da10fb74cac1eaba5d9b37818eab7b0a1a4f6d22df17006a44a72275ee79654; ft="yyd7ilFMCSvPmVhenHG7f3zgG9y/aA5LmbOZdDSwABktB0XYWMxemeAmXKWOK9kYevRiqnnv08nn5Whoy1gX7Ia2dvzdmZNyWTlUfkq271vXhElRv92xoFgb+2Rbo4RPdlrM/ynOgh9APxpnUTVZ/w=="; v=1782985296; cssid=28805c82-b692-471a-b123-08c787cc66ce; cssid_exp=1782987099574; buyer_from_page=catalog; sx=H4sIAAAAAAAC%2F1TMMa6CQBAG4LtMTbHLz84A7XuJNhobGztmd8YCNNEYISHc3crCC3wrcZICi1qAVhQl5wytRaOlZGiF%2BpXe1FPa%2Fc3H8rT59LiM7i%2BqyKiP0iJI5I63igxuDM%2FuEaqo89CZqw7WBIZI%2BFIH7abrfrFxuf%2Bfp%2Bb2Q0ngbfsEAAD%2F%2F3HUibWXAAAA; tmr_lvid=f18e0a65305840b8206b3f0ae143af8a; tmr_lvidTS=1704448814427; domain_sid=xjgx3fJR1R3syH_6fe10Q%3A1782985616308; _ym_uid=1704448817787041633; _ym_d=1782985624; _ym_isad=2; _ym_visorc=b; _avisc=3t95wUSidDkUNBQ4L3dO+tmvvJ1VoAGF+L/zDKy0Isc=; pageviewCount=5; _ga_M29JC28873=GS2.1.s1782985298$o2$g1$t1782985663$j3$l0$h0; tmr_detect=0%7C1782985675403; _adcc=2.ntWQoKgamyW81ZVkS4xg72z0DJmMpOLGeT3hkfgJTM8dw1Qt34rF/rGvcTqLaPqnfGaCMDOQqZzwoLTgsySiTJnxh1OXXOq9qMQuyWBUZ73bWXjN/gdAoxbGc9Y+SQa4pp2OHmTvKzIAvRT0C2JQYBnEzcma; csprefid=b4e9018b-f76b-48ba-80bf-78141a56e5e6',
}

params = {
    'categoryId': '24',
    'locationId': '637640',
    'i': '1',
    'cd': '0',
    'p': '1',
    'params[201]': '1059',
    'params[499]': '5254',
    'params[110472]': '437131',
    'verticalCategoryId': '1',
    'rootCategoryId': '4',
    'localPriority': '0',
    'updateListOnly': 'true',
    'context': 'H4sIAAAAAAAA_wEmANn_YToxOntzOjE6InkiO3M6MTY6IkMyc0FveHRrS1BkQUxudHciO30fw85KJgAAAA',
}

result = []

while True:

    response = requests.get('https://www.avito.ru/web/1/js/items', params=params, cookies=cookies, headers=headers, proxies=proxies)

    print(response.status_code)
    items = response.json()['catalog']['items']
    for item in items:
        try:
            if item['type'] != 'item':
                continue
            address_user = item['coords']['address_user']
            street = item['geo']['addressLinks']['streetLink']['text']
            house = item['geo']['addressLinks']['houseLink']['text']
            metro = item['geo']['addressLinks']['metroLink']['text']
            price = item['priceDetailed']['value']
            title = item['title']
            url = 'https://www.avito.ru/' + item['urlPath']

            print(address_user, price, url)
            result.append([address_user, street, house, metro, price, title, url])

        except:
            continue
    if not items:
        break
    params['p'] = str(int(params['p']) +1)
    if int(params['p']) > 56:
        break
    sleep_time = random.uniform(7, 9)
    time.sleep(sleep_time)

df = pd.DataFrame(result)
df.to_excel('avito_02-07-26.xlsx', index=False)

