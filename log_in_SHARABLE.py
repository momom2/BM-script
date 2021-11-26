#in a terminal :
# pip install mechanicalsoup
# pip install nums_from_string
import mechanicalsoup

def choose_character(login_page):
    list_tags = login_page.select("[class~=charName]")

    list_names = [tag.string for tag in list_tags]

    print("Choose one of the following characters:")
    for i in range(len(list_names)):
        print(i+1,"-",list_names[i])
    return int(input())-1

def logged_in_browser(e_mail_address,password):
    
    
    browser = mechanicalsoup.StatefulBrowser()


    ### Connecting to your account. ###
    browser.open("https://battlemaster.org/account")
    
    form = browser.select_form() #login form
    #form.print_summary #confirmation that it's the correct form


    form["username"] = e_mail_address   #My e-mail address.
    form["password"] = password         #My password.


    form.set("_remember_me", False)
    form.choose_submit(None)
    browser.submit_selected()

    #browser.launch_browser()
    character_chosen = choose_character(browser.page)
    form = browser.select_form(nr = character_chosen) #play form
    #form.print_summary() #confirmation that it's the correct form
    form.set("play", True)
    form.choose_submit(None)
    browser.submit_selected()
    ### Connected to your account
    return browser
