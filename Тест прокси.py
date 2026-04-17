import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

driver = webdriver.Chrome(options=options)

driver.get("https://api.ipify.org")
time.sleep(20)
print(driver.find_element("tag name", "body").text)

'''
89.23.114.250:17331
e0gdcKM8OS:8C0r1I3U7R
'''