import requests
from bs4 import BeautifulSoup

url = 'https://dnd5e.wikidot.com/'
page = requests.get(url, timeout=10)
soup = BeautifulSoup(page.content, 'html.parser')
classes = soup.select("h1 span a")
for name in classes:
    print(name.text)