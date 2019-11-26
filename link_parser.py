import requests
import bs4
r = requests.get("https://en.wikipedia.org/wiki/Littlemore_Priory_scandals#Atwater_investigates,_1517")
html = r.text
parser = bs4.BeautifulSoup(html, features='html.parser')
links = list(set(parser.find_all('a'))) # removes duplicates and then converts back to list

def filter_links(link):
    if not link.get('href'):
        return False
    if link.get('href')[0] == '#':
        return False
    if link.get('href').startswith('/w/'):
        return False
    if link.get('href').lower().startswith('/wiki/wikipedia'):
        return False
    if link.get('href').lower().startswith('/wiki/file'):
        return False
    if link.get('href').lower().startswith('/wiki/category'):
        return False
    if link.get('href').lower().startswith('//'):
        return False
    if link.get('href').lower().startswith('/wiki/special'):
        return False
    if link.get('href').lower().startswith('/wiki/portal'):
        return False
    if link.get('href').lower().startswith('/wiki/help'):
        return False
    if link.get('href').lower().startswith('/wiki/mainpage'):
        return False
    if link.get('href').lower().startswith('/wiki/talk'):
        return False
    if link.get('href').lower().startswith('http'):
        return False
    return True

filtered_links = [tag.get('href') for tag in filter(filter_links, links)]

for link in filtered_links:
    print(link)
    
