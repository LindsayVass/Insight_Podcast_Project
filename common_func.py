
# coding: utf-8

# In[1]:

def convert_unicode(input):
    if isinstance(input, dict):
        return {convert_unicode(key): convert_unicode(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert_unicode(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# In[2]:

def check_url(url, num_tries, wait_secs):
    """Check whether a url is valid. Allows multiple checks with waiting in between."""
    import time
    import urllib2
    for x in range(0, num_tries):  
        try:
            urllib2.urlopen(url)
            str_error = None
        except urllib2.URLError as str_error:
            pass

        if str_error:
            time.sleep(wait_secs)  
        else:
            break
    return str_error


# In[ ]:



