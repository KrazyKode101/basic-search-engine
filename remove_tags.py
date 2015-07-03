def remove_tags(ip):    
    tag_start = ip.find('<',0)    
    while tag_start != -1:        
        tag_end = ip.find('>',tag_start)
        print tag_start,tag_end
        ip = ip[:tag_start] + ' ' + ip[tag_end+1:]
        tag_start = ip.find('<',0)  
    return ip.split()
    
print remove_tags('''<h1>Title</h1><p>This is a <a href="http://www.udacity.com">link</a>.<p>''')
