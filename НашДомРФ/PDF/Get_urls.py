from selenium import webdriver
import json

def making_list_of_urls(corpus_id):

    driver = webdriver.Chrome()
    url_list = []

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{corpus_id}/document/rpd'


    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    json_text = driver.find_element("tag name", "body").text  # Читаем текст из <body>
    data = json.loads(json_text)['data']

    for i in data:

        date = i['rpdIssueDttm']
        link = i['rpdPdfLink']
        pd_number = i['rpdNum']
        url_list.append([date, link, pd_number])

    return url_list




