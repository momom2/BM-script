#in a terminal :
# pip install mechanicalsoup
# pip install nums_from_string



def web_report(e_mail_address,password,browser):
    import mechanicalsoup
    import nums_from_string


    browser.open("https://battlemaster.org/war/play-scribe.php")

    list_temp = browser.links()
    list_reports = [tag for tag in list_temp if "Battle" in tag.contents[0]][1:]

    def extract_names(list_links):
        list_names = []
        for link in list_links:
            list_names.append(link.get_text())
        return list_names

    def extract_battles_i(list_report_names): #i is the position of the report
        battles_i = []                        #in list_reports
        for i in range(len(list_report_names)):
            if list_report_names[i][:6] == "Battle":
                battles_i.append(i)
        return battles_i
    
    def extract_battles(list_reports):
        #urls = extract_urls(list_reports)
        reports_name = extract_names(list_reports)
        battles_i = extract_battles_i(extract_names(list_reports))
        battles = [(reports_name[i],i) for i in battles_i]
        return battles
    

    ### Useless ###
    def extract_urls(list_links):
        list_urls = []
        for link in list_links:
            list_urls.append(link.get("href"))
        return list_urls

    def find_id(report_url):
        return report_url[31:]

    def extract_id(list_reports):
        return list(map(int, list(map(find_id, extract_url(list_reports)))))

    def extract_battle_text(list_spans):
        list_battle_texts = []
        for span in list_spans:
            list_battle_texts.append(span.get_text())
        return list_battle_texts
    
    ### End_Useless ###
    
    
    def choose_battle(battles):
        print("Battles available (by age):\n")
        for battle in battles:
            print(battle[0])
        for i in range (len(battles)):
            print("\nChoose this battle ?", battles[i][0])
            string = input("y/n\n")
            if string == "y" or string == "yes":
                return battles[i][1]
        #No battle chosen.
            
     
    try:
        link = list_reports[choose_battle(extract_battles(list_reports))]
        browser.follow_link(link)
    except TypeError:
        print ("No battle chosen.")
        exit(0)


    #list_spans = page.find_all("span")
    
    return browser.page.get_text()

def local_report():
    path = input("Path of the file: ")
    from bs4 import BeautifulSoup
    return BeautifulSoup(open(path).read(),features = "lxml").get_text()
