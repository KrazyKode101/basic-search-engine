def get_len_between(graph,visited,page1,page2):
    visited.append(page1)
    outlinks = graph[page1]
    if page2 in outlinks:
        if page1==page2:
            return 0
        else:
            return 1
    else:
        minimum = float('inf')
        for e in outlinks:                
            if e not in visited:
                length = 1 + get_len_between(graph,visited,e,page2)
                if minimum==None or length < minimum:
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