import requests
from datetime import datetime
import time
import pandas as pd
import openpyxl
import os
import random

cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'DMIR_AUTH': '6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744095038128%2C%22sl%22%3A%7B%22224%22%3A1744008638128%2C%221228%22%3A1744008638128%7D%7D',
    '_yasc': 'QG4aPQs+5Fze4KmEjttcFE3EtmDAdt73mR3RN89Q5nU15dTfMQ1AYAnVGj/cPRzX9IU=',
    '_yasc': 'fKvML3PgmyiDQnB5q4cqA2Uk3/gQzlZKpKasfXTV1IghUVHOdEbwCc2GNi9raBchUKw=',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
    'adrdel': '1744094487237',
    'F6_CIAN_SID': 'e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956',
    'F6_CIAN_UID': '8098251',
    'session_region_id': '4619',
    'session_main_town_region_id': '176083',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCkdEQhvKE8PFFtDPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVhUPT1dPXZyc1tBISViTGBUdlxVMiseFngoKVUJPmBCdHQuLTxnHWJ9XyV1D1N6WyAZM3EqDAg+Y0ZCcHoyQGsPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomR1lNCikeEX90I1d7dScOCSplMy0tWRgIH2N4JRlrcmY=qOrDWA==',
    '_gcl_au': '1.1.150541652.1744094509',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    'sopr_utm': '%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D',
    'sopr_session': '24dfe084219d480f',
    'cookieUserID': '8098251',
    '_ga': 'GA1.1.2141111618.1744094510',
    'uxfb_usertype': 'searcher',
    'afUserId': '01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p',
    'AF_SYNC': '1744094510966',
    'cian_ruid': '8098251',
    '_ga_3369S417EL': 'GS1.1.1744094510.1.1.1744094538.32.0.0',
    'cfidsw-cian': 'H1vjqn5vmj+YGg5Xm86d7UR8gnDIoCNFY8gdrCFcTqtHKZYUgdtgp9iKpXdSSbGFVM3wIOb0e7OaMH1QrB3vP/D7z3Lo7OVWAPrjxgKydnUn4xnnv+F/ykNQmUGqLP3wFn3hu6LKswrIKqeD9Q72FwQBVpK60oRaOJC1yJU=',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://tver.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://tver.cian.ru/',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; DMIR_AUTH=6taU2fxYUK9ueK3v9H%2FinxPLBeylmpWK1TRc9t0epfkverMXTikTFSx6jpqFQwWItMRZisykrzBiRnVB8iFUUAffcck7zRtJLc%2B88RX8lXpn4th4%2FfkvQeZt%2BP%2FicK2e4qBNPv2QrGlB3VqFMQA0c44kdcfYraf0teyhsZ%2BNEVg%3D; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744095038128%2C%22sl%22%3A%7B%22224%22%3A1744008638128%2C%221228%22%3A1744008638128%7D%7D; _yasc=QG4aPQs+5Fze4KmEjttcFE3EtmDAdt73mR3RN89Q5nU15dTfMQ1AYAnVGj/cPRzX9IU=; _yasc=fKvML3PgmyiDQnB5q4cqA2Uk3/gQzlZKpKasfXTV1IghUVHOdEbwCc2GNi9raBchUKw=; _ym_isad=2; _ym_visorc=b; adrdel=1744094487237; F6_CIAN_SID=e5fb20e50b6d8357ec78a6551e662c55c7c41203f66bb61f78d67e1c89137956; F6_CIAN_UID=8098251; session_region_id=4619; session_main_town_region_id=176083; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCkdEQhvKE8PFFtDPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVhUPT1dPXZyc1tBISViTGBUdlxVMiseFngoKVUJPmBCdHQuLTxnHWJ9XyV1D1N6WyAZM3EqDAg+Y0ZCcHoyQGsPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomR1lNCikeEX90I1d7dScOCSplMy0tWRgIH2N4JRlrcmY=qOrDWA==; _gcl_au=1.1.150541652.1744094509; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; sopr_utm=%7B%22utm_source%22%3A+%22direct%22%2C+%22utm_medium%22%3A+%22None%22%7D; sopr_session=24dfe084219d480f; cookieUserID=8098251; _ga=GA1.1.2141111618.1744094510; uxfb_usertype=searcher; afUserId=01d5d1e2-93cc-4880-8496-5dfe7ddb17cf-p; AF_SYNC=1744094510966; cian_ruid=8098251; _ga_3369S417EL=GS1.1.1744094510.1.1.1744094538.32.0.0; cfidsw-cian=H1vjqn5vmj+YGg5Xm86d7UR8gnDIoCNFY8gdrCFcTqtHKZYUgdtgp9iKpXdSSbGFVM3wIOb0e7OaMH1QrB3vP/D7z3Lo7OVWAPrjxgKydnUn4xnnv+F/ykNQmUGqLP3wFn3hu6LKswrIKqeD9Q72FwQBVpK60oRaOJC1yJU=',
}

json_data = {
    'jsonQuery': {
        'region': {
            'type': 'terms',
            'value': [
                176083,
            ],
        },
    },
    'uri': '/newobjects/list?deal_type=sale&engine_version=2&offer_type=newobject&region=176083&p=2',
    'subdomain': 'tver',
    'offset': 0,
    'count': 25,
    'userCanUseHiddenBase': False,
}

id_list = []

while True:

    response = requests.post(
        'https://api.cian.ru/newbuilding-search/v1/get-newbuildings-for-serp/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )


    items = response.json()['newbuildings']

    for i in items:
        id = i['id']
        id_list.append(id)
    if not items:
        break
    json_data['offset'] += 25


print(id_list)
