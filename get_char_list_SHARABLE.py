#in a terminal :
# pip install mechanicalsoup
# pip install nums_from_string
import mechanicalsoup
import nums_from_string
from text_treatment_functions import *

def char_list(e_mail_address,password,browser):

    
    browser.open("https://battlemaster.org/war/charlist.php")
    
    text = browser.page.get_text()

    text_list = text.splitlines()
    
    def index_first_name(text_list):
        i = 0
        while text_list[i] != "Status":
            i += 1
        return i+5

    def names_last_names_realm(text_list):
        list_names_last_names_realm = []
        i = index_first_name(text_list)
        try:
            while True:
                while text_list[i+5] == "noble":
                    list_names_last_names_realm.append((text_list[i],text_list[i+1],text_list[i+2]))
                    i += 8
                i += 1
        except IndexError:
            pass
        return list_names_last_names_realm
    return names_last_names_realm(text_list)


### Usable in https://battlemaster.org/war/leaderlist.php ###
    def extract_index_nobles_names(line):
        def add_two(n):
            return n+2
        index_list = list(map(add_two, find_index("  ",line)))
        return index_list

    index_list = extract_index_nobles_names(line)
    def extract_noble_list(line):
        index_list = extract_index_nobles_names(line)
        noble_list = [noble_name_in_noble_str_after(i, line) for i in index_list]
        return noble_list
    return extract_noble_list(line)
