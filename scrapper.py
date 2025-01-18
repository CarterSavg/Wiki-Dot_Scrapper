import requests
from bs4 import BeautifulSoup

class spell:
    def __init__(self, name, school, desc, level, casting_time, distance, components, duration, users, higher_level = None):
        self.name = name
        self.school = school
        self.desc = desc
        self.higher_level = higher_level
        self.level = level
        self.casting_time = casting_time
        self.distance = distance
        self.components = components
        self.duration = duration
        self.users = users 


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
    #TODO:
    # create class and constructor
    '''Scrapes the individual spell information and puts it into an object before returning the list of objects'''
    for level_num, level in enumerate(links):
        for spell in level:
            url = f'https://dnd5e.wikidot.com{spell}'
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            content = soup.select("#page-content p")
            title = soup.select(".page-title")
            print(title[0].text)
            if level_num > 0:
                print(f"school {content[1].text.split(" ")[-1].capitalize()}")
            else:
                print(f"school {content[1].text.split(" ")[0].capitalize()}")
            casting_time = soup.find('strong', string='Casting Time:').next_sibling.strip()
            range_ = soup.find('strong', string='Range:').next_sibling.strip()
            components = soup.find('strong', string='Components:').next_sibling.strip()
            duration = soup.find('strong', string='Duration:').next_sibling.strip()
            try:
                users = content[-1].text.replace(" ", "").split(".")[1].split(",") #getting all users after the . in "Spell List."
            except IndexError: #Spell List has a : instead of a . 
                users = content[-1].text.replace(" ", "").split(":")[1].split(",") #getting all users after the : in "Spell List:"  
            desc = ""
            higher_levels = None
            try:
                higher_levels = soup.find('strong', string=('At Higher Levels.', 'At Higher Levels:')).next_sibling.strip()
            except:
                pass
            print("Casting Time:", casting_time)
            print("Range:", range_)
            print("Components:", components)
            print("Duration:", duration)
            print(f"users {users}")
            if higher_levels:
                print(higher_levels)
                for part in content[3:-2]:
                    desc += part.text
                extra = soup.select("#page-content ul")
                for part in extra:
                    desc += part.text
                print(desc)
            else:
                for part in content[3:-1]:
                    desc += part.text
                extra = soup.select("#page-content ul")
                for part in extra:
                    desc += part.text
                print(desc)

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