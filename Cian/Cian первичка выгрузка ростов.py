# меняем настройки поиска через json_data. Парсим отдельно по каждому ЖК. Если в ЖК более 1500 объявлений, то нужно разбивать по корпусам

import numpy
import requests
import datetime
import time
import pandas as pd
import openpyxl
import os
import random
import re
from functions import classify_renovation, clean_filename


def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s

cookies = {
    '_CIAN_GK': '38928be9-bba1-4562-8d8e-71aa9dfb2ba9',
    'cf_clearance': 'iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk',
    '_ym_uid': '174161324651361127',
    '_ym_d': '1741613246',
    'adrcid': 'Ad53EZahiTy4QvZYZHYhh0Q',
    'adrdel': '1744094487237',
    'acs_3': '%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D',
    '_gcl_au': '1.1.358370826.1745923014',
    'newbuilding-search-frontend.consultant_cian_chat_onboarding_shown': '1',
    'cookie_agreement_accepted': '1',
    'tmr_lvid': '61ae9374a9f1699406db7cc31ef00775',
    'tmr_lvidTS': '1741613242260',
    '_ga': 'GA1.1.460280003.1749468781',
    'uxfb_usertype': 'searcher',
    'uxs_uid': '1ed08180-4604-11f0-94f5-19dbce91137e',
    'forever_region_id': '4951',
    'forever_region_name': '%D0%9F%D1%8F%D1%82%D0%B8%D0%B3%D0%BE%D1%80%D1%81%D0%BA',
    'DMIR_AUTH': 'VIa7V2wMqaR44qYIlt2%2FiLrl32BcTqB%2FBPyLd23IM6WASiU8GWloP9h03GkKWcpPXH%2F7wpf01F9aYP7LQw2WiNB2RiMbEBat9reqrTVmjtgP2qw8fov1cgifTeelRd5LXS5yiuhpoBMd%2BurIUUTrN7fpXGZmJkFTJ47U2RA7q4o%3D',
    'seen_cpd_landing': '1',
    'cian_ruid': '8098251',
    'map_preview_onboarding_counter': '3',
    'last_paid_utm': '?utm_source=yandex&utm_medium=cpc&utm_term=cian&utm_content=kw:40322435580|ad:12512988661|grp:4986514529|drf:no|dev:desktop|p:premium|n:1|reg:213|s:none&utm_campaign=b2c_all_mskmo_perf_mix_search_tgo_brand_76962079&etext=&yclid=11097115837649387519',
    'sopr_utm': '%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
    'frontend-serp.offer_chat_onboarding_shown': '1',
    'F6_CIAN_SID': 'ab846777590ab2ba1b3153c2ac0704592e89667154d24985d82b17ee2febc127',
    'sopr_session': '035692db869045f3',
    'countCallNowPopupShowed': '0%3A1752134500871',
    'domain_sid': 'h9UFzhDmhYsy0jug-hr66%3A1752134546668',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobEnpwJVgOC11EPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVQJDw9hREh0eDI7Hk9heRIgdVhOfihMEzAmI1Z/D2BGQyp7MkFrJGBMXVNFWVYJKk0ZeSUkVjxAXXN2Jy4qPWwPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdOfCobGn5rJVd7dScOCSplMy0tWRgIH2N4JRlrcmY=2NJARw==',
    'tmr_detect': '0%7C1752135299923',
    'uxfb_card_satisfaction': '%5B294040371%2C318468055%5D',
    'cfidsw-cian': 'qkFLlZe/Ej9vCcyEi9G/kIWJn2AIZlPLjgZ/EbaPvzElyjW8t2nqT8Od/d1cBS1Afe7OP+Q4liH6aUKFsk1F8APPu5LbCA6MqqhCMx4RgI8cMFM6TOai83ECjP5IYrbjP66CI8J4IKfWnoUVyjqsEHQeFkpVGJZ8hi/QtmTo',
    'gsscw-cian': '75jXpXeNdG99nfBxXB0Q4sVaWuLkPS/v39K1u+2Zs5SVNhiSFX2E2z2nlAe9Y4rNQwUlME4/Pu2nHD9+LB4j9s3acS8rJaZuPWL7G5S/28lWhcPq9/y5l/eJ9xeWtDygwAcWRtGNBbcQSv0OSK3ju+hBKsI7vuO8pJ29N6xSgmZUzxldJkIu4RMZKchnLXzvtn763SbCqeSHK5oGtLvuQWrHbFAXcPeO22gyLXjfUsg46Ykzhk8RlW5UJMklZu3tCkaou7tXM7G7MLfiIMwfAXxR',
    'fgsscw-cian': 'G3hU93d75b1a14a67cd96262135a723df6631905',
    'F6_CIAN_UID': '8098251',
    'cookieUserID': '8098251',
    'session_region_id': '1',
    'session_main_town_region_id': '1',
    '__zzatw-cian': 'MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobEnpyK08NDGM/PV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVQJDw9hREh0eDI7Hk9heRIgdVhOfihMEzAmI1Z/D2BGQyp7MkFrJGBMXVNFWVYJKk0ZeSUkVjxAXXN2Jy4qPWwPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdOfCwhEX1sK1J7dScOCSplMy0tWRgIH2N4JRlrcmY=QweRKQ==',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
    '_yasc': 'ysA1mBFiB0M4ksQnEpcBeA86SaaBLTBJEkUXpyjc61b1/9ke+UiRw1Ft2NqB3P1Kue4=',
    '_yasc': 'to/6lu14yw66sxQu8W+jamMtd96cMR8TDv5nBXVeE6KGPnlA3PuBwTbJvMJy4l6noDE=',
    'cfidsw-cian': 'CGOJVuoYANhlrbKzA4Z1i45vU7Jj3BbjgrLD9c7oqtz1euhtMkxmYy7Pt4SafbBg7y8QpDofgOkgpvE8I0MJALM7Xnk+omjSRkFDRqENYWOG34Ziame+1DB25uA8X0yLCz9zKItxo9sZb+bUHDPmuhYv3UBAqpHbyG4C2XKK',
    'gsscw-cian': 'yyvD124T4nrkT3zCZot2mkC2IsyS483LTb87qxsrDFElVIwQp84cSFs3vrDHJ78NfWKtwT/XfKU9XZ1JvpseXpzpu3WyK7eEiPeWoljhx+Tps7rPvV1cOM3h0g+JVRVhbgH+b/ubwAHqlZXrRivnn2E+qXZ2xUthm568X2BC1qsaL6RahA+FChV5MIk9uJIZMFVh26K+pEAwhXzPdfRuY7XQVk4dnLk3dsjbJKYsHt8DwWiVqMAuV9Us10hBy/5NTYXmnH9CHPHXJXkwjLkm+hCC',
    'fgsscw-cian': 'gxSV5fce8eb99fff4fc00b9f2469e57bb9fa7d2f',
    '_ga_3369S417EL': 'GS2.1.s1752137804$o79$g1$t1752138538$j60$l0$h0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.cian.ru',
    'priority': 'u=1, i',
    'referer': 'https://www.cian.ru/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': '_CIAN_GK=38928be9-bba1-4562-8d8e-71aa9dfb2ba9; cf_clearance=iV44UjyYQedk6k6mLlGxFJSJQ8vRTpRyJAEbHdgR6qI-1741613241-1.2.1.1-p.Lq7YMuxUI71ds4r6v2szise7f_47ZvUdX0qvtqEAXpdnxav4CojfSw.MBjSEs4FLka37z6PFsx.G08NzlLVoTo1DmLc159.35zaGtS1DGpsnMa9MNvwJ4V5cqaGW0hittfBDfPlVKpPmziKz3LADg87IAgNBg4_BJW.59U5.Up8A6OI7pBmeTd9PK.MFYBtAewGarUpGxZqU17t96CtbRMcNC53qneva02mFMk4n3mBhbRCfzNVRU3ao5xCAmDRNLqSTrHi7kdErRD8UPEa2IZrZRbznqM87Q6RvimgB9YDOHBut1KblkoOtTEDL5FKaz00aHCvP80uDJOKdar00wq2rLs5g2J.mJ.vls1N_nm0Qx46EAdE7wsdPwSBkeuPAR_q4xQJ0JWVe7isTRmi7V7LbD_NavVvRSboBnq_Xk; _ym_uid=174161324651361127; _ym_d=1741613246; adrcid=Ad53EZahiTy4QvZYZHYhh0Q; adrdel=1744094487237; acs_3=%7B%22hash%22%3A%221aa3f9523ee6c2690cb34fc702d4143056487c0d%22%2C%22nst%22%3A1744181465976%2C%22sl%22%3A%7B%22224%22%3A1744095065976%2C%221228%22%3A1744095065976%7D%7D; _gcl_au=1.1.358370826.1745923014; newbuilding-search-frontend.consultant_cian_chat_onboarding_shown=1; cookie_agreement_accepted=1; tmr_lvid=61ae9374a9f1699406db7cc31ef00775; tmr_lvidTS=1741613242260; _ga=GA1.1.460280003.1749468781; uxfb_usertype=searcher; uxs_uid=1ed08180-4604-11f0-94f5-19dbce91137e; forever_region_id=4951; forever_region_name=%D0%9F%D1%8F%D1%82%D0%B8%D0%B3%D0%BE%D1%80%D1%81%D0%BA; DMIR_AUTH=VIa7V2wMqaR44qYIlt2%2FiLrl32BcTqB%2FBPyLd23IM6WASiU8GWloP9h03GkKWcpPXH%2F7wpf01F9aYP7LQw2WiNB2RiMbEBat9reqrTVmjtgP2qw8fov1cgifTeelRd5LXS5yiuhpoBMd%2BurIUUTrN7fpXGZmJkFTJ47U2RA7q4o%3D; seen_cpd_landing=1; cian_ruid=8098251; map_preview_onboarding_counter=3; last_paid_utm=?utm_source=yandex&utm_medium=cpc&utm_term=cian&utm_content=kw:40322435580|ad:12512988661|grp:4986514529|drf:no|dev:desktop|p:premium|n:1|reg:213|s:none&utm_campaign=b2c_all_mskmo_perf_mix_search_tgo_brand_76962079&etext=&yclid=11097115837649387519; sopr_utm=%7B%22utm_source%22%3A+%22yandex%22%2C+%22utm_medium%22%3A+%22organic%22%7D; frontend-serp.offer_chat_onboarding_shown=1; F6_CIAN_SID=ab846777590ab2ba1b3153c2ac0704592e89667154d24985d82b17ee2febc127; sopr_session=035692db869045f3; countCallNowPopupShowed=0%3A1752134500871; domain_sid=h9UFzhDmhYsy0jug-hr66%3A1752134546668; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobEnpwJVgOC11EPV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVQJDw9hREh0eDI7Hk9heRIgdVhOfihMEzAmI1Z/D2BGQyp7MkFrJGBMXVNFWVYJKk0ZeSUkVjxAXXN2Jy4qPWwPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdOfCobGn5rJVd7dScOCSplMy0tWRgIH2N4JRlrcmY=2NJARw==; tmr_detect=0%7C1752135299923; uxfb_card_satisfaction=%5B294040371%2C318468055%5D; cfidsw-cian=qkFLlZe/Ej9vCcyEi9G/kIWJn2AIZlPLjgZ/EbaPvzElyjW8t2nqT8Od/d1cBS1Afe7OP+Q4liH6aUKFsk1F8APPu5LbCA6MqqhCMx4RgI8cMFM6TOai83ECjP5IYrbjP66CI8J4IKfWnoUVyjqsEHQeFkpVGJZ8hi/QtmTo; gsscw-cian=75jXpXeNdG99nfBxXB0Q4sVaWuLkPS/v39K1u+2Zs5SVNhiSFX2E2z2nlAe9Y4rNQwUlME4/Pu2nHD9+LB4j9s3acS8rJaZuPWL7G5S/28lWhcPq9/y5l/eJ9xeWtDygwAcWRtGNBbcQSv0OSK3ju+hBKsI7vuO8pJ29N6xSgmZUzxldJkIu4RMZKchnLXzvtn763SbCqeSHK5oGtLvuQWrHbFAXcPeO22gyLXjfUsg46Ykzhk8RlW5UJMklZu3tCkaou7tXM7G7MLfiIMwfAXxR; fgsscw-cian=G3hU93d75b1a14a67cd96262135a723df6631905; F6_CIAN_UID=8098251; cookieUserID=8098251; session_region_id=1; session_main_town_region_id=1; __zzatw-cian=MDA0dC0cTHtmcDhhDHEWTT17CT4VHThHKHIzd2UxO24lYUxaET9HFTZnXEpCNxVZcU4nfAsmMl4tYQ8rCB5UNV9OCCobEnpyK08NDGM/PV8/cnsiD2k5IVt0FhNFWmFVaUAfQTY6flJkGBRIWRw2czljajUjfj1qTnsJXVQJDw9hREh0eDI7Hk9heRIgdVhOfihMEzAmI1Z/D2BGQyp7MkFrJGBMXVNFWVYJKk0ZeSUkVjxAXXN2Jy4qPWwPWzkhVA0gDkRpCxtpNmcWSTwacjNpZW10KlJRUVomSFdOfCwhEX1sK1J7dScOCSplMy0tWRgIH2N4JRlrcmY=QweRKQ==; _ym_visorc=b; _ym_isad=2; _yasc=ysA1mBFiB0M4ksQnEpcBeA86SaaBLTBJEkUXpyjc61b1/9ke+UiRw1Ft2NqB3P1Kue4=; _yasc=to/6lu14yw66sxQu8W+jamMtd96cMR8TDv5nBXVeE6KGPnlA3PuBwTbJvMJy4l6noDE=; cfidsw-cian=CGOJVuoYANhlrbKzA4Z1i45vU7Jj3BbjgrLD9c7oqtz1euhtMkxmYy7Pt4SafbBg7y8QpDofgOkgpvE8I0MJALM7Xnk+omjSRkFDRqENYWOG34Ziame+1DB25uA8X0yLCz9zKItxo9sZb+bUHDPmuhYv3UBAqpHbyG4C2XKK; gsscw-cian=yyvD124T4nrkT3zCZot2mkC2IsyS483LTb87qxsrDFElVIwQp84cSFs3vrDHJ78NfWKtwT/XfKU9XZ1JvpseXpzpu3WyK7eEiPeWoljhx+Tps7rPvV1cOM3h0g+JVRVhbgH+b/ubwAHqlZXrRivnn2E+qXZ2xUthm568X2BC1qsaL6RahA+FChV5MIk9uJIZMFVh26K+pEAwhXzPdfRuY7XQVk4dnLk3dsjbJKYsHt8DwWiVqMAuV9Us10hBy/5NTYXmnH9CHPHXJXkwjLkm+hCC; fgsscw-cian=gxSV5fce8eb99fff4fc00b9f2469e57bb9fa7d2f; _ga_3369S417EL=GS2.1.s1752137804$o79$g1$t1752138538$j60$l0$h0',
}



