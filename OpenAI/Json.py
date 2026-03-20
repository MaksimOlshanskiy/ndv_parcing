from selenium import webdriver
import json

def making_list_of_urls(corpus_id):
    driver = webdriver.Chrome()
    try:
        url_list = []

        url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/construction/progress/photo/{corpus_id}'
        driver.get(url=url)

        json_text = driver.find_element("tag name", "body").text
        data = json.loads(json_text)

        for i in data:
            date = i['objPeriodDt']
            link = i['objPhotoUrl']
            url_list.append([date, link])

        return url_list

    finally:
        driver.quit()  # закрываем браузер, даже если будет исключение





