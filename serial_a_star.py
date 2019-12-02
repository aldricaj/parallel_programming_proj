import link_parser

unused = []
endPage = '/wiki/University_of_Utah_School_of_Medicine'

def pathToPage(page):
    path = [page.page_url]
    while page.parent != '':
        path.append(page.parent.page_url)
        page = page.parent
    return path

def heuristic(page):
    return page.depth / page.num_sub_pages

def initSubpage(page, subpageLink):
    page2 = link_parser.Page(subpageLink)
    page2.parent = page
    page2.depth = page.depth + 1
    page2.heuristic = heuristic(page2)
    return page2

def findPage(page):
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

def main():
    startURL = 'https://en.wikipedia.org/wiki/Handsfree'
    page = link_parser.Page(startURL)
    if endPage in page.links:
        print('Starting page already contains the end page link')
        return
    
    while page:
        page = findPage(page)
     
if __name__ == '__main__':
    main()
