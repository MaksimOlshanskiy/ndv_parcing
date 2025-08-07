import requests
from bs4 import BeautifulSoup

url = 'https://dream-towers.ru/'

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Ищем все блоки объявлений по классу, который ты привел
# Обычно в таких случаях лучше искать по наиболее уникальному классу,
# здесь у тебя есть "bg-white-100 rounded-lg transition cursor-pointer ..."
# Можно искать по "bg-white-100" или "rounded-lg" вместе с "cursor-pointer"
# или же просто по селектору, который включает эти классы

# Пример поиска по классу bg-white-100 (может быть много других блоков с таким классом)
blocks = soup.find_all('div', class_='bg-white-100')

for block in blocks:
    # Внутри блока попробуем найти основные элементы, например название, площадь, цену
    # Тут нужно смотреть реальную структуру, но предположим:

    # Цена (примерно)
    price_div = block.find('div', class_='pb-3.5 border-b border-olive-100 mb-3.5 text-black-100 t3')
    price = price_div.get_text(strip=True) if price_div else 'Цена не указана'

    # Площадь - например, в тексте может быть что-то вроде "Площадь: 56 м²"
    # Попробуем найти все <div> с текстом, где есть "м²"
    area_div = None
    for div in block.find_all('div'):
        if div.string and 'м²' in div.string:
            area_div = div
            break
    area = area_div.get_text(strip=True) if area_div else 'Площадь не указана'

    print(f'Название: Цена: {price}, Площадь: {area}')
