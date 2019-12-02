import requests
import bs4


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
    if link.get('href').lower().startswith('ftp'):
        return False
    return True

class Page:
    def __init__(self, page_url):
        
        if page_url.startswith('/'):
            page_url = 'https://en.wikipedia.org' + page_url
        self.page_url = page_url
        self.parent = ''
        self.depth = 0
        self.heuristic = 0

        ## Get HTML

        r = requests.get(self.page_url)
        r.raise_for_status()

        ## Parse HTML and get links
        self.html = bs4.BeautifulSoup(r.text, features='html.parser')
        self.links = list(set([tag.get('href') for tag in filter(filter_links, self.html.find_all('a'))]))

        self.num_sub_pages = len(self.links)

def get_links(url):
    return Page(url).links
        
if __name__ == '__main__':
    page = Page('https://en.wikipedia.org/wiki/Canon_law')
    page2 = Page(' ')
    links = page.links
    first_link = page.links[0]
    num_links = page.num_sub_pages
    page2 = Page(links[0])
