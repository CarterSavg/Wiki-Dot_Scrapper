import os
import psycopg2
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

class Spell:
    def __init__(self, name, school, desc, level, casting_time, distance, components, duration, users, material, verbal, somatic, higher_level = None, mat_desc = None):
        self.name = name
        self.school = school
        self.desc = desc
        self.higher_level = higher_level
        self.level = level
        self.casting_time = casting_time
        self.distance = distance
        self.components = components
        self.material = material
        self.mat_desc = mat_desc
        self.verbal = verbal
        self.somatic = somatic
        self.duration = duration
        self.users = users 
    
    def __str__(self):
        result = f"{self.name}\nLevel: {self.level}\nV: {self.verbal} \tS: {self.somatic} \t M: {self.material} {self.mat_desc}\nSchool: {self.school}\nCasting time: {self.casting_time}\nRange: {self.distance}\nDuration: {self.duration}\n\n{self.desc}\n"
        if self.higher_level:
            result += f"At Higher Levels: {self.higher_level}\n"
        result += f"Spell Lists:{self.users}\n\n"
        return result 
    

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

def scrape_spell_description(soup, content, higher_levels):
    '''Get spell description. Is slightly different if it is a level 0 than all the others (Transmutation cantrip) vs (2nd-level evocation)'''
    desc = ""
    if higher_levels:
        for part in content[3:-2]:
            desc += part.text
        extra = soup.select("#page-content ul")
        for part in extra:
            desc += part.text
    else:
        for part in content[3:-1]:
            desc += part.text
        extra = soup.select("#page-content ul")
        for part in extra:
            desc += part.text
    return desc

def scrape_spell_details(soup, level_num):
    '''Getting all the information for the spell from the soup and returning it as a Spell object'''
    content = soup.select("#page-content p")
    title = soup.select(".page-title")
    school = ""
    mat_desc = None
    if level_num > 0:
        school = content[1].text.split(" ")[-1].capitalize()
    else:
        school = content[1].text.split(" ")[0].capitalize()
    casting_time = soup.find('strong', string='Casting Time:').next_sibling.strip()
    range_ = soup.find('strong', string='Range:').next_sibling.strip()
    duration = soup.find('strong', string='Duration:').next_sibling.strip()
    components = soup.find('strong', string=re.compile(r'Components:?'))
    if components:
        components = components.next_sibling.strip()
    else:
        components = None
    try:
        users = content[-1].text.replace(" ", "").split(".")[1].split(",") #getting all users after the . in "Spell List."
    except IndexError: #Spell List has a : instead of a . 
        users = content[-1].text.replace(" ", "").split(":")[1].split(",") #getting all users after the : in "Spell List:"  
    higher_levels = None
    try:
        higher_levels = soup.find('strong', string=('At Higher Levels.', 'At Higher Levels:')).next_sibling.strip()
    except:
        pass
    if "M" in components:
        mat_desc = components.replace(")", "").split("(")[-1]
    desc = scrape_spell_description(soup, content, higher_levels)
    spell = Spell(title[0].text, school, desc, level_num, casting_time, range_, components, duration, users, "M" in components, "V" in components, "S" in components, higher_levels, mat_desc)
    print(spell)
    return spell

def scrape_spell(links):
    #TODO:
    # Maybe don't scrape UA because its inconsistent
    spells = []
    '''Scrapes the individual spell information and puts it into an object before returning the list of objects'''
    for level_num, level in enumerate(links):
        for spell in level:
            url = f'https://dnd5e.wikidot.com{spell}'
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            spells.append(scrape_spell_details(soup, level_num))
    return spells
            

def scrape_spell_links():
    '''gets all of the hrefs from the tables at the following address: https://dnd5e.wikidot.com/spells and returns it as a list of lists ordered by spell level'''
    url = 'https://dnd5e.wikidot.com/spells'
    page = requests.get(url, timeout=10)
    soup = BeautifulSoup(page.content, 'html.parser')
    hrefs_arr = []
    for level in range(0,1):    
        links = soup.select(f"#wiki-tab-0-{level} tr a")
        hrefs = [link['href'] for link in links]
        hrefs_arr.append(hrefs)
    return hrefs_arr

def database_setup(spells):
    cursor, conn = create_spells_tables()
    populate_spells(cursor, conn, spells)

def populate_spells(cursor, conn, spells):
    for spell in spells:
        # TODO: create spell commit message
        print(spell)
        print((spell.name, spell.school, spell.desc, spell.higher_level, spell.level, spell.casting_time, spell.distance, spell.verbal, spell.somatic, spell.material, spell.mat_desc, spell.duration, spell.users))
        cursor.execute("""
        INSERT INTO spells (
        name,
        school,
        description,
        higher_level,
        level,
        casting_time,
        distance,
        verbal,
        somatic,
        component,
        material_desc
        duration,
        users
        );
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (spell.name, spell.school, spell.desc, spell.higher_level, spell.level, spell.casting_time, spell.distance, spell.verbal, spell.somatic, spell.material, spell.mat_desc, spell.duration, spell.users))
        conn.commit()
    

def create_spells_tables():
    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL")

    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Create table if it doesn't exist 
    # NOTE: change VSM to be bools in the spells class and add a materials section if there are material components (also maybe a cost section for mats)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spells (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    school TEXT NOT NULL,
    description TEXT NOT NULL,
    higher_level TEXT,
    level INT NOT NULL,
    casting_time TEXT NOT NULL,
    distance TEXT NOT NULL,
    verbal BOOLEAN NOT NULL,
    somatic BOOLEAN NOT NULL,
    component BOOLEAN NOT NULL,
    material_desc TEXT,
    duration TEXT NOT NULL,
    users TEXT[] 
    );""")
    conn.commit()
    
    # UA table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UA (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    school TEXT NOT NULL,
    description TEXT NOT NULL,
    higher_level TEXT,
    level INT NOT NULL,
    casting_time TEXT NOT NULL,
    distance TEXT NOT NULL,
    verbal BOOLEAN NOT NULL,
    somatic BOOLEAN NOT NULL,
    material BOOLEAN NOT NULL,
    material_desc TEXT,
    duration TEXT NOT NULL,
    users TEXT[] 
    );""")
    conn.commit()
    print("Connected to database!")
    return cursor, conn

def scrape_spells_brain():
    '''Scrapes all of the spells from https://dnd5e.wikidot.com/spells creates the tables and populates them'''

    links = scrape_spell_links()
    spells = scrape_spell(links)
    database_setup(spells)
    
    

scrape_spells_brain()