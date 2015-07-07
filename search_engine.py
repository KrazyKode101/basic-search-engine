import sys
from clean_page import clean_page
from database import cache

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)
					
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
    
def extract_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_page(url):
    if url in cache:
        return cache[url]
    return ""
		
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  #[url] = [url1,url2,...urln] [list of pages it has links to]
    index = {}  #[keyword] = [url1,url2,...urln] [list of pages keyword is in]
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            outlinks = extract_all_links(content)
            content = clean_page(content)
            add_page_to_index(index, page, content)            
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def main():
    #crawl web   
    index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')

    #compute ranks
    from compute_ranks import compute_ranks
    ranks = compute_ranks(graph,10) #where rank is [url] = [a number indicating rank of the web page]

    #perform search
    from search_util import ordered_search

    # Here are some example showing what ordered_search should do:
    # Observe that the result list is sorted so the highest-ranking site is at the
    # beginning of the list.

    print ordered_search(index, ranks, 'Hummus')
    #>>> ['http://udacity.com/cs101x/urank/kathleen.html',
    #    'http://udacity.com/cs101x/urank/nickel.html',
    #    'http://udacity.com/cs101x/urank/arsenic.html',
    #    'http://udacity.com/cs101x/urank/hummus.html',
    #    'http://udacity.com/cs101x/urank/index.html']

    print ordered_search(index, ranks, 'the')
    #>>> ['http://udacity.com/cs101x/urank/nickel.html',
    #    'http://udacity.com/cs101x/urank/arsenic.html',
    #    'http://udacity.com/cs101x/urank/hummus.html',
    #    'http://udacity.com/cs101x/urank/index.html']

    print ordered_search(index, ranks, 'babaganoush')
    #>>> None

if __name__ == '__main__':
    main()