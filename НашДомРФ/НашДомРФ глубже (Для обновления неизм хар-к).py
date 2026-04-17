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

proxy_host = "89.23.114.250"
proxy_port = "17331"
proxy_user = "e0gdcKM8OS"
proxy_pass = "8C0r1I3U7R"

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





def convert_quarter(text: str) -> str:
    roman_to_int = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4
    }

    for roman, arabic in roman_to_int.items():
        if text.startswith(roman):
            # удаляем " кв." или " кв. "
            rest = text.replace(f"{roman} кв.", "").replace(f"{roman} кв. ", "")
            return f"{arabic} кв {rest.strip()}"

    return text  # если формат не совпал

cookies = {
    'spid': '1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3',
    '_ym_uid': '1741679472430329696',
    'tmr_lvid': '21dd9990a0516763e1af5efdddfe2ece',
    'tmr_lvidTS': '1741679492626',
    '___dmpkit___': 'a4186694-8f1a-4c72-a444-15171df726ff',
    '_ym_d': '1757920713',
    'spjs': '1763471574517_02f93493_013501e8_8f0b3b874fce18ec51ebb135a76ec58b_c0R5YGTsV2e6g14u40DmpDQR7osRwjR1mPDcOv/WHyNWLqoqb0YQbeXseXh81RjQpSuHJ2rJbs+S2tY0cMEcTRGI1YQowApmn9ZzcnbfFapfJYEhZMe4eZzU0D56W4ZHa4LPI/JrNbU5kNM8oejE5CmFWzpfF5LzOV7Zi71nklITH0ub7xIJyeD9RGWJRLhIFG/m01pXD2+D7mdAodmKa24sgrL2TzvvjrYio5e/zi4aZcm5QGhFlTmB3b732uZGD2PfqlYuAGI9f2mITk7iczd8Wct9F7LjN89+FJig/OxweUDlHHGOfrKfBiLL04oPs1TVwEQpTImextIg9c47ai6ShvMnD5H07cDJbeT55QVJUpu+Ilpngp6jOn2cwYDnFQ3s6Q3VgnKG/kq+z1fmBhdo1NQIwHiNxJxlRp+X/htXbASkegQO664vcxJ+vtvMytMmB+OL3vpP1rMt8U7h8d1EKdlATvCnupJfz/N6kRKu7LjozUCRgfQcXj76w1c0Q1r8HusG7LyA+bQVmMAa2rdNAWe7R9p6BtpQVaH5LZmtAuQlULjPu06WEgIXzntq3wHamWUtAcAocQ0egyqmBxlAXC1wirMDN54LKvbFY7I2DdmrfUYwtcIauxTYYd/PZC2Ec18TPbqW24ABqeDKOtLTp4JXaD27ntAEwyCYqEkbUjSgcO8HZ7qjKlhkLNCRTTB9KUfOMhJuFwr6XxPllcF4HPh6cJbHQ1sIiEgiZyXAGdOAXVX4q5LK1jT5lD1NsS7UotkzKPjslEAxtY25KS1W8oJWDlv7n6dDPNTLkMSroukt8Ss1xtrDXS5Qy7QRTpk97YgwIULVncjK/yaVQdYfm4qfRvyc8MgVxemhqu43qaHjLnerqkeAdDNDuW2dScCApuCoKwE9lngA5EwXxzTL//5wQTb2sCJPDXT4tUW5Efzs8FkT8jZNWyh+xLVSlj3JqXxI8MKV7EgX6+Off3NKxrZqUh3Nkcl1BNjDbF6RZ9Ozd38K6r62YhHF/ZlpDQTgoHR8J+Sas9//8ksWtDqDfT4CaofHmwPfuIxnU7M3Dt6rLkYZ4kQNTQi608cmwCuRQY2lSs70nQFjDeHbi8fuhgYYy/vKP4VzEubemMr+hdChdM0a6L4EUy/wy5THe4LfrnZKEWW8gW4JUGpU5WkP+ittRkBjhY55qfnFleEwDN0IK2NNOpbdVyB6xZ5ps1HVtXHBDOWwmGUuJ+26q5/ShfVQuR+7SVOmFsI76UgbJI4PAGnAoCz0yW99Bnqaxv8jU4+4AEcnLqui/jeZ4reF2Vt1xZJBokpOwbz1qXg1WAGhXNTL+pYYdERwwG1nIHYDoXmrWLq6gJZjfc1qYb2FcBD1zRZma4NXLQDKhGsaJfaNUGh0RN5nOr25UYJDNq69rGlwJ/d3rVuo/WxAcLQq9uMNteiYdNhSsx/zf2+17bAwPNQJehqzR8aCCshouuC1NTHZCiq4YTS7t1+FY01WuFlUfEfhzMNeP/P7lma7CFiofEQR9vWNSLv5gwZHYzubnD9XDejUvqRzCcCZaQf6gFZ7gxivhMtHMWXvXh1pImQ1NEtvv5nxk4CRus5MipScp3tLBWe+jbHdw+uTQ2pT799WG1CQNMx4vM3FseRgPkr6/hMj5qcKCzHdkI3kMzl2JmpSDf2hmUUw3VA/zbAP26NvRxryv45TIbtN6cm8BdAA9IQf5/RMoNECspZOOiFVpXlBFGVQgV3rd8eLazcm2iJ+wh4eRbx5CXzFMTAkG8e3e1MO/rKKRiX5wZ1tMQjUpHpAD02/BUID9kaSZTH1IK9vVmk5MpqvPlLql+8zDdFeg0Sq78vA1FIauXXE+IMQNuLt0qO/FfIY/0CSQVWMyahtxAvkQ55Y1u9iPu4zCdQle0EebLao9P39d+8qbDXjFlDCFn3ojqqaO/DrXewP2hs1SWBGvaNYs77ZdDE0s+to1Xtk/1YOU=',
    'domain_sid': 'p9NEOoC7wfYKTfSohYE69%3A1763471581292',
    'spsc': '1763538114091_0df2f6bc4e2b6141bff199e3478158b0_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3745525d5f4f58455e445a4a423660',
    'tmr_detect': '0%7C1763539348930',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic MTpxd2U=',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8/?place=0',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; ___dmpkit___=a4186694-8f1a-4c72-a444-15171df726ff; _ym_d=1757920713; spjs=1763471574517_02f93493_013501e8_8f0b3b874fce18ec51ebb135a76ec58b_c0R5YGTsV2e6g14u40DmpDQR7osRwjR1mPDcOv/WHyNWLqoqb0YQbeXseXh81RjQpSuHJ2rJbs+S2tY0cMEcTRGI1YQowApmn9ZzcnbfFapfJYEhZMe4eZzU0D56W4ZHa4LPI/JrNbU5kNM8oejE5CmFWzpfF5LzOV7Zi71nklITH0ub7xIJyeD9RGWJRLhIFG/m01pXD2+D7mdAodmKa24sgrL2TzvvjrYio5e/zi4aZcm5QGhFlTmB3b732uZGD2PfqlYuAGI9f2mITk7iczd8Wct9F7LjN89+FJig/OxweUDlHHGOfrKfBiLL04oPs1TVwEQpTImextIg9c47ai6ShvMnD5H07cDJbeT55QVJUpu+Ilpngp6jOn2cwYDnFQ3s6Q3VgnKG/kq+z1fmBhdo1NQIwHiNxJxlRp+X/htXbASkegQO664vcxJ+vtvMytMmB+OL3vpP1rMt8U7h8d1EKdlATvCnupJfz/N6kRKu7LjozUCRgfQcXj76w1c0Q1r8HusG7LyA+bQVmMAa2rdNAWe7R9p6BtpQVaH5LZmtAuQlULjPu06WEgIXzntq3wHamWUtAcAocQ0egyqmBxlAXC1wirMDN54LKvbFY7I2DdmrfUYwtcIauxTYYd/PZC2Ec18TPbqW24ABqeDKOtLTp4JXaD27ntAEwyCYqEkbUjSgcO8HZ7qjKlhkLNCRTTB9KUfOMhJuFwr6XxPllcF4HPh6cJbHQ1sIiEgiZyXAGdOAXVX4q5LK1jT5lD1NsS7UotkzKPjslEAxtY25KS1W8oJWDlv7n6dDPNTLkMSroukt8Ss1xtrDXS5Qy7QRTpk97YgwIULVncjK/yaVQdYfm4qfRvyc8MgVxemhqu43qaHjLnerqkeAdDNDuW2dScCApuCoKwE9lngA5EwXxzTL//5wQTb2sCJPDXT4tUW5Efzs8FkT8jZNWyh+xLVSlj3JqXxI8MKV7EgX6+Off3NKxrZqUh3Nkcl1BNjDbF6RZ9Ozd38K6r62YhHF/ZlpDQTgoHR8J+Sas9//8ksWtDqDfT4CaofHmwPfuIxnU7M3Dt6rLkYZ4kQNTQi608cmwCuRQY2lSs70nQFjDeHbi8fuhgYYy/vKP4VzEubemMr+hdChdM0a6L4EUy/wy5THe4LfrnZKEWW8gW4JUGpU5WkP+ittRkBjhY55qfnFleEwDN0IK2NNOpbdVyB6xZ5ps1HVtXHBDOWwmGUuJ+26q5/ShfVQuR+7SVOmFsI76UgbJI4PAGnAoCz0yW99Bnqaxv8jU4+4AEcnLqui/jeZ4reF2Vt1xZJBokpOwbz1qXg1WAGhXNTL+pYYdERwwG1nIHYDoXmrWLq6gJZjfc1qYb2FcBD1zRZma4NXLQDKhGsaJfaNUGh0RN5nOr25UYJDNq69rGlwJ/d3rVuo/WxAcLQq9uMNteiYdNhSsx/zf2+17bAwPNQJehqzR8aCCshouuC1NTHZCiq4YTS7t1+FY01WuFlUfEfhzMNeP/P7lma7CFiofEQR9vWNSLv5gwZHYzubnD9XDejUvqRzCcCZaQf6gFZ7gxivhMtHMWXvXh1pImQ1NEtvv5nxk4CRus5MipScp3tLBWe+jbHdw+uTQ2pT799WG1CQNMx4vM3FseRgPkr6/hMj5qcKCzHdkI3kMzl2JmpSDf2hmUUw3VA/zbAP26NvRxryv45TIbtN6cm8BdAA9IQf5/RMoNECspZOOiFVpXlBFGVQgV3rd8eLazcm2iJ+wh4eRbx5CXzFMTAkG8e3e1MO/rKKRiX5wZ1tMQjUpHpAD02/BUID9kaSZTH1IK9vVmk5MpqvPlLql+8zDdFeg0Sq78vA1FIauXXE+IMQNuLt0qO/FfIY/0CSQVWMyahtxAvkQ55Y1u9iPu4zCdQle0EebLao9P39d+8qbDXjFlDCFn3ojqqaO/DrXewP2hs1SWBGvaNYs77ZdDE0s+to1Xtk/1YOU=; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1763471581292; spsc=1763538114091_0df2f6bc4e2b6141bff199e3478158b0_YFFv8xBSXhZdrc7.EyCpz3Jm33T58AS4t2c9Ap-PXdAZ; _ym_isad=2; _ym_visorc=b; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3745525d5f4f58455e445a4a423660; tmr_detect=0%7C1763539348930',
}

