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
    # for level in links:
    #     for spell in level:
    url = f'https://dnd5e.wikidot.com{links[0][0]}'
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.select("#page-content p")
    title = soup.select(".page-title")
    print(title[0].text)
    print(f"school {content[1].text}")
    casting_time = soup.find('strong', string='Casting Time:').next_sibling.strip()
    range_ = soup.find('strong', string='Range:').next_sibling.strip()
    components = soup.find('strong', string='Components:').next_sibling.strip()
    duration = soup.find('strong', string='Duration:').next_sibling.strip()
    higher_levels = None
    try:
        higher_levels = soup.find('strong', string='At Higher Levels.').next_sibling.strip()
    except:
        pass
    # print("Casting Time:", casting_time)
    # print("Range:", range_)
    # print("Components:", components)
    # print("Duration:", duration)
    # print(f"users {content[-1].text.replace(" ", "").split(".")[1].split(",")}")
    if higher_levels:
        print(higher_levels)

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
    return hrefs_arr

def scrape_spells_brain():
    '''Scrapes all of the spells from https://dnd5e.wikidot.com/spells and returns them as a list of objects'''

    links = scrape_spell_links()
    scrape_spell(links)
    
scrape_spells_brain()