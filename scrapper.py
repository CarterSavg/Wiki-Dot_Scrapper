import requests
from bs4 import BeautifulSoup

def scrape_classes():
    '''Scrapes the classes from dnd5e wikidot using the classes.txt file as the extensions for each class'''
    file = open("classes.txt", "r")
    extensions = file.read().splitlines()

    for extension in extensions:
        if extension == "fighter":
            url = f'https://dnd5e.wikidot.com/{extension}'
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            print(soup.text)

def scrape_spells():
    url = 'https://dnd5e.wikidot.com/spells'
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    for level in range(0,10):    
        links = soup.select(f"#wiki-tab-0-{level} tr a")
        hrefs = [link['href'] for link in links]
        print(hrefs)
        # print(f'\nLevel {level}:')
        # for name in spells:
        #     print(name.text.lower().replace('/', ' ').replace(':', '').replace(' ', '-').replace("(hb)", ''))

scrape_spells()