json_data = {
    'jsonQuery': {
        '_type': 'flatsale',
        'sort': {
            'type': 'term',
            'value': 'price_object_order',
        },
        'engine_version': {
            'type': 'term',
            'value': 2,
        },
        'geo': {
            'type': 'geo',
            'value': [
                {
                    'type': 'polygon',
                    'name': 'Область поиска',
                    'coordinates': [
                        [
                            '20.3571312',
                            '54.7479954',
                        ],
                        [
                            '20.3543846',
                            '54.7273584',
                        ],
                        [
                            '20.3557579',
                            '54.7067214',
                        ],
                        [
                            '20.3598778',
                            '54.6876718',
                        ],
                        [
                            '20.3406517',
                            '54.6710035',
                        ],
                        [
                            '20.309066',
                            '54.6646536',
                        ],
                        [
                            '20.2774803',
                            '54.6590975',
                        ],
                        [
                            '20.2445213',
                            '54.6567163',
                        ],
                        [
                            '20.2033226',
                            '54.6527477',
                        ],
                        [
                            '20.1703636',
                            '54.6471915',
                        ],
                        [
                            '20.1360313',
                            '54.6440166',
                        ],
                        [
                            '20.0989525',
                            '54.6392542',
                        ],
                        [
                            '20.0632469',
                            '54.6392542',
                        ],
                        [
                            '20.0302879',
                            '54.6360793',
                        ],
                        [
                            '19.997329',
                            '54.6297295',
                        ],
                        [
                            '19.9616234',
                            '54.6233796',
                        ],
                        [
                            '19.9286644',
                            '54.6186172',
                        ],
                        [
                            '19.8970787',
                            '54.6130611',
                        ],
                        [
                            '19.8627464',
                            '54.6114736',
                        ],
                        [
                            '19.832534',
                            '54.6194109',
                        ],
                        [
                            '19.8215477',
                            '54.6376668',
                        ],
                        [
                            '19.8297875',
                            '54.6590975',
                        ],
                        [
                            '19.8490135',
                            '54.6757659',
                        ],
                        [
                            '19.8696129',
                            '54.6948154',
                        ],
                        [
                            '19.8833458',
                            '54.7162462',
                        ],
                        [
                            '19.8929588',
                            '54.7400581',
                        ],
                        [
                            '19.9011986',
                            '54.7630763',
                        ],
                        [
                            '19.9053185',
                            '54.7845071',
                        ],
                        [
                            '19.9066917',
                            '54.8043504',
                        ],
                        [
                            '19.9066917',
                            '54.828956',
                        ],
                        [
                            '19.9053185',
                            '54.8535617',
                        ],
                        [
                            '19.898452',
                            '54.8741987',
                        ],
                        [
                            '19.8902123',
                            '54.8964232',
                        ],
                        [
                            '19.8860924',
                            '54.9162665',
                        ],
                        [
                            '19.8902123',
                            '54.9376973',
                        ],
                        [
                            '19.9039452',
                            '54.9551593',
                        ],
                        [
                            '19.9245445',
                            '54.9726214',
                        ],
                        [
                            '19.9575035',
                            '54.9845274',
                        ],
                        [
                            '19.997329',
                            '54.9924647',
                        ],
                        [
                            '20.0371544',
                            '54.9948459',
                        ],
                        [
                            '20.0742333',
                            '54.9948459',
                        ],
                        [
                            '20.115432',
                            '54.9948459',
                        ],
                        [
                            '20.1634972',
                            '54.9932585',
                        ],
                        [
                            '20.2033226',
                            '54.9892898',
                        ],
                        [
                            '20.2486412',
                            '54.9853211',
                        ],
                        [
                            '20.309066',
                            '54.9805587',
                        ],
                        [
                            '20.3433983',
                            '54.9773838',
                        ],
                        [
                            '20.3873436',
                            '54.9750026',
                        ],
                        [
                            '20.4340355',
                            '54.9742089',
                        ],
                        [
                            '20.4752342',
                            '54.9750026',
                        ],
                        [
                            '20.5191795',
                            '54.979765',
                        ],
                        [
                            '20.5521385',
                            '54.9813525',
                        ],
                        [
                            '20.6098167',
                            '54.9837337',
                        ],
                        [
                            '20.6523888',
                            '54.9829399',
                        ],
                        [
                            '20.6977074',
                            '54.9781776',
                        ],
                        [
                            '20.7375328',
                            '54.9757964',
                        ],
                        [
                            '20.785598',
                            '54.9742089',
                        ],
                        [
                            '20.8254234',
                            '54.9694465',
                        ],
                        [
                            '20.8721153',
                            '54.9638904',
                        ],
                        [
                            '20.9050743',
                            '54.959128',
                        ],
                        [
                            '20.9448998',
                            '54.9511907',
                        ],
                        [
                            '20.9847252',
                            '54.9448408',
                        ],
                        [
                            '21.0163109',
                            '54.938491',
                        ],
                        [
                            '21.0163109',
                            '54.9186477',
                        ],
                        [
                            '20.9929649',
                            '54.9043605',
                        ],
                        [
                            '20.9627525',
                            '54.8932483',
                        ],
                        [
                            '20.9284203',
                            '54.8861047',
                        ],
                        [
                            '20.8913414',
                            '54.8837235',
                        ],
                        [
                            '20.851516',
                            '54.8797549',
                        ],
                        [
                            '20.8130638',
                            '54.8797549',
                        ],
                        [
                            '20.7746117',
                            '54.8797549',
                        ],
                        [
                            '20.7279198',
                            '54.8861047',
                        ],
                        [
                            '20.6812279',
                            '54.8908671',
                        ],
                        [
                            '20.6400292',
                            '54.8956295',
                        ],
                        [
                            '20.601577',
                            '54.8995981',
                        ],
                        [
                            '20.5672447',
                            '54.9051543',
                        ],
                        [
                            '20.5301659',
                            '54.9099167',
                        ],
                        [
                            '20.4944603',
                            '54.9130916',
                        ],
                        [
                            '20.4615013',
                            '54.9154728',
                        ],
                        [
                            '20.4230492',
                            '54.9162665',
                        ],
                        [
                            '20.3859703',
                            '54.9162665',
                        ],
                        [
                            '20.3461449',
                            '54.917854',
                        ],
                        [
                            '20.3131859',
                            '54.9170602',
                        ],
                        [
                            '20.2747337',
                            '54.9154728',
                        ],
                        [
                            '20.2390282',
                            '54.9154728',
                        ],
                        [
                            '20.200576',
                            '54.9130916',
                        ],
                        [
                            '20.1648705',
                            '54.9115041',
                        ],
                        [
                            '20.1277916',
                            '54.9075355',
                        ],
                        [
                            '20.0934593',
                            '54.9027731',
                        ],
                        [
                            '20.0577538',
                            '54.8980107',
                        ],
                        [
                            '20.0344078',
                            '54.8845172',
                        ],
                        [
                            '20.0247948',
                            '54.8654677',
                        ],
                        [
                            '20.0124352',
                            '54.8464181',
                        ],
                        [
                            '20.0096886',
                            '54.8273686',
                        ],
                        [
                            '20.0083153',
                            '54.8075253',
                        ],
                        [
                            '20.0083153',
                            '54.7868883',
                        ],
                        [
                            '20.0151817',
                            '54.7678387',
                        ],
                        [
                            '20.0412743',
                            '54.7511704',
                        ],
                        [
                            '20.0742333',
                            '54.7440268',
                        ],
                        [
                            '20.1085655',
                            '54.7384707',
                        ],
                        [
                            '20.1428978',
                            '54.7360895',
                        ],
                        [
                            '20.190963',
                            '54.7352957',
                        ],
                        [
                            '20.2417748',
                            '54.7337083',
                        ],
                        [
                            '20.2870934',
                            '54.7392644',
                        ],
                        [
                            '20.3200523',
                            '54.7416456',
                        ],
                        [
                            '20.3530113',
                            '54.746408',
                        ],
                        [
                            '20.3571312',
                            '54.7479954',
                        ],
                    ],
                },
            ],
        },
        'bbox': {
            'type': 'term',
            'value': [
                [
                    20.0395576538,
                    54.8360132604,
                ],
                [
                    20.9184639038,
                    54.9871285477,
                ],
            ],
        },
        'floor': {
            'type': 'range',
            'value': {
                'gte': 1,
                'lte': 2,
            },
        },
        'publish_period': {
            'type': 'term',
            'value': 2592000,
        },
        'electronic_trading': {
            'type': 'term',
            'value': 2,
        },
        'room': {
            'type': 'terms',
            'value': [
                1,
            ],
        },
        'building_status': {
            'type': 'term',
            'value': 2,
        },
        'from_developer': {
            'type': 'term',
            'value': True,
        },
        'page': {
            'type': 'term',
            'value': 1,
        },
    },
}

current_date = datetime.date.today()


rooms_ids = [1,2,3,4,5,6,7,9]
total_floor_list = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 200]]
session = requests.Session()

for rooms in rooms_ids:

    json_data["jsonQuery"]["page"]["value"] = 1
    json_data["jsonQuery"]["room"]["value"][0] = rooms
    print(f'Комнатность: {rooms}')


    for f in total_floor_list:

        flats = []
        json_data["jsonQuery"]["floor"]["value"]["gte"] = f[0]
        json_data["jsonQuery"]["floor"]["value"]["lte"] = f[1]
        json_data["jsonQuery"]["page"]["value"] = 1
        print(f'Этажи квартир: {f}')

        name_counter = f'{rooms}-{f[0]}-{f[1]}'

        counter = 1
        total_count = 1

        while len(flats) < total_count:

            if counter > 1:
                sleep_time = random.uniform(7, 11)
                time.sleep(sleep_time)
            try:
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data
                )

                print(response.status_code)

                items = response.json()["data"]["offersSerialized"]
            except:
                print("Произошла ошибка, пробуем ещё раз")
                time.sleep(30)
                session = requests.Session()
                response = session.post(
                    'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
                    cookies=cookies,
                    headers=headers,
                    json=json_data
                )
                print(response.status_code)
                items = response.json()["data"]["offersSerialized"]

            for i in items:
                try:
                    if i['building']['deadline']['isComplete'] == True:
                        srok_sdachi = "Дом сдан"
                    elif i['building']['deadline']['quarterEnd'] is None and i['building']['deadline']['year'] is None:
                        srok_sdachi = ''
                    else:
                        srok_sdachi = f"Cдача ГК: {i['newbuilding']['house']['finishDate']['quarter']} квартал, {i['newbuilding']['house']['finishDate']['year']} года".replace('None', '')
                except:
                    srok_sdachi = ''
                try:
                    url = i['fullUrl']
                except:
                    url = ''

                try:
                    if i['isApartments'] == True:
                        type = "Апартаменты"
                    else:
                        type = "Квартира"
                except:
                    type = ''

                try:
                    price = i['bargainTerms']['priceRur']
                except:
                    price = ''
                try:
                    project = i['geo']['jk']['displayName'].replace('ЖК ', '').replace('«', '').replace('»', '')
                except:
                    project = ''
                try:
                    if i['decoration'] == "fine":
                        finish_type = "С отделкой"
                    elif i['decoration'] == "without" or i['decoration'] == "rough":
                        finish_type = "Без отделки"
                    else:
                        finish_type = i['decoration']
                except:
                    finish_type = ''
                if not finish_type:
                    finish_type = classify_renovation(i['description'])

                try:
                    adress = i['geo']['userInput']
                except:
                    adress = ""

                try:
                    korpus = i["geo"]["jk"]["house"]["name"]
                except:
                    korpus = ''

                try:
                    developer = i['geo']['jk']['developer']['name']
                except:
                    developer = ""

                try:
                    if i["roomsCount"] == None:
                        room_count = 0
                    else:
                        room_count = int(i["roomsCount"])
                except:
                    room_count = ''
                try:
                    area = float(i["totalArea"])
                except:
                    area = ''


                date = datetime.date.today()

                try:
                    floor = i["floorNumber"]
                except:
                    floor = ''
                try:
                    added = i['added']
                except:
                    added = ''


                print(
                    f"{project}, {url}, дата: {date}, кол-во комнат: {room_count}, площадь: {area}, цена: {price}, срок сдачи: {srok_sdachi}, корпус: {korpus}, этаж: {floor}, {finish_type} ")
                result = [date, srok_sdachi, url, project, developer, adress, korpus, type, finish_type, room_count, area, price, floor, added]
                flats.append(result)


            if not items:
                break
            json_data["jsonQuery"]["page"]["value"] += 1
            print("-----------------------------------------------------------------------------")
            total_count = response.json()["data"]["offerCount"]
            downloaded = len(flats)
            counter += 1



        df = pd.DataFrame(flats, columns=['Дата обновления',
                                          'Срок сдачи',
                                          'Ссылка',
                                          'Название проекта',
                                          'Девелопер',
                                          'Адрес',
                                          'Корпус',
                                          'Тип помещения',
                                          'Отделка',
                                          'Кол-во комнат',
                                          'Площадь, кв.м',
                                          'Цена лота, руб.',
                                          'Этаж',
                                          'Дата объявления'])

        current_date = datetime.date.today()

        # Базовый путь для сохранения
        base_path = r""

        folder_path = os.path.join(base_path, str(current_date))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        def sanitize_filename(name):
            for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
                name = name.replace(char, '_')
            return name

        project = sanitize_filename(project)
        filename = f"Калин_область_{rooms}_{f}_{current_date}.xlsx"

        # Полный путь к файлу0
        file_path = os.path.join(folder_path, filename)

        # Сохранение файла в папку
        try:
            df.to_excel(file_path, index=False)
        except:
            filename = f"{project}_{current_date}_2.xlsx"
            file_path = os.path.join(folder_path, filename)
            df.to_excel(file_path, index=False)