params = {
    'offset': '0',
    'limit': '20',
    'sortField': 'obj_publ_dt',
    'sortType': 'desc',
    'place': '0-67',
    'objStatus': '0',
}

buildings_id = ['50448', '50695', '54383', '54348', '54377', '44964', '50420', '56693', '50270', '51056', '53591', '53592', '54680', '58299', '58298', '59538', '56102', '56795', '53523', '53519', '53521', '53522', '54578', '54580', '54581', '54582', '54583', '54579', '52712', '53498', '52381', '54293', '54294', '58804', '54897', '46687', '58243', '46646', '46644', '58803', '25173', '59328', '54298', '54299', '57919', '58132', '51566', '61266', '56394', '56750', '60525', '60526', '60527', '63957', '51894', '62265', '50893', '58289', '53542', '53543', '54533', '56341', '55472', '59327', '50144', '56974', '56866', '57033', '55644', '36234', '51091', '62732', '58217', '51119', '67094', '57805', '56862', '55433', '58064', '51108', '51450', '51452', '63646', '58524', '32274', '58133', '54218', '54219', '54220', '54723', '54724', '54725', '55205', '57179', '37859', '49357', '57478', '54577', '56544', '59150', '62044', '59896', '59629', '59628', '56944', '56945', '56949', '61484', '59753', '66809', '66807', '66808', '54518', '59210', '<NA>', '56304', '56305', '56306', '56307', '58776', '58775', '56212', '64936', '59683', '68122', '54102', '48693', '48694', '57291', '57355', '51725', '52567', '54984', '53635', '54281', '54454', '59391', '62793', '62839', '62840', '62841', '37984', '61312', '51560', '55142', '53713', '59440', '59326', '57881', '57882', '57883', '57884', '57885', '60229', '56266', '55760', '58281', '62498', '59213', '59157', '59237', '51766', '55028', '60176', '60177', '60178', '53590', '60247', '53874', '59966', '59967', '57849', '56363', '42833', '42834', '44411', '44969', '62137', '62138', '51928', '19620', '56452', '56715', '58802', '47579', '37322', '37324', '55218', '64568', '53748', '53988', '44603', '54616', '52713', '58644', '56842', '54394', '32319', '62401', '24534', '24535', '40687', '40688', '62843', '62055', '60896', '60421', '62547', '63222', '69086', '59365', '59367', '64123', '61251', '62414', '5209', '31015', '64126', '68291', '64204', '61588', '56725', '58301', '53464', '53370', '59934', '59146', '59147', '56234', '57817', '61674', '61521', '66399', '66400', '53359', '55796', '66003', '63969', '56269', '56270', '55421', '61676', '61675', '51881', '66910', '65561', '64587', '67732', '67731', '67735', '67733', '67314', '66547', '43322', '57752', '53661', '52870', '45970', '58312', '58168', '62728', '55198', '48767', '47431', '64446', '60880', '61714', '28290', '28291', '32140', '37183', '64029', '64104', '61311', '60622', '60486', '61323', '59759', '50325', '61276', '56210', '62789', '51818', '63895', '63896', '56031', '56036', '64768', '59595', '51432', '62503', '65114', '64620', '64622', '64621', '64627', '57807', '63031', '59540', '59897', '50327', '60011', '59887', '51623', '51741', '45826', '49777', '59370', '62103', '58232', '61088', '64096', '39481', '61562', '59212', '59685', '53382', '56157', '56514', '68181', '60790', '63047', '66212', '57447', '64520', '63900', '63789', '63754', '63787', '63901', '63755', '64805', '64806', '64807', '65723', '59144', '62614', '65023', '64641', '58488', '65463', '31910', '31911', '31912', '31913', '63685', '63048', '63049', '63051', '63052', '63053', '63055', '63056', '63050', '63054', '67384', '62247', '69153', '61842', '61843', '43708', '61294', '63497', '65533', '67507', '63629', '43709', '55420', '57838', '63924', '55387', '61303', '59686', '59598', '60564', '66746', '65460', '67099', '60533', '60712', '66869', '59756', '68618', '59507', '67209', '60548', '64219', '56950', '56951', '62069', '63821', '66052', '63450', '63045', '65373', '58489', '63925', '65182', '65183', '63732', '63804', '63805', '63686', '63731', '61422', '69387', '59506', '62677', '62590', '57362', '66013', '65141', '58300', '64065', '65192', '63948', '63659', '64003', '64566', '58256', '61610', '62087', '28074', '66132', '64494', '61221', '62038', '65249', '65371', '68503', '56264', '60532', '56265', '60425', '64454', '64932', '64933', '67679', '57448', '63949', '63962', '63603', '58828', '65455', '67972', '66131', '53747', '62431', '65901', '44142', '52082', '67276', '65465', '66793', '66240', '60872', '65944', '67620', '56687', '63966', '62293', '66801', '65419', '27247', '27248', '27250', '66274', '62039', '65248', '63015', '68396', '69433', '69524', '63594', '68513', '62556', '64808', '64244', '66661', '64921', '64596', '67723', '59505', '66234', '68144', '68264', '63029', '68831', '56224', '68929', '68901', '69352', '64983', '65338', '68001', '66710', '68014', '66520', '67396', '68275', '62125', '58150', '66931', '66480', '67067', '69675', '65452', '52790', '68781', '53669', '66008', '69179', '64985', '68821', '1688', '1689', '11446', '35601', '37418', '37417', '20033', '38377', '38163', '3373', '48486', '46826', '42009', '48278', '53175', '38823', '43955', '48736', '46173', '46174', '43633', '43699', '43359', '30782', '30783', '37714', '29419', '29414', '49763', '49764', '51453', '51454', '51511', '49870', '49819', '50610', '39040', '55781', '58597', '56792', '39041', '39042', '27749', '53467', '53468', '40632', '40465', '16222', '25172', '24279', '42772', '16128', '16127', '36569', '36570', '31042', '37819', '37820', '26835', '36567', '25400', '37024', '38388', '7482', '39566', '39567', '62998', '22945', '42908', '43879', '43707', '31626', '40640', '37715', '42855', '28577', '44483', '28576', '32325', '32326', '44481', '44482', '40279', '46127', '46066', '43864', '27921', '27917', '27918', '27916', '27919', '27923', '27920', '49580', '45822', '64840', '64841', '48298', '46925', '51310', '12092', '65496', '51315', '48257', '46429', '44676', '44675', '41018', '47012', '47013', '41764', '29420', '46357', '9604', '45009', '48071', '52451', '52452', '52453', '52454', '49871', '49678', '30182', '25799', '19142', '30475', '41180', '48915', '34848', '48613', '27748', '37645', '34125', '20977', '19430', '7706', '36920', '34180', '26038', '44069', '46532', '46536', '46539', '40325', '45959', '37342', '37202', '25870', '37646', '45604', '37004', '45197', '45199', '45203', '37647', '50307', '38951', '47065', '47061', '47067', '47066', '47059', '47063', '46588', '9601', '9602', '9603', '45065', '44858', '39826', '23196', '69291', '27843', '27927', '49564', '45205', '43667', '45349', '68887', '58854', '57194', '44330', '44331', '44332', '51002', '57750', '49696', '52949', '47112', '48124', '48125', '44387', '53577', '48466', '56531', '56533', '57119', '51415', '51388', '50516', '50517', '50764', '50234', '50235', '50236', '47502', '47503', '45219', '50442', '47154', '49609', '49610', '49608', '58855', '46292', '51771', '48620', '50135', '50136', '50132', '50133', '50134', '49794', '46649', '48996', '47786', '51996', '45060', '45061', '50536', '50537', '51192', '37622', '37623', '45998', '52146', '52147', '49606', '61741', '61740', '25663', '29553', '21486', '40685', '27752', '65525', '21358', '65834', '7708', '37556', '37555', '37554', '27738', '41549', '37487', '41182', '32318', '45081', '45082', '62494', '19561', '40855', '42441', '65513', '70050', '43749', '40380', '40381', '46585', '46586', '40165', '45631', '37967', '65703', '63354', '41606', '45473', '70051', '43253', '23185', '23186', '27926', '27928', '42714', '43668', '44841', '25802', '25801', '25260', '47464', '43779', '50682', '38022', '29997', '29999', '39321', '35358', '63359', '70052', '60273', '55103', '50150', '50152', '50153', '50154', '39483', '39482', '39485', '23773', '29438', '43820', '45596', '48581', '48578', '49494', '48577', '48580', '49495', '38367', '24926', '26141', '35466', '24222', '47770', '44510', '46537', '34307', '48522', '46540', '46118', '44775', '44777', '28315', '7910', '45882', '25407', '25405', '47685', '18422', '48981', '48583', '40373', '47907', '37541', '44093', '44095', '43451', '43836', '52788', '48535', '28978', '56296', '38361', '38364', '50148', '10884', '45908', '43264', '43267', '46019', '46021', '46020', '41475', '41476', '1286', '20461', '46432', '39825', '40410', '22643', '22644', '31981', '45498', '40359', '44354', '44356', '47625', '12328', '47132', '46638', '61985', '43381', '39214', '39215', '1838', '46851', '11572', '45958', '47540', '37971', '39712', '45354', '44857', '37721', '37717', '37718', '37719', '37720', '27291', '27295', '27296', '34072', '27292', '27293', '27294', '34073', '34074', '34075', '36580', '24702', '20007', '57474', '24472', '37014', '45630', '36877', '44867', '44868', '27741', '44770', '40231', '40232', '44767', '40233', '30548', '30549', '30543', '30544', '30545', '30546', '30547', '45404', '50909', '42922', '42923', '42914', '42921', '37275', '47084', '42266', '44338', '40363', '40163', '46220', '34549', '41967', '43153', '49925', '45318', '37270', '42764', '50740', '50326', '46601', '68245', '50363', '50364', '50365', '41352', '52220', '52221', '52222', '52223', '52224', '52350', '49932', '49933', '55874', '30231', '54355', '54356', '52950', '48389', '48946', '52641', '57962', '58598', '51416', '55115', '56436', '55116', '52142', '59656', '53066', '46091', '48184', '28075', '28076', '28077', '28078', '54862', '50519', '50890', '50891', '50581', '50493', '50494', '47336', '47337', '47338', '51274', '52267', '53620', '53978', '46860', '46859', '52375', '50158', '52662', '52346', '52347', '52348', '52349', '40964', '47436', '34850', '47447', '25682', '56494', '49684', '57841', '34852', '13616', '13617', '41982', '44647', '44511', '44512', '25183', '47383', '44436', '46733', '39428', '45972', '40334', '12246', '42662', '47076', '44165', '43313', '43314', '44393', '47990', '63504', '45973', '63064', '5210', '21857', '45276', '54521', '47486', '50268', '53897', '56214', '57918', '54864', '58588', '39827', '49356', '54036', '54037', '54038', '54039', '56672', '56674', '56673', '55393', '56513', '44965', '44893', '44894', '55701', '42557', '51572', '64073', '54489', '54490', '54482', '54483', '55034', '55035', '55036', '54628', '52455', '52456', '44769', '44476', '52711', '57465', '37318', '56028', '55109', '51567', '55312', '46310', '45192', '53658', '56623', '48808', '57963', '53790', '55633', '56965', '59789', '62749', '50975', '50976', '55686', '55687', '51949', '54528', '58714', '58713', '46163', '58759', '51374', '28072', '58110', '44596', '57479', '57480', '57481', '57482', '57483', '57484', '57485', '57486', '57487', '57488', '57489', '55469', '55470', '69773', '67730', '48352', '43199', '51053', '49325', '51308', '48706', '53516', '45185', '66242', '45184', '46510', '45977', '50269', '53618', '49291', '49099', '50237', '50238', '46238', '50218', '54980', '49532', '46281', '52951', '40159', '41332', '50651', '45969', '55165', '55166', '55594', '55595', '56502', '55432', '59215', '47219', '59036', '58056', '45298', '58201', '45519', '48243', '49470', '49360', '30977', '36389', '42848', '42849', '51218', '54449', '54450', '54313', '54314', '54315', '54316', '55224', '56356', '59184', '53889', '53150', '56694', '49226', '25993', '25372', '54931', '53142', '44125', '53581', '47909', '48259', '54860', '27243', '52063', '54505', '54541', '56071', '57792', '48266', '53411', '53412', '53413', '51503', '47114', '29421', '47690', '51437', '51438', '51439', '51440', '51055', '39716', '45888', '53596', '46647', '46648', '50407', '50408', '50409', '46278', '64340', '49393', '55419', '44768', '48563', '40634', '50214', '54895', '46305', '49942', '44140', '57906', '58482', '58481', '58480', '58483', '58479', '56898', '56899', '56932', '56933', '56062', '56063', '64205', '9607', '58111', '64082', '50049', '44646', '57808', '51394', '51395', '57008', '57009', '47384', '55422', '61267', '57490', '57491', '57496', '67728', '68200', '30640', '30090', '36169', '68806', '41016', '69549', '69489', '60457', '69149', '612944452', '70198', '48547', '64071', '64072', '64084', '58507', '70095', '44648', '47382', '69508', '54791', '70357', '67708', '51237', '70778', '69138', '69962', '69088', '68221', '68222', '68196', '68198', '70009', '70382', '69431', '41014', '46307', '61654', '70548', '69275', '50291', '66103', '62896', '69384', '64430', '67146', '69663', '64462', '64595', '69718', '65566', '58464', '48353', '50200', '69199', '67205']

