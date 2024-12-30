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

def scrape_spell(links):
    '''Scrapes the individual spell information and puts it into an object before returning the list of objects'''
    for level in links:
        for spell in level:
            url = f'https://dnd5e.wikidot.com{spell}'
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            print(soup)

def scrape_spell_links():
    '''gets all of the hrefs from the tables at the following address: https://dnd5e.wikidot.com/spells and returns it as a list of lists ordered by spell level'''
    url = 'https://dnd5e.wikidot.com/spells'
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    hrefs_arr = []
    for level in range(0,10):    
        links = soup.select(f"#wiki-tab-0-{level} tr a")
        hrefs = [link['href'] for link in links]
        hrefs_arr.append(hrefs)


def scrape_spells_brain():
    '''Scrapes all of the spells from https://dnd5e.wikidot.com/spells and returns them as a list of objects'''

    links = scrape_spell_links()
    scrape_spell(links)
    
scrape_spells_brain()