import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.vedomosti.ru',
    'Pragma': 'no-cache',
    'Referer': 'https://www.vedomosti.ru/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'X-Access-Token': '09707890e54c96debd0f603618e719a0c7cc9a2b',
    'X-Original-Referer': 'https://www.vedomosti.ru/realty',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'offset': '0',
    'limit': '13',
}
final_result = []

while True:

    response = requests.get('https://api.vedomosti.ru/v2/lists/rubrics-realty-top', params=params, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        break

    items = response.json()['list']['documents']

    if not items:
        break
    for i in items:

        title = i.get('title', '')
        date = i.get('published_at', '')
        url = i.get('url', '')

        try:
            company = i['links']['companies'][0]['bound_document']['title']
        except:
            company = ""

        print(f"Компания: {company} Заголовок: {title}   {date}  {url}")

        result = [title, date, url, company]
        final_result.append(result)

    params['offset'] = str(int(params['offset']) + 13)
    time.sleep(3)
    if int(params['offset']) >= 20:
        break

df = pd.DataFrame(final_result, columns=['Заголовок', 'Дата', 'URL', 'Компания'])

file_path = r'C:\PycharmProjects\ndv_parcing\Статьи.xlsx'

df.to_excel(file_path, index=False)







