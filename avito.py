import pandas as pd
import requests

cookies = {
    'srv_id': 'Gb6Fbx7syC7LYy8t.jYvIB-wUSRkcTmceXH4pn9zZVfdze23ZHsmYi0exT35flimYd7rPKb5yZ-5seBk=.26yBxWLRrZ-tm0iy-6Ah-hqesd5YHu7AsEIxLemnUqE=.web',
    '_avisc': 'X92YRW9wgisQUX6avuJxhcrlGrC9W5bG9gJdat2/vF8=',
    'u': '3bpzd62a.1l1blx.ymfdyb1js200',
    'v': '1780932810',
    'h_u': 'fba9ad8efced2bb2:1780932780',
    'selected_locale': 'ru-RU',
    '_gcl_au': '1.1.1955744551.1780932811',
    '_ga': 'GA1.1.1765901951.1780932812',
    'cssid': 'e5cb9e02-dc6b-4a59-9135-b12b00d7b1d9',
    'cssid_exp': '1780934612038',
    '_ym_uid': '1780932813814473936',
    '_ym_d': '1780932813',
    'cookie_consent_shown': '1',
    '_ym_isad': '2',
    'luri': 'moskva',
    'buyer_location_id': '637640',
    '_ym_visorc': 'b',
    'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
    'ma_id_api': 'k5dgGahBF6xn8morr02075wvMGXm7UT/3MtIfJrhEbdqsT7sOIKaLL4VtE51x+Sml98uM6yBIYIMj5CKjKH0InNTfMKycU+T0Hcv/cLfP8U6tFZWjkSzLbct8rjaWfvaocUABNRRYib0DqAT7HiWm1wAT1yTsrjlsoM5/iOq9xJVz5l5/XpM+TR8yTEBd0XE7aP4DvzdQeS+25oG3sz6MygsGSxzcHthuZSGbXi45NUTLoIb/CbKwltDuj991YLc73NTcJgVfjDOn4fEN39JM2J+rfq2UnSUfzfasiv0lqEQlr8XMrlj9XZ8mIVmhpEizcvuRg8dnw2UrdqaiwcqCA==',
    'tmr_lvid': '28d77703c279a2a9a1db42f152d89865',
    'tmr_lvidTS': '1780932817796',
    'adrdel': '1780932817803',
    'adrdel': '1780932817803',
    'adrcid': 'APu4BCRWelBbzwV_SPdwf5g',
    'adrcid': 'APu4BCRWelBbzwV_SPdwf5g',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1781019217813%2C%22sl%22%3A%7B%22224%22%3A1780932817813%2C%221228%22%3A1780932817813%7D%7D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1781019217813%2C%22sl%22%3A%7B%22224%22%3A1780932817813%2C%221228%22%3A1780932817813%7D%7D',
    'domain_sid': 'QOE2hQdHwoZGihqoqA7QQ%3A1780932817979',
    'uxs_uid': '6bae0950-634f-11f1-93e8-4f04af640159',
    '__upin': '09HKMOBPxRUdOhKhiUQ99w',
    'ma_id': '6322120861780932813192',
    '_ga_M29JC28873': 'GS2.1.s1780932811$o1$g1$t1780932822$j49$l0$h0',
    'sx': 'H4sIAAAAAAAC%2FwTAqw6DMBgF4Hc5emKn%2By9t3dS2ZIBCYClFk5Bgmr47X4O%2FkvimLCa%2BC2mmKkZfK72WpMgNFzL0%2FTmXadafj%2FH7Hw48UJHpkU%2BmENj7HQAA%2F%2F8EIbnNTAAAAA%3D%3D',
    '__ai_fp_uuid': '131e0b86379cf11a%3A2',
    'buyer_from_page': 'catalog',
    'f': '5.0c4f4b6d233fb906b75ecc2c69e0e99847e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9c99dece94c5a563168e2978c700f15b6831064c92d93c3903815369ae2d1a81d4e0d8a280d6b65f00df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f6421a43c89527accb13a8f8bc44c0f353f1a9afb448c9611b8c080393b6e127dbba00594a1bd53a660e6233a985e80aa28afb04ec07e43a120cfb0fb526bb39450a46b8ae4e81acb9fa46b8ae4e81acb9fadc0d86d9e44006d8b4d7926e9ef7a8c2b062cda5fe463b4f2da10fb74cac1eab2da10fb74cac1eaba5d9b37818eab7b0a1a4f6d22df17006a44a72275ee79654',
    '_buzz_aidata': 'JTdCJTIydWZwJTIyJTNBJTIyMDlIS01PQlB4UlVkT2hLaGlVUTk5dyUyMiUyQyUyMmJyb3dzZXJWZXJzaW9uJTIyJTNBJTIyMTQ5LjAlMjIlMkMlMjJ0c0NyZWF0ZWQlMjIlM0ExNzgwOTMyODI1Njc3JTdE',
    '_buzz_mtsa': 'JTdCJTIydWZwJTIyJTNBJTIyNGUxNGU5YWQ2MTgwNDljZWFkZTNmZTQ3NjJiNzUzNWMlMjIlMkMlMjJicm93c2VyVmVyc2lvbiUyMiUzQSUyMjE0OS4wJTIyJTJDJTIydHNDcmVhdGVkJTIyJTNBMTc4MDkzMjgyNDI2NCU3RA==',
    'ft': '"qBNztO0ALfnBaBzy4VQDiZvJRATK4bAG6Rtn5TIIwfI4DdDMxZZcuNDbqbhQZcCD6CW8rwrxo0PqmCbSLZ+7nShJqOLEoJ2vbCpznvalpmgSuntSsSCkqqjx7ZeyiIpC8MGFK1FSR93OJVk1NL/kUg=="',
    'tmr_detect': '0%7C1780932829251',
    '_adcc': '2.Qmt149XHISRthVlynquAi+AyJulqbhaOncWANwmlK2nSJ1DCjGwsEHRyq3pR92Q4hCqa9yhtIs8wu5S2A+uDd9O2k0jxKvAa43Bwsvym1Hayy7ItLhD6JeaPMjzJRJwR9ME0zV9myvrDCC2/6JEUq5YvGpiQ',
    'csprefid': '97880f0a-11d6-4427-b4bb-8a871d144db9',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_wEmANn_YToxOntzOjE6InkiO3M6MTY6IlFmY2tHdXg5UVl6WTBieHUiO33K-cy0JgAAAA&f=ASgBAgICAkSSA8YQkL4Nlq41&i=1&p=2',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-source': 'client-browser',
    # 'cookie': 'srv_id=Gb6Fbx7syC7LYy8t.jYvIB-wUSRkcTmceXH4pn9zZVfdze23ZHsmYi0exT35flimYd7rPKb5yZ-5seBk=.26yBxWLRrZ-tm0iy-6Ah-hqesd5YHu7AsEIxLemnUqE=.web; _avisc=X92YRW9wgisQUX6avuJxhcrlGrC9W5bG9gJdat2/vF8=; u=3bpzd62a.1l1blx.ymfdyb1js200; v=1780932810; h_u=fba9ad8efced2bb2:1780932780; selected_locale=ru-RU; _gcl_au=1.1.1955744551.1780932811; _ga=GA1.1.1765901951.1780932812; cssid=e5cb9e02-dc6b-4a59-9135-b12b00d7b1d9; cssid_exp=1780934612038; _ym_uid=1780932813814473936; _ym_d=1780932813; cookie_consent_shown=1; _ym_isad=2; luri=moskva; buyer_location_id=637640; _ym_visorc=b; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; ma_id_api=k5dgGahBF6xn8morr02075wvMGXm7UT/3MtIfJrhEbdqsT7sOIKaLL4VtE51x+Sml98uM6yBIYIMj5CKjKH0InNTfMKycU+T0Hcv/cLfP8U6tFZWjkSzLbct8rjaWfvaocUABNRRYib0DqAT7HiWm1wAT1yTsrjlsoM5/iOq9xJVz5l5/XpM+TR8yTEBd0XE7aP4DvzdQeS+25oG3sz6MygsGSxzcHthuZSGbXi45NUTLoIb/CbKwltDuj991YLc73NTcJgVfjDOn4fEN39JM2J+rfq2UnSUfzfasiv0lqEQlr8XMrlj9XZ8mIVmhpEizcvuRg8dnw2UrdqaiwcqCA==; tmr_lvid=28d77703c279a2a9a1db42f152d89865; tmr_lvidTS=1780932817796; adrdel=1780932817803; adrdel=1780932817803; adrcid=APu4BCRWelBbzwV_SPdwf5g; adrcid=APu4BCRWelBbzwV_SPdwf5g; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1781019217813%2C%22sl%22%3A%7B%22224%22%3A1780932817813%2C%221228%22%3A1780932817813%7D%7D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1781019217813%2C%22sl%22%3A%7B%22224%22%3A1780932817813%2C%221228%22%3A1780932817813%7D%7D; domain_sid=QOE2hQdHwoZGihqoqA7QQ%3A1780932817979; uxs_uid=6bae0950-634f-11f1-93e8-4f04af640159; __upin=09HKMOBPxRUdOhKhiUQ99w; ma_id=6322120861780932813192; _ga_M29JC28873=GS2.1.s1780932811$o1$g1$t1780932822$j49$l0$h0; sx=H4sIAAAAAAAC%2FwTAqw6DMBgF4Hc5emKn%2By9t3dS2ZIBCYClFk5Bgmr47X4O%2FkvimLCa%2BC2mmKkZfK72WpMgNFzL0%2FTmXadafj%2FH7Hw48UJHpkU%2BmENj7HQAA%2F%2F8EIbnNTAAAAA%3D%3D; __ai_fp_uuid=131e0b86379cf11a%3A2; buyer_from_page=catalog; f=5.0c4f4b6d233fb906b75ecc2c69e0e99847e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a7b0d53c7afc06d0b2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9c99dece94c5a563168e2978c700f15b6831064c92d93c3903815369ae2d1a81d4e0d8a280d6b65f00df103df0c26013aba0ac8037e2b74f9268a7bf63aa148d20df103df0c26013a8b1472fe2f9ba6b97b0d53c7afc06d0b71e7cb57bbcb8e0f03c77801b122405c03c77801b122405c03c77801b122405c2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f6421a43c89527accb13a8f8bc44c0f353f1a9afb448c9611b8c080393b6e127dbba00594a1bd53a660e6233a985e80aa28afb04ec07e43a120cfb0fb526bb39450a46b8ae4e81acb9fa46b8ae4e81acb9fadc0d86d9e44006d8b4d7926e9ef7a8c2b062cda5fe463b4f2da10fb74cac1eab2da10fb74cac1eaba5d9b37818eab7b0a1a4f6d22df17006a44a72275ee79654; _buzz_aidata=JTdCJTIydWZwJTIyJTNBJTIyMDlIS01PQlB4UlVkT2hLaGlVUTk5dyUyMiUyQyUyMmJyb3dzZXJWZXJzaW9uJTIyJTNBJTIyMTQ5LjAlMjIlMkMlMjJ0c0NyZWF0ZWQlMjIlM0ExNzgwOTMyODI1Njc3JTdE; _buzz_mtsa=JTdCJTIydWZwJTIyJTNBJTIyNGUxNGU5YWQ2MTgwNDljZWFkZTNmZTQ3NjJiNzUzNWMlMjIlMkMlMjJicm93c2VyVmVyc2lvbiUyMiUzQSUyMjE0OS4wJTIyJTJDJTIydHNDcmVhdGVkJTIyJTNBMTc4MDkzMjgyNDI2NCU3RA==; ft="qBNztO0ALfnBaBzy4VQDiZvJRATK4bAG6Rtn5TIIwfI4DdDMxZZcuNDbqbhQZcCD6CW8rwrxo0PqmCbSLZ+7nShJqOLEoJ2vbCpznvalpmgSuntSsSCkqqjx7ZeyiIpC8MGFK1FSR93OJVk1NL/kUg=="; tmr_detect=0%7C1780932829251; _adcc=2.Qmt149XHISRthVlynquAi+AyJulqbhaOncWANwmlK2nSJ1DCjGwsEHRyq3pR92Q4hCqa9yhtIs8wu5S2A+uDd9O2k0jxKvAa43Bwsvym1Hayy7ItLhD6JeaPMjzJRJwR9ME0zV9myvrDCC2/6JEUq5YvGpiQ; csprefid=97880f0a-11d6-4427-b4bb-8a871d144db9',
}

params = {
    'categoryId': '24',
    'locationId': '637640',
    'i': '1',
    'cd': '0',
    'p': '0',
    'params[201]': '1059',
    'params[110472]': '437131',
    'verticalCategoryId': '1',
    'rootCategoryId': '4',
    'localPriority': '0',
    'updateListOnly': 'true',
    'context': 'H4sIAAAAAAAA_wEmANn_YToxOntzOjE6InkiO3M6MTY6IlFmY2tHdXg5UVl6WTBieHUiO33K-cy0JgAAAA',
}

result = []
response = requests.get('https://www.avito.ru/web/1/js/items', params=params, cookies=cookies, headers=headers)

print(response.status_code)
items = response.json()['catalog']['items']
for item in items:
    try:
        if item['type'] == 'banner':
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

df = pd.DataFrame(result)
df.to_excel('avito.xlsx', index=False)