flats = []
problem_id = []
current_date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

for building_id in buildings_id:



    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/{building_id}'

    driver.get(url)
    print(driver.title)
    print(driver.current_url)

    wait = WebDriverWait(driver, 10)

    # ждем появления нужных элементов
    element = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[text()='Все характеристики']")
        )
    )

    driver.execute_script("arguments[0].click();", element)

    page_content = driver.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    info = soup.find_all('h5', class_=["_heading_7t2en_1 _h5_7t2en_74", 'CharacteristicsBlock__Value-sc-1fyyfia-9', 'ciMWMC'])
    i = []
    for inf in info:

        i.append(inf.text)

    print(i)


    if len(i) == 3:  # сданный проект
        developer = i[0]
        developer_group = 'Сдан'
        project_declaration = i[1]
        publication_date = 'Сдан'
        explotation_start_date = i[2]
        keys_date = 'Сдан'
        avg_metr_price = 'Сдан'
        flats_sales_perc = 'Сдан'
    if len(i) == 4:  # сданный проект
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[2]
        publication_date = 'Сдан'
        explotation_start_date = i[3]
        keys_date = 'Сдан'
        avg_metr_price = 'Сдан'
        flats_sales_perc = 'Сдан'
    if len(i) == 5:   # сданный проект
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[2]
        publication_date = 'Сдан'
        explotation_start_date = i[4]
        keys_date = 'Сдан'
        avg_metr_price = 'Сдан'
        flats_sales_perc = 'Сдан'
    if len(i) == 8:
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[2]
        publication_date = i[3]
        explotation_start_date = i[4]
        keys_date = i[5]
        avg_metr_price = i[6]
        flats_sales_perc = i[7]
    if len(i) == 9:
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[3]
        publication_date = i[4]
        explotation_start_date = i[5]
        keys_date = i[6]
        avg_metr_price = i[7]
        flats_sales_perc = i[8]
    if len(i) == 7:
        developer = i[0]
        developer_group = '-'
        project_declaration = i[1]
        publication_date = i[2]
        explotation_start_date = i[3]
        keys_date = i[4]
        avg_metr_price = i[5]
        flats_sales_perc = i[6]
    if soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY') and len(i) == 6:
        developer = i[0]
        developer_group = '-'
        project_declaration = i[1]
        publication_date = i[2]
        explotation_start_date = soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY').text
        keys_date = i[3]
        avg_metr_price = i[4]
        flats_sales_perc = i[5]
    if soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY') and len(i) == 7:
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[2]
        publication_date = i[3]
        explotation_start_date = soup.find('div', class_='Row__Value-sc-13pfgqd-2 ClvkY').text
        keys_date = i[4]
        avg_metr_price = i[5]
        flats_sales_perc = i[6]




    dop_info = driver.find_elements(
        By.XPATH,
        "//p[contains(@class, 'paragraphBold2')]"
    )
    i = []
    for inf in dop_info:



        i.append(inf.text)
    print(i)
    klass = i[1]
    material = i[3]
    finish_type = i[5].replace('\xa0', ' ')
    is_free_plan = i[7]
    floors_count = i[9]
    flats_count = i[11]
    living_area = i[13].replace(' ', '')
    roofs_height = i[15]
    bike_paths = i[17]
    playgrounds_count = i[19]
    sports_grounds_count = i[21]
    garbage_collection_sites_count = i[23]
    parking_place_count = i[25]
    guest_places_inside = i[27]
    guest_places_outside = i[29]
    pandus = i[31]
    low_places = i[33]
    wheelchair_lifts_count = i[35]
    entrances_count = i[37]
    passenger_elevators_count = i[39]
    freight_and_passenger_elevators_count = i[41]

    res = [int(building_id), developer, developer_group, project_declaration, publication_date, explotation_start_date.replace('IV', '4').replace('III', '3').replace('II', '2').replace('I', '1').replace('.', ''), keys_date, avg_metr_price, flats_sales_perc, klass, material,
           finish_type, is_free_plan, floors_count, flats_count, living_area, roofs_height, bike_paths, playgrounds_count, sports_grounds_count, garbage_collection_sites_count, parking_place_count, guest_places_inside,
           guest_places_outside, pandus, low_places, wheelchair_lifts_count, entrances_count, passenger_elevators_count, freight_and_passenger_elevators_count]
    print(res)
    flats.append(res)

    sleep_time = random.uniform(2, 7)
    time.sleep(sleep_time)




