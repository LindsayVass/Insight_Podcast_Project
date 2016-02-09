import re
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer

# create list of stop words
stop = get_stop_words('en')

# remove non-alphanumeric, non-space
stop = [re.sub(r'([^\s\w]|_)+', '', x) for x in stop]

# add in custom stop words
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
other = ['nan', 'podcast']

[stop.append(unicode(day)) for day in days]
[stop.append(unicode(month)) for month in months]
[stop.append(unicode(x)) for x in other]


def remove_stop(text, stop):
    new_text = []
    for word in text:
        if word not in stop:
            new_text.append(word)
    return new_text


# create tokenizer
tokenizer = RegexpTokenizer(r'\w+')


# create stemmer
p_stemmer = PorterStemmer()


def stem_list(text, p_stemmer):
    new_list = []
    for word in text:
        new_list.append(p_stemmer.stem(word))
    return new_list


def preprocess_text(text):
    # remove mixed alphanumeric
    text = re.sub(r"""(?x) # verbose regex
                            \b    # Start of word
                            (?=   # Look ahead to ensure that this word contains...
                             \w*  # (after any number of alphanumeric characters)
                             \d   # ...at least one digit.
                            )     # End of lookahead
                            \w+   # Match the alphanumeric word
                            \s*   # Match any following whitespace""", 
                             "", text)
    
    # remove urls (will check and remove http and www later)
    text = re.sub(r'\s([\S]*.com[\S]*)\b', '', text)
    text = re.sub(r'\s([\S]*.org[\S]*)\b', '', text)
    text = re.sub(r'\s([\S]*.net[\S]*)\b', '', text)
    text = re.sub(r'\s([\S]*.edu[\S]*)\b', '', text)
    text = re.sub(r'\s([\S]*.gov[\S]*)\b', '', text)
    
    # remove non-alphanumeric, non-space
    text = re.sub(r'([^\s\w]|_)+', '', text)
    
    # tokenize text
    text = tokenizer.tokenize(text.lower())
    
    # remove stop words
    text = remove_stop(text, stop)
    
    # stem
    text = stem_list(text, p_stemmer)
    
    # remove instances of http or www
    new_text = []
    for word in text:
        if re.search(r'http', word):
            continue
        if re.search(r'www', word):
            continue
        new_text.append(word)
    
    return new_text

