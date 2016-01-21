
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


# In[ ]:



