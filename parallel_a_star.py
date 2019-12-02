import link_parser
import multiprocessing as mp
import time


sharedList = []
currentPage = None
endPage = '/wiki/University_of_Utah_Honors_College'

class Page:
    def __init__(self, page_url):
        self.page_url = page_url
        self.parent = ''
        self.depth = 0
        self.heuristic = 0
        self.links = getLinks(self.page_url)
        self.num_sub_pages = len(self.links)

def pathToPage(page):
    path = [page.page_url]
    while page.parent != '':
        path.append(page.parent.page_url)
        page = page.parent
    return path

def heuristic(page):
    return page.depth / page.num_sub_pages

def getLinks(subpageLink):
    return link_parser.get_links(subpageLink)

def setParent(page, parent):
    page.parent = parent
    page.depth = parent.depth + 1
    page.heuristic = heuristic(page)

def createSubpages(url):
    page = Page(url)
    page.links = getLinks(url)
    page.num_sub_pages = len(page.links)
    return page

def log_result(results):
    for result in results:
        if result.page_url not in sharedList:
            sharedList.append(result)

def findPage(page):
    pool = mp.Pool(mp.cpu_count())
    [pool.map_async(createSubpages, page.links, callback = log_result)]
    pool.close()
    pool.join()
    
    pool = mp.Pool(mp.cpu_count())
    [pool.apply_async(setParent, args = (newPage, page)) for newPage in sharedList]
    pool.close()
        
    for subpage in sharedList:
        for link in subpage.links:
            if endPage == link:
                print("SUCCESS")
                print(pathToPage(subpage))
                return False
        
    sharedList.sort(key=lambda x: x.heuristic)
    nextPage = sharedList[0]
    for i in range(len(sharedList)-1):
        if sharedList[i].page_url == nextPage.page_url:
            sharedList.pop(i)
            break 
    
    print(nextPage.page_url)
    print(len(sharedList))
    return nextPage

def main():
    startURL = 'https://en.wikipedia.org/wiki/Handsfree'
    print("Number of processors: ", mp.cpu_count())
    start_time = time.time()
    
    sharedList = link_parser.get_links(startURL)
    if endPage in sharedList:
        print('Starting page already contains the end page link')
        return
    
    page = Page(startURL)
    while page:
        page = findPage(page)
     
    print("Total Time: %s seconds " % (time.time() - start_time))
if __name__ == '__main__':
    main()
