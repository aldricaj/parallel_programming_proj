import link_parser
import time
import sys

unused = []

def pathToPage(page):
    print('Most efficient path to end page:')
    path = [page.page_url]
    while page.parent != '':
        path.append(page.parent.page_url)
        page = page.parent
    path.reverse()
    return path

def heuristic(page):
    return page.depth / page.num_sub_pages

def initSubpage(page, subpageLink):
    page2 = link_parser.Page(subpageLink)
    page2.parent = page
    page2.depth = page.depth + 1
    page2.heuristic = heuristic(page2)
    return page2

def findPage(page, endPage):
    nextPageHeuristic = 1
    if unused != []:
        unused.sort(key=lambda x: x.heuristic)
        nextPage = unused[0]
    else:
        nextPage = link_parser.Page(page.links[0])
        
    for subpageLink in page.links:
        page2 = initSubpage(page, subpageLink)
        if endPage in page2.links:
            print(pathToPage(page2))
            return False
        if heuristic(page2) < nextPageHeuristic:
            nextPage = page2
            nextPageHeuristic = heuristic(nextPage)
        unused.append(page2)
        
    print(nextPage.page_url)
    return nextPage

def checkArguments():
    if (len(sys.argv) == 2):
        return False
    return True

def defaultPages():
    startURL = 'https://en.wikipedia.org/wiki/'
    endPage = '/wiki/'
    useDefaultURLs = checkArguments()
    if (useDefaultURLs):
        print('No arguments passed for start page and end page.\nUsing default pages...\n')
        startURL = startURL + 'Handsfree'
        endPage = endPage + 'University_of_Utah_Honors_College'
    else:
        startURL = startURL + sys.argv[1]
        endPage = endPage + sys.argv[2]
    defaultPages = [startURL, endPage]
    return defaultPages

def main():
    wikiPages = defaultPages()
    startURL = wikiPages[0]
    endPage = wikiPages[1]
        
    start_time = time.time()
    
    try:
        page = link_parser.Page(startURL)
    except:
        print('Start page or end page is not valid!\nPlease ensure page name is correct\nExample Arguments: Handsfree University_of_Utah_Honors_College')
        return
        
    if endPage in page.links:
        print('Starting page already contains the end page link')
        return
    
    while page:
        page = findPage(page, endPage)
     
    print("Total Time: %s seconds " % (time.time() - start_time))
if __name__ == '__main__':
    main()