# Базовый путь для сохранения
base_path = r""

folder_path = os.path.join(base_path, str(current_date))
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = f"НашДомРФ_глубже_МО.xlsx"

# Полный путь к файлу
file_path = os.path.join(folder_path, filename)

df = pd.DataFrame(flats, columns=['ID дом.рф',
                                  'Застройщик',
                                  'Группа компаний',
                                  'Проектная декларация',
                                  'Дата публикации проекта',
                                  'Ввод в эксплуатацию',
                                  'Выдача ключей',
                                  'Средняя цена за 1 м²',
                                  'Распроданность квартир',
                                  'Класс недвижимости',
                                  'Материал стен',
                                  'Тип отделки',
                                  'Свободная планировка',
                                  'Количество этажей',
                                  'Количество квартир',
                                  'Жилая площадь, м²',
                                  'Высота потолков, м',
                                  'Велосипедные дорожки',
                                  'Количество детских площадок',
                                  'Количество спортивных площадок',
                                  'Количество площадок для сбора мусора',
                                  'Количество мест в паркинге',
                                  'Гостевые места на придомовой территории',
                                  'Гостевые места вне придомовой территории',
                                  'Наличие пандуса',
                                  'Наличие понижающих площадок',
                                  'Количество инвалидных подъемников',
                                  'Количество подъездов',
                                  'Количество пассажирских лифтов',
                                  'Количество грузовых и грузопассажирских лифтов'
                                  ])

# Сохранение файла в папку
df.to_excel(file_path, index=False)
print(f"Проблемные ID: {problem_id}")