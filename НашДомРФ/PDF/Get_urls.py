from selenium import webdriver
import json
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import requests
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def making_list_of_urls(corpus_id):


    proxy_host = "185.42.27.210"
    proxy_port = "10270"
    proxy_user = "STm87nUFS6"
    proxy_pass = "6StepJYs2y"

    manifest_json = """
    {
        "version": "1.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    plugin_file = "proxy_auth_plugin.zip"

    with zipfile.ZipFile(plugin_file, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    options = Options()
    options.add_extension(plugin_file)

    driver = webdriver.Chrome(options=options)
    driver.get("https://api.ipify.org")
    print(driver.page_source)

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



