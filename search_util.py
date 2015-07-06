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

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def ordered_search(index, ranks, keyword):
    results = lookup(index, keyword)
    if not results:
        return None
    else:
        quick_sort_utility(ranks, results, 0, len(results)-1)
        return results    