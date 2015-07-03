cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}


def quick_sort(ranks,results,start,end):
    if not results:
        return
    
    pivot = end
    i = start - 1    
    for j in range(start,end):
        if ranks[ results[j] ] <= ranks[ results[pivot] ] :
            temp = results[i+1]
            results[i+1] = results[j]
            results[j] = temp
            i += 1    
    temp = results[i+1]
    results[i+1] = results[pivot]
    results[pivot] = temp
    
    return i+1

	
def quick_sort_utility(ranks,results,start,end):    
    if start<end:        
        p = quick_sort(ranks,results,start,end)
        quick_sort_utility(ranks, results, start, p-1)        
        quick_sort_utility(ranks, results, p+1, end)                
    return

	
def ordered_search(index, ranks, keyword):
    results = lookup(index, keyword)
    if not results:
        return None
    else:
        quick_sort_utility(ranks, results, 0, len(results)-1)
        return results
		

def get_page(url):
    if url in cache:
        return cache[url]
    return ""


def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

	
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)
			

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

		
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

		
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

		
def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  # <url>, [list of pages it has links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def get_len_between(graph,visited,page1,page2):
    visited.append(page1)
    outlinks = graph[page1]
    if page2 in outlinks:
        if page1==page2:
            return 0
        else:
            return 1
    else:
        minimum = 10000
        for e in outlinks:                
            if e not in visited:
                length = 1 + get_len_between(graph,visited,e,page2)
                if length < minimum:
                    minimum = length
        return minimum                                            

def get_len_between_utility(graph,page1,page2):
    visited = []
    return get_len_between(graph,visited,page1,page2)   
    
def is_not_reciprocal(graph,page1,page2,k):    
    if get_len_between_utility(graph,page1,page2) <= k:
        return False
    else:
        return True

def get_rank(graph,ranks,d,page,k):
    rank = 0
    for node in graph:
        if page in graph[node] and is_not_reciprocal(graph,page,node,k):
            rank = rank + d * (ranks[node]/len(graph[node]))
    return rank

def compute_ranks(graph,k):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)        
    for page in graph:
        ranks[page] = 1.0 / npages
        
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            newrank += get_rank(graph,ranks,d,page,k) 
            newranks[page] = newrank
        ranks = newranks
    return ranks



# Here are some example showing what ordered_search should do:

# Observe that the result list is sorted so the highest-ranking site is at the
# beginning of the list.

# Note: the intent of this question is for students to write their own sorting
# code, not to use the built-in sort procedure.

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

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