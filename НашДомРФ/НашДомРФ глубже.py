from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random
from selenium import webdriver
import requests
import json
from bs4 import BeautifulSoup

driver = webdriver.Chrome()


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
    'searchValue': 'москва',
    'residentialBuildings': '1',
    'place': '77',
    'objStatus': '0',
}



buildings_id = ['46278', '54578', '57491', '57496', '61276', '68806', '69086', '69153', '69433', '69524', '10884', '11446', '11572', '12092', '12246', '12328', '1286', '13616', '13617', '16127', '16128', '16222', '1688', '1689', '1838', '18422', '19142', '19430', '19561', '19620', '20007', '20033', '20461', '20977', '21358', '21486', '22643', '22644', '22945', '23185', '23186', '23196', '23773', '24222', '24279', '24472', '24534', '24535', '24702', '24926', '25172', '25173', '25183', '25260', '25372', '25400', '25405', '25407', '25663', '25682', '25799', '25801', '25802', '25870', '25993', '26038', '26141', '26835', '27243', '27247', '27248', '27250', '27291', '27292', '27293', '27294', '27295', '27296', '27738', '27741', '27748', '27749', '27752', '27843', '27916', '27917', '27918', '27919', '27920', '27921', '27923', '27926', '27927', '27928', '28072', '28074', '28075', '28076', '28077', '28078', '28315', '28576', '28577', '28978', '29414', '29419', '29420', '29421', '29438', '29553', '29997', '29999', '30182', '30231', '30475', '30543', '30544', '30545', '30546', '30547', '30548', '30549', '30782', '30783', '30977', '31015', '31042', '31626', '31910', '31911', '31912', '31913', '31981', '32274', '32318', '32319', '32325', '32326', '3373', '34072', '34073', '34074', '34075', '34125', '34180', '34307', '34549', '34848', '34850', '34852', '35358', '35466', '35601', '36169', '36234', '36389', '36567', '36569', '36570', '36580', '36877', '36920', '37004', '37014', '37024', '37202', '37270', '37275', '37318', '37322', '37324', '37342', '37417', '37418', '37480', '37487', '37541', '37554', '37555', '37556', '37622', '37623', '37645', '37646', '37647', '37714', '37715', '37717', '37718', '37719', '37720', '37721', '37819', '37820', '37859', '37967', '37971', '37984', '38022', '38163', '38361', '38364', '38367', '38377', '38388', '38823', '38951', '39040', '39041', '39042', '39214', '39215', '39321', '39428', '39481', '39482', '39483', '39485', '39566', '39567', '39712', '39716', '39825', '39826', '39827', '40159', '40163', '40165', '40231', '40232', '40233', '40279', '40325', '40334', '40359', '40363', '40373', '40380', '40381', '40410', '40465', '40634', '40640', '40685', '40687', '40688', '40855', '40964', '41014', '41016', '41018', '41180', '41182', '41332', '41352', '41475', '41476', '41549', '41606', '41764', '41967', '41982', '42009', '42266', '42441', '42557', '42662', '42714', '42764', '42772', '42833', '42834', '42848', '42849', '42855', '42908', '42914', '42921', '42922', '42923', '43153', '43199', '43253', '43264', '43267', '43313', '43314', '43322', '43359', '43381', '43451', '43633', '43667', '43668', '43699', '43707', '43708', '43709', '43749', '43779', '43820', '43836', '43864', '43879', '43955', '44069', '44093', '44095', '44125', '44140', '44142', '44165', '44330', '44331', '44332', '44338', '44354', '44356', '44387', '44393', '44411', '44436', '44476', '44481', '44482', '44483', '44510', '44511', '44512', '44596', '44603', '44646', '44647', '44675', '44676', '44767', '44768', '44769', '44770', '44775', '44777', '44841', '44857', '44858', '44867', '44868', '44893', '44894', '44964', '44965', '44969', '45009', '45060', '45061', '45065', '45081', '45082', '45184', '45185', '45192', '45197', '45199', '45203', '45205', '45206', '45219', '45276', '45298', '45318', '45349', '45354', '45404', '45473', '45498', '45519', '45596', '45604', '45630', '45631', '45822', '45882', '45888', '45908', '45958', '45959', '45969', '45970', '45972', '45973', '45977', '45998', '46019', '46020', '46021', '46066', '46091', '46118', '46127', '46163', '46173', '46174', '46220', '46238', '46281', '46292', '46305', '46307', '46310', '46357', '46429', '46432', '46510', '46532', '46536', '46537', '46539', '46540', '46585', '46586', '46588', '46601', '46638', '46644', '46646', '46647', '46648', '46649', '46687', '46733', '46826', '46851', '46859', '46860', '46925', '47012', '47013', '47059', '47061', '47063', '47065', '47066', '47067', '47076', '47084', '47112', '47114', '47115', '47132', '47154', '47219', '47336', '47337', '47338', '47383', '47384', '47431', '47436', '47447', '47464', '47486', '47502', '47503', '47540', '47579', '47625', '47685', '47690', '47770', '47786', '47907', '47909', '47990', '48071', '48124', '48125', '48184', '48243', '48257', '48259', '48266', '48278', '48298', '48352', '48389', '48466', '48486', '48522', '48535', '48563', '48577', '48578', '48580', '48581', '48583', '48613', '48620', '48693', '48694', '48706', '48736', '48767', '48808', '48915', '48946', '48981', '48996', '49099', '49226', '49291', '49325', '49356', '49357', '49360', '49393', '49470', '49494', '49495', '49532', '49564', '49580', '49606', '49608', '49609', '49610', '49678', '49684', '49696', '49763', '49764', '49794', '49819', '49870', '49871', '49925', '49932', '49933', '49942', '50049', '50132', '50133', '50134', '50135', '50136', '50144', '50148', '50150', '50152', '50153', '50154', '50158', '50214', '50218', '50234', '50235', '50236', '50237', '50238', '50268', '50269', '50270', '50307', '50325', '50326', '50327', '50363', '50364', '50365', '50407', '50408', '50409', '50420', '50442', '50448', '50493', '50494', '50516', '50517', '50519', '50536', '50537', '50581', '50610', '50651', '50682', '50695', '50740', '50764', '50890', '50891', '50893', '50909', '50975', '50976', '51002', '51053', '51055', '51056', '51091', '51108', '51119', '51192', '51218', '51237', '51274', '51308', '51310', '51315', '51374', '51388', '51394', '51395', '51415', '51416', '51432', '51437', '51438', '51439', '51440', '51450', '51452', '51453', '51454', '51503', '51511', '51560', '51566', '51567', '51572', '51623', '51725', '51741', '51766', '51771', '51818', '51881', '51894', '51928', '51949', '51996', '52063', '52082', '5209', '5210', '52142', '52146', '52147', '52220', '52221', '52222', '52223', '52224', '52267', '52346', '52347', '52348', '52349', '52350', '52375', '52381', '52451', '52452', '52453', '52454', '52455', '52456', '52567', '52641', '52662', '52711', '52712', '52713', '52788', '52790', '52870', '52949', '52950', '52951', '53066', '53142', '53150', '53175', '53359', '53370', '53382', '53411', '53412', '53413', '53464', '53467', '53468', '53498', '53516', '53519', '53521', '53522', '53523', '53542', '53543', '53577', '53581', '53590', '53591', '53592', '53596', '53618', '53620', '53635', '53658', '53661', '53669', '53713', '53747', '53748', '53790', '53874', '53889', '53897', '53978', '53988', '54036', '54037', '54038', '54039', '54102', '54218', '54219', '54220', '54281', '54282', '54293', '54294', '54298', '54299', '54313', '54314', '54315', '54316', '54348', '54355', '54356', '54377', '54383', '54394', '54449', '54450', '54454', '54482', '54483', '54489', '54490', '54505', '54518', '54519', '54521', '54528', '54533', '54541', '54577', '54579', '54580', '54581', '54582', '54583', '54616', '54628', '54680', '54723', '54724', '54725', '54860', '54862', '54864', '54895', '54897', '54931', '54980', '54984', '55028', '55034', '55035', '55036', '55103', '55109', '55115', '55116', '55142', '55165', '55166', '55198', '55205', '55218', '55224', '55312', '55387', '55393', '55419', '55420', '55421', '55422', '55432', '55433', '55469', '55470', '55472', '55594', '55595', '55633', '55644', '55645', '55686', '55687', '55701', '55760', '55781', '55796', '55874', '56028', '56031', '56036', '56062', '56063', '56071', '56102', '56157', '56210', '56212', '56214', '56224', '56234', '56264', '56265', '56266', '56269', '56270', '56296', '56304', '56305', '56306', '56307', '56341', '56356', '56363', '56394', '56436', '56452', '56494', '56502', '56513', '56514', '56531', '56533', '56544', '56623', '56672', '56673', '56674', '56687', '56693', '56694', '56715', '56725', '56750', '56792', '56795', '56842', '56862', '56866', '56898', '56899', '56932', '56933', '56944', '56945', '56949', '56950', '56951', '56965', '56974', '57008', '57009', '57033', '57119', '57179', '57194', '57291', '57355', '57362', '57447', '57448', '57465', '57474', '57478', '57479', '57480', '57481', '57482', '57483', '57484', '57485', '57486', '57487', '57488', '57489', '57490', '57750', '57752', '57792', '57805', '57807', '57808', '57817', '57838', '57841', '57849', '57881', '57882', '57883', '57884', '57885', '57906', '57918', '57919', '57962', '57963', '58056', '58064', '58110', '58111', '58132', '58133', '58150', '58168', '58201', '58217', '58232', '58243', '58256', '58281', '58289', '58298', '58299', '58300', '58301', '58312', '58479', '58480', '58481', '58482', '58483', '58488', '58489', '58507', '58524', '58588', '58597', '58598', '58644', '58713', '58714', '58759', '58775', '58776', '58802', '58803', '58804', '58828', '58854', '58855', '59036', '59144', '59146', '59147', '59150', '59157', '59184', '59210', '59212', '59213', '59215', '59237', '59326', '59327', '59328', '59365', '59367', '59370', '59391', '59440', '59505', '59506', '59507', '59538', '59540', '59595', '59598', '59628', '59629', '59656', '59683', '59685', '59686', '59753', '59756', '59759', '59789', '59887', '59896', '59897', '59934', '59966', '59967', '60011', '60176', '60177', '60178', '60229', '60247', '60273', '60421', '60425', '60486', '60525', '60526', '60527', '60532', '60533', '60548', '60564', '60622', '60712', '60790', '60872', '60880', '60896', '61088', '61221', '61251', '61266', '61267', '61276', '61294', '61303', '61311', '61312', '61422', '61484', '61521', '61562', '61588', '61610', '61674', '61675', '61676', '61714', '61740', '61741', '61842', '61843', '61985', '62038', '62039', '62044', '62055', '62069', '62087', '62103', '62125', '62137', '62138', '62247', '62265', '62293', '62401', '62414', '62431', '62494', '62498', '62503', '62547', '62556', '62590', '62614', '62677', '62728', '62732', '62749', '62789', '62793', '62839', '62840', '62841', '62843', '62998', '63015', '63029', '63031', '63045', '63047', '63048', '63049', '63050', '63051', '63052', '63053', '63054', '63055', '63056', '63064', '63222', '63354', '63359', '63450', '63497', '63504', '63603', '63629', '63646', '63659', '63685', '63686', '63731', '63732', '63754', '63755', '63787', '63789', '63804', '63805', '63821', '63822', '63895', '63896', '63900', '63901', '63924', '63925', '63948', '63949', '63957', '63962', '63966', '63969', '64003', '64065', '64083', '64084', '64096', '64104', '64123', '64126', '64204', '64205', '64219', '64244', '64340', '64446', '64454', '64494', '64520', '64566', '64568', '64587', '64596', '64620', '64621', '64622', '64627', '64641', '64768', '64805', '64806', '64807', '64808', '64840', '64841', '64921', '64932', '64933', '64983', '65023', '65114', '65141', '65182', '65183', '65192', '65248', '65249', '65338', '65371', '65373', '65419', '65452', '65455', '65460', '65463', '65465', '65496', '65513', '65525', '65533', '65561', '65703', '65723', '65834', '65901', '65944', '66003', '66008', '66013', '66052', '66131', '66132', '66212', '66234', '66240', '66242', '66274', '66399', '66400', '66480', '66520', '66547', '66661', '66710', '66746', '66793', '66801', '66807', '66808', '66809', '66869', '66910', '66931', '67067', '67094', '67099', '67209', '67276', '67314', '67396', '67507', '67620', '67679', '67723', '67730', '67972', '68001', '68014', '68122', '68144', '68181', '68245', '68264', '68275', '68291', '68396', '68503', '68513', '68618', '68781', '68821', '68831', '68901', '68929', '69179', '7482', '7706', '7708', '7910', '9601', '9602', '9603', '9604', '9607']


flats = []
problem_id = []
current_date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

for building_id in buildings_id:

    try:

        url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/{building_id}'


        driver.get(url=url)
        page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
        soup = BeautifulSoup(page_content, 'html.parser')
        info = soup.find_all('div', class_=["Row__Value-sc-13pfgqd-2 dySlPJ", 'Row__Value-sc-13pfgqd-2 ClvkY'])
        i = []
        for inf in info:

            i.append(inf.text)


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



        dop_info = soup.find_all('span', class_="CharacteristicsBlock__RowSpan-sc-1fyyfia-4 eCBXEE")
        i = []
        for inf in dop_info:

            i.append(inf.text)

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
    except:
        print('Ошибка, пропускаем id')
        problem_id.append(building_id)
        continue



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