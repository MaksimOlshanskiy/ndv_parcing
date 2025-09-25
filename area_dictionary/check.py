import json

with open('normalized_output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_values = {v for inner in data.values() for v in inner.values()}

print(all_values)
import json
import re

lst = {0, 1, 2, 3, 4, '6е', 5, '5 2 ур', 7, 6, '9е', 'пент.', 'студия', 'mr', '4 2 ур', '2е', 'коттеджи', '3 2 ур',
       '3е 2 ур', '7е', 'Студия', '2е 2 ур', '1 2 ур', '4е', '4е 2 ур', '5е', '8е 2 ур', 'пентхаус', '2 ур', '3е',
       'тип', 'таунхаус', '2 2 ур', '5е 2 ур', '6е 2 ур', '8е', 'st', '10е', '7е 2 ур', '7 2 ур'}

# original_set = {0, 1, 2, 3, 4, 5, '2 ур. 5е', 'коттеджи', 7, 'таунхаус', 6, '4eph', '2 ур. 4е', '5еLph (терр.+бассейн)',
#                 '7еph', 'пентхаусы', 'ph (терр.)', '2е ', '2еL', '8еLph (терр.)', '3к2L', '2 (терр.)',
#                 'студия (антресоль)',
#                 '7 ph', '3 (терр.)', '3е(терр)', '5eph', '5е терр.', '1 (терр.)', '4е2L', '5 ph', 'студия (терр.)',
#                 'студия ', 'ph', '5е', 'phL (терр.)', '3еL терр.', '2 ур. 3е', '4ph', '5еph', '4еL (терр.)',
#                 '2е (антресоль)', '4 2-ур', '7е', '2еph', '5еL (таун)', '5еL', '5ph', '7еph (терр.)', '10е', 'mr',
#                 '6еph (терр.)', '2e', '2L4e', '3е (терр.)', 'студия', '6еL (таун)', 'студия\xa0', '3е ', '4е', '6eph',
#                 '4еLph', '2еL (терр.)', '5еLph', '5е терр', '3еph (терр.)', '7еL (терр.)', '2к2L', '6еph',
#                 '6еphL (терр.)',
#                 '7е ph', '4 ph(терр.)', '5е 2-ур терр', '8еph', '4L', '6е (терр.)', '9еLph (терр.+бассейн)',
#                 '4еL ph (терр.)', '2L', '4еL (таун)', '10еLph', '5е city house', '4е(терр)', '4e', '3еph', '4еL',
#                 '2 ур.5е',
#                 '3е терр', '4е (таунхаус)', '6е 2-ур', '5e', '4е терр.', 'Студия', '4еL (патио)', '4еph (терр.)', '3е',
#                 '2е (терр.)', '5е (терр.)', 'Студия ', '7L', '4е 2-ур', 'mr (вилла)', '2е', '4е ph', '3еL (патио)',
#                 '3е(терр.)', '4еL city house', '6еL (терр.)', '5eph (терр.)', '6е 2-ур терр', '3е ph', '4еph', '6е ph',
#                 'таунхаусы', '6еL', '1 (ситихаус)', '2еL city house', '8е', '3е 2-ур', 'тип', '6еLph (терр.+бассейн)',
#                 '7е (терр.)', '2е ph', '6е', '3еL', '7еL ph (терр.)', '8еL', '5еL (терр.)', '2 ур', '4ph (терр.)', '9е',
#                 '2 р. 5е', '2е (ситихаус)', '6еL (терр.) city house', '3e', '2л', '5еL  ', '3еL city house', '7еL',
#                 '5е ph',
#                 '5еLph (терр.)', '3е (терр)', '3еL (терр.)', '3L', '6еL ph (терр.)', '5L', '3e ph', 'st',
#                 '7е 2-ур терр',
#                 '5еph (терр.)', '7е 2-ур', '6eL (терр.)', '7еLph', '4е (терр.)', 'таун', '5eLph (терр.)', '2е(терр)',
#                 '5е 2-ур', '9еL ph (терр.)', '1L'}
#
#
# # Суффиксы, которые надо убрать
# suffixes = [
#     '(терр.)', '(терр.+бассейн)', '(терр)', ' терр', ' терр.', ' (антресоль)', ' (патио)', ' city house',
#     ' (ситихаус)', '(терр.)', '(терр.)'
# ]
#
# # Если любой из них встречается — значение меняем на 'таунхаус'
# taun_variants = ['(таун)', 'таун', 'таунхаус', '(таунхаус)', 'таунхаусы', '(вилла)']
#
# level_replacements = {
#     'к2L': '2 ур',
#     'л': '2 ур',
#     'L': '2 ур',
#     '2-ур': '2 ур',
#     '2 ур.': '2 ур',
#     '2 р.': '2 ур',
#     '2ур.': '2 ур',
#     '2ур': '2 ур'
# }
#
# cleaned_set = set()
#
# for val in original_set:
#     if isinstance(val, str):
#         # Ручная замена конкретного случая (если нужно)
#         val = val.replace('6еL (терр.)', '6еL')
#
#         # Если есть любой из таунхаус-вариантов — заменяем всё значение
#         if any(variant in val for variant in taun_variants):
#             val = 'таунхаус'
#         else:
#             # Удаляем суффикс (если есть)
#             for suffix in suffixes:
#                 if val.endswith(suffix):
#                     val = val[:-len(suffix)].strip()
#                     break
#
#         cleaned_set.add(val.strip())
#     else:
#         cleaned_set.add(val)
#
# # Второй этап: замена ph на пент во всех строках
# ph_replaced_set = set()
#
# for item in cleaned_set:
#     if isinstance(item, str):
#         # Заменяем 'ph' на 'пент' с проверкой пробела
#         if 'ph' in item:
#             parts = item.split('ph')
#             modified_item = []
#             for i, part in enumerate(parts[:-1]):
#                 modified_item.append(part)
#                 # Проверяем, есть ли пробел перед ph
#                 if part and not part.endswith(' '):
#                     modified_item.append(' пент.')
#                 else:
#                     modified_item.append('пент.')
#             modified_item.append(parts[-1])
#             modified_item = ''.join(modified_item)
#         else:
#             modified_item = item
#
#         ph_replaced_set.add(modified_item)
#     else:
#         ph_replaced_set.add(item)
#
# # Третий этап: замена вариантов уровня на "2 ур" и перенос в конец
# final_set = set()
#
# for item in ph_replaced_set:
#     if isinstance(item, str):
#         modified_item = item
#
#         # Специальная обработка для "к2L" (сохраняем цифру перед "к")
#         if 'к2L' in modified_item:
#             parts = modified_item.split('к2L')
#             # Сохраняем цифру перед "к"
#             if parts[0] and parts[0][-1].isdigit():
#                 modified_item = f"{parts[0]} 2 ур{' '.join(parts[1:])}"
#             else:
#                 modified_item = ' '.join(parts) + ' 2 ур'
#
#         # Обработка остальных вариантов
#         for variant, replacement in level_replacements.items():
#             if variant != 'к2L' and variant in modified_item:
#                 modified_item = modified_item.replace(variant, replacement)
#
#         # Переносим все "2 ур" в конец
#         if '2 ур' in modified_item:
#             parts = [p.strip() for p in modified_item.split('2 ур') if p.strip()]
#             count = modified_item.count('2 ур')
#             modified_item = ' '.join(parts) + ' 2 ур' * count
#
#         modified_item = modified_item.replace('4е2 2 ур', '4е 2 ур')
#         modified_item = modified_item.replace('2 4e 2 ур', '4e 2 ур')
#
#         final_set.add(modified_item.strip())
#     else:
#         final_set.add(item)
#
# # Четвертый этап: преобразование строк в int, где это возможно
# processed_set = set()
# for item in final_set:
#     if isinstance(item, str):
#         # Пробуем преобразовать строку в int
#         try:
#             num = int(item)
#             processed_set.add(num)
#         except ValueError:
#             processed_set.add(item)
#     else:
#         processed_set.add(item)
#
# normalize_set = set()
# for item in processed_set:
#     if isinstance(item, str):
#         word = item.replace('e', 'е')
#         normalize_set.add(word)
#     else:
#         normalize_set.add(item)
#
# print(normalize_set)
