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



cookies = {
    'spid': '1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3',
    '_ym_uid': '1741679472430329696',
    '_ym_d': '1741679472',
    'tmr_lvid': '21dd9990a0516763e1af5efdddfe2ece',
    'tmr_lvidTS': '1741679492626',
    '_ym_isad': '2',
    'domain_sid': 'p9NEOoC7wfYKTfSohYE69%3A1743597502986',
    'NSC_wtsw_obti.epn.sg_dzs_iuuqt': 'ffffffff09da1a3745525d5f4f58455e445a4a423660',
    'tmr_detect': '0%7C1743599371818',
    'spsc': '1743603129300_0cb4a77edd3a2899c0fb9888c1ef36d6_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    'authorization': 'Basic MTpxd2U=',
    'priority': 'u=1, i',
    'referer': 'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BE%D0%B2/%D1%81%D0%BF%D0%B8%D1%81%D0%BE%D0%BA?place=0-1156&sortName=objReady100PercDt&sortDirection=desc',
    'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    # 'cookie': 'spid=1741679465470_d3eb45434c69fa862e96f696b2311a6c_mqsl1svnw3dudau3; _ym_uid=1741679472430329696; _ym_d=1741679472; tmr_lvid=21dd9990a0516763e1af5efdddfe2ece; tmr_lvidTS=1741679492626; _ym_isad=2; domain_sid=p9NEOoC7wfYKTfSohYE69%3A1743597502986; NSC_wtsw_obti.epn.sg_dzs_iuuqt=ffffffff09da1a3745525d5f4f58455e445a4a423660; tmr_detect=0%7C1743599371818; spsc=1743603129300_0cb4a77edd3a2899c0fb9888c1ef36d6_e6cfb3ea8f0a0fa28cc6ebefdcae8ea5',
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



buildings_id = [66038, 66037, 66004, 66003, 66002, 66001, 65994, 65993, 65834, 65833, 65716, 65715, 65714, 65713, 65712, 65711, 65710, 65709, 65708, 65707, 65706, 65705, 65704, 65703, 65702, 65701, 65700, 65699, 65698, 65697, 65696, 65695, 65694, 65693, 65692, 65691, 65690, 65689, 65688, 65687, 65686, 65685, 65684, 65683, 65682, 65681, 65680, 65679, 65678, 65677, 65676, 65675, 65674, 65673, 65672, 65671, 65670, 65669, 65668, 65667, 65666, 65665, 65664, 65663, 65662, 65661, 65660, 65659, 65658, 65657, 65656, 65655, 65654, 65653, 65652, 65651, 65650, 65566, 65561, 65533, 65525, 65513, 65496, 65495, 65494, 65463, 65455, 65419, 65400, 65399, 65373, 65270, 65269, 65215, 65214, 65213, 65212, 65193, 65183, 65182, 65123, 65122, 65121, 65120, 65119, 65118, 65114, 65023, 64936, 64933, 64932, 64836, 64807, 64806, 64805, 64704, 64684, 64683, 64682, 64641, 64627, 64626, 64624, 64623, 64622, 64621, 64620, 64595, 64587, 64520, 64462, 64430, 64374, 64373, 64372, 64205, 64204, 64172, 64130, 64126, 64123, 64104, 64091, 64084, 64083, 64082, 64073, 64072, 64071, 64065, 64029, 63972, 63971, 63970, 63969, 63957, 63925, 63901, 63900, 63896, 63895, 63805, 63804, 63789, 63787, 63755, 63754, 63732, 63731, 63686, 63685, 63362, 63361, 63360, 63359, 63358, 63357, 63356, 63355, 63354, 63283, 63236, 63222, 63056, 63055, 63054, 63053, 63052, 63051, 63050, 63049, 63048, 63047, 63045, 63031, 63030, 62992, 62896, 62841, 62840, 62839, 62793, 62749, 62732, 62728, 62547, 62498, 62495, 62494, 62401, 62293, 62138, 62137, 62090, 62089, 62045, 62044, 61743, 61742, 61741, 61740, 61676, 61675, 61674, 61654, 61484, 61438, 61323, 61304, 61267, 61266, 61251, 61152, 61150, 61143, 61142, 61088, 60532, 60527, 60526, 60525, 60486, 60457, 60421, 60229, 60178, 60177, 60176, 59896, 59789, 59754, 59753, 59656, 59629, 59628, 59540, 59538, 59505, 59440, 59367, 59365, 59328, 59326, 59210, 59201, 59192, 59184, 59147, 59146, 59036, 58855, 58854, 58828, 58804, 58803, 58802, 58776, 58775, 58759, 58714, 58713, 58606, 58605, 58604, 58603, 58602, 58601, 58600, 58599, 58598, 58597, 58507, 58483, 58482, 58481, 58480, 58479, 58464, 58301, 58289, 58243, 58220, 58219, 58218, 58217, 58215, 57963, 57962, 57885, 57884, 57883, 57882, 57881, 57850, 57849, 57841, 57805, 57792, 57750, 57655, 57499, 57498, 57497, 57496, 57495, 57493, 57492, 57491, 57490, 57489, 57488, 57487, 57486, 57485, 57484, 57483, 57482, 57481, 57480, 57479, 57448, 57447, 57355, 57119, 56965, 56955, 56933, 56932, 56899, 56898, 56862, 56795, 56792, 56725, 56674, 56673, 56672, 56659, 56658, 56657, 56656, 56655, 56654, 56544, 56533, 56531, 56494, 56452, 56451, 56436, 56394, 56234, 56214, 56117, 56063, 56062, 56036, 56031, 56028, 56027, 56012, 56011, 56010, 56009, 56007, 55954, 55953, 55952, 55876, 55796, 55741, 55740, 55739, 55738, 55737, 55736, 55735, 55734, 55701, 55633, 55595, 55594, 55470, 55469, 55420, 55419, 55393, 55391, 55338, 55337, 55319, 55216, 55215, 55205, 55166, 55165, 55116, 55115, 55109, 55102, 55036, 55035, 55034, 55029, 55028, 54980, 54895, 54873, 54864, 54847, 54791, 54725, 54724, 54723, 54680, 54616, 54533, 54518, 54490, 54489, 54483, 54482, 54450, 54449, 54383, 54377, 54348, 54316, 54315, 54314, 54313, 54299, 54298, 54294, 54293, 54220, 54219, 54218, 54039, 54038, 54037, 54036, 53837, 53655, 53653, 53650, 53626, 53615, 53607, 53595, 53592, 53591, 53590, 53577, 53503, 53468, 53467, 53382, 53370, 53142, 53066, 52950, 52949, 52713, 52712, 52711, 52662, 52366, 52349, 52348, 52347, 52346, 52224, 52223, 52222, 52221, 52220, 52148, 52147, 52146, 52145, 52142, 51949, 51894, 51818, 51771, 51741, 51662, 51632, 51623, 51560, 51514, 51416, 51415, 51388, 51374, 51364, 51363, 51274, 51056, 51055, 50988, 50987, 50893, 50891, 50890, 50863, 50857, 50764, 50695, 50682, 50581, 50537, 50536, 50519, 50517, 50516, 50494, 50493, 50442, 50327, 50326, 50325, 50157, 50136, 50135, 50132, 50014, 49943, 49933, 49932, 49871, 49684, 49291, 49099, 48915, 48835, 48694, 48693, 48495, 48494, 48493, 48492, 48491, 48490, 48489, 48488, 48266, 48260, 48259, 48258, 48156, 48155, 48154, 48128, 48125, 48124, 48123, 48118, 48107, 47909, 47839, 47822, 47696, 47695, 47694, 47693, 47692, 47691, 47690, 47503, 47502, 47338, 47337, 47336, 47166, 47154, 47013, 47012, 46583, 46418, 46417, 46416, 46415, 46414, 46413, 46412, 46352, 45320, 45219, 45061, 45060, 44965, 44964, 44894, 44893, 44373, 44332, 44331, 44330, 44193, 43381, 42890, 42889, 42888, 42887, 42886, 42885, 42884, 42477, 42475, 42409, 41764, 41332, 41180, 39413, 39412, 39411, 39410, 39409, 39408, 39407, 39406, 39405, 39404, 39403, 39402, 39401, 39400, 39399, 39398, 39397, 39396, 39395, 39394, 39393, 39392, 39391, 39390, 39389, 39388, 39387, 39386, 39385, 39384, 39383, 37623, 37622, 34699, 34698, 33422, 33421, 32268, 32336, 32335, 31936, 31935]
flats = []
current_date = datetime.now().date()

def extract_digits_or_original(s):
    digits = ''.join([char for char in s if char.isdigit()])
    return int(digits) if digits else s
offset_counter = 0

for building_id in buildings_id:

    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/{building_id}'


    driver.get(url=url)
    page_content = driver.page_source  # Получаем HTML страницы после полной загрузки JavaScript
    soup = BeautifulSoup(page_content, 'html.parser')
    info = soup.find_all('div', class_="Row__Value-sc-13pfgqd-2 dySlPJ")
    i = []
    for inf in info:

        i.append(inf.text)

    print(i)


    if len(i) == 8:
        developer = i[0]
        developer_group = i[1]
        project_declaration = i[2]
        publication_date = i[3]
        explotation_start_date = i[4]
        keys_date = i[5]
        avg_metr_price = i[6]
        flats_sales_perc = i[7]
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
    finish_type = i[5]
    is_free_plan = i[7]
    floors_count = i[9]
    flats_count = i[11]
    living_area = i[13]
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

    res = [building_id, developer, developer_group, project_declaration, publication_date, explotation_start_date, keys_date, avg_metr_price, flats_sales_perc, klass, material,
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

df = pd.DataFrame(flats, columns=['id',
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





