import requests
import pandas as pd
import json

cookies = {
    '_ym_uid': '1782721241609193716',
    '_ym_d': '1782721241',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Authorization': 'bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMDEzMCIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWVpZGVudGlmaWVyIjoiMzAxMzAiLCJqdGkiOiJmMDQ1ZDk1Yi1mNmIzLTQyMGYtYjU1Yy02MDNkODE4MGFhMjUiLCJhZG1pbmlzdHJhdGlvbi1zZWN0aW9uLWFjY2VzcyI6IkZhbHNlIiwibGFuZExlYWQtc2VjdGlvbi1hY2Nlc3MiOiJGYWxzZSIsIm5iZiI6MTc4NDcwMzkwNywiZXhwIjoxNzg5ODg3OTA3LCJpc3MiOiJyaWNjaS50ZWNoLmlzc3VlciIsImF1ZCI6InJpY2NpLnRlY2guYXVkaWVuY2UifQ.uJe-j5gyAmcl7R9pdtj_5-J3LayLEseHnRkMwEgGbAo',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://in.ricci.ru',
    'Referer': 'https://in.ricci.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="8", "Chromium";v="150", "Google Chrome";v="150"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': '_ym_uid=1782721241609193716; _ym_d=1782721241',
}

json_data = {
    'pageSize': 10000,
    'sortColumn': 'title',
    'isDescending': 1,
    'filters': [
        {
            'property': 'date',
            'type': 'dateRange',
            'referenceType': '',
            'dateFromValue': '2020-12-31T21:00:00.000Z',
        },
    ],
    'page': 1,
    'propertiesToShow': [
        {
            'property': 'title',
            'title': 'Название',
            'type': {
                'name': 'string',
                'param': '',
            },
            'columnSelected': True,
            'columnPosition': 0,
            'filterSelected': True,
            'filterPosition': 0,
            'columnTpl': 'deal-title.tpl',
            'filterTpl': 'string.tpl',
            'isPinned': True,
        },
    ],
    'skip': 0,
}
result = []
response = requests.post('https://in.ricci.ru/api/tables/deal/search', cookies=cookies, headers=headers, json=json_data)
items = response.json()['dealsDic']
for i in items:
    title = items[i]['title'].split('-')
    buyer = title[1].strip()
    seller = title[2].strip()
    type = title[3].strip()
    building_adress = title[4].strip()
    area = items[i]['area']
    try:
        completeDate = items[i]['completeDate']
    except:
        completeDate = None
    buildingId = items[i]['buildingId']
    result.append([title, buyer, seller, type, building_adress, area, completeDate, buildingId])

print(len(result))
df = pd.DataFrame(result, columns=['title', 'buyer', 'seller', 'type', 'building_adress', 'area', 'completeDate', 'buildingId'])
df.to_excel('crm.xlsx', index=False)


