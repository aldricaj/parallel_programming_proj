import link_parser
import multiprocessing as mp
import time

sharedList = []
nextPage = None
endPage = '/wiki/World_Trade_Organization'

def pathToPage(page):
    path = [page.page_url]
    while page.parent != '':
        path.append(page.parent.page_url)
        page = page.parent
    return path

def heuristic(page):
    return page.depth / page.num_sub_pages

def parallelHeuristic(page):
    page.heuristic = heuristic(page)
    return page

def initSubpage(subpageLink):
    page2 = link_parser.Page(subpageLink)
    return page2

def createSubpages(page, subpageLink):
    page2 = initSubpage(subpageLink)
    page2.parent = page
    page2.depth = page.depth + 1
    parallelHeuristic(page2)
    return page2

def findPage(page):
    if sharedList != []:
        sharedList.sort(key=lambda x: x.heuristic)
        nextPage = sharedList[0]
        nextPageHeuristic = heuristic(nextPage)
    else:
        nextPage = link_parser.Page(page.links[0])
        nextPageHeuristic = 1
    
    # This is where I am having trouble
    # Removing these next three lines results in the serial code
    #pool = mp.Pool(mp.cpu_count())
    #results = [pool.apply(createSubpages, args=(page, subpageLink)) for subpageLink in page.links]
    #print(results)
     
    # This for loop would be modified/removed with working parallel code   
    for subpageLink in page.links:
        page2 = createSubpages(page, subpageLink)
        
        if endPage in page2.links:
            print(pathToPage(page2))
            return False
        if heuristic(page2) < nextPageHeuristic:
            nextPage = page2
            nextPageHeuristic = heuristic(nextPage)
        sharedList.append(page2)
    
    for i in range(len(sharedList)-1):
        if sharedList[i].page_url == nextPage.page_url:
            sharedList.pop(i)
            break 
    print(nextPage.page_url)
    return nextPage

def main():
    print("Number of processors: ", mp.cpu_count())
    start_time = time.time()

    startURL = 'https://en.wikipedia.org/wiki/Handsfree'
    page = link_parser.Page(startURL)
    if endPage in page.links:
        print('Starting page already contains the end page link')
        return
    
    while page:
        page = findPage(page)
     
    print("Total Time: %s seconds " % (time.time() - start_time))
if __name__ == '__main__':
    main()