from bs4 import BeautifulSoup

url = "<a href=\"/msk/zhilye-kompleksy/wave/\"  target=\"_blank\" class=\"isColorAlizarinCrimson\"> в ЖК WAVE</a>"

soup = BeautifulSoup(url, 'html.parser')
flats_soup = soup.find('a')
print(flats_soup.text)
