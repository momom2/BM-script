def sample_text(index,text, minus=50,plus=50):
    return text[index-minus:index+plus+1]

def is_pattern(index, pattern, text, p = None):
    if p == None:
        p = len(pattern)
    for i in range(p):
        if text[index+i] != pattern[i]:
            return False
    return True
def find_index(pattern, text):
    p = len(pattern)
    n = len(text)
    index = []
    
    for i in range(n-p+1):
        
        if is_pattern(i,pattern,text,p):
            index.append(i)
    return index

def find_max(lst):
    n = len(lst)
    maxi = lst[0]
    max_i = 0
    for i in range(n):
        if lst[i]>maxi:
            maxi = lst[i]
            max_i = i
    return maxi,max_i
    
def number_around(index, text, minus=0, plus=0):
    n = len(text)
    boolean = True
    while boolean and text[index-minus].isnumeric():
        if index == minus:
            boolean = False
        else:
            minus += 1
    if boolean:
        minus -= 1
    boolean = True
    while boolean and text[index+plus].isnumeric():
        if index+plus+1 == n:
            boolean = False
        plus += 1
    return text[index-minus:index+plus]

def sentence_around(index, text, minus=0, plus=0):
    while not text[index-minus].isupper():
        minus += 1
    bool = True          #bool : faut-il continuer la recherche
    for i in range(8):
        if text[index-minus-i] ==".":
            bool = False #non, c'est le bon !
    if bool:
        #print(sample_text(index-minus,5,0))
        return sentence_around(index, text, minus+1)
        
    while text[index+plus] != ".":
        plus += 1
    #print(index-minus,index,index+plus+1)
    return text[index-minus:index+plus+1]

def word_around(index, text, minus=0, plus=0):
    n = len(text)
    boolean = True
    while boolean and text[index-minus]!=" ":
        if index == minus:
            boolean = False
        else:
            minus += 1
    if boolean:
        minus -= 1
    boolean = True
    while boolean and text[index+plus]!=" ":
        if index+plus+1 == n:
            boolean = False
        plus += 1
    return text[index-minus:index+plus]

def add(L):
     S=0
     for x in L:
         S+=x
     return S
    
def noble_name_in_noble_str_after(i, str):
    plus = 0
    bool = True
    while bool:
        title = str[i+plus:i+plus+3]
        if title == "Kni" or title == "Lor" or title == "Duk" or title == "Roy":
            bool = False
        plus += 1
    return str[i:i+plus-1]

def is_before_index(pattern, i, text):
    return pattern in text[:i]

def unindent(string,i=0):
    try:
        if string[i] == " ":
            return unindent(string,i+1)
    except IndexError:
        return string
    return string[i:]

def print_list(lst):
    for line in lst:
        print(unindent(line))

def remove_duplicates(lst):
    return list(dict.fromkeys(lst))
