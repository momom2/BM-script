#in a terminal :
# pip install mechanicalsoup
# pip install nums_from_string
import mechanicalsoup
import nums_from_string
#import re
import get_report_SHARABLE
import get_char_list_SHARABLE
import log_in_SHARABLE
from text_treatment_functions import *


unit_types = ["Cav","Inf","Arch","MI","SF"]
unit_formations = ["box","skirmish","line","wedge"]
unit_deployments = ["Rear","Back","Middle","Front"] #no way to know that for now.




e_mail_address = input("Your e-mail adress: ")
password = input("Your BM password (promise I won't do bad things with it): ")
logged_in_browser = log_in_SHARABLE.logged_in_browser(e_mail_address,password)
if int(input("Which one do you want:\n\n1 - Web\n2 - Local\n")) == 1:
    text_report = get_report_SHARABLE.web_report(e_mail_address,password,logged_in_browser)
else:
    text_report = get_report_SHARABLE.local_report()
char_list = get_char_list_SHARABLE.char_list(e_mail_address,password,logged_in_browser)

#def main():
#    e_mail_address = input("Your e-mail address: ")
#    password = input("Your password: ")
#    global text_report
#    text_report = Take_dat_report_SHARABLE.text_report(e_mail_address,password)
#    global char_list
#    char_list = Take_dat_char_list_SHARABLE.char_list(e_mail_address,password)

#if __name__ == "__main__":
#    main()



nb_realms_present = int(input("Number of realms present at the battle:\n"))

print("Names of the realms:")
realms_present = [input(str(i+1)+" - ") for i in range(nb_realms_present)]
peoples_present = [realm+"ian" for realm in realms_present[:nb_realms_present]]





### Functions that use a global variable. ###
def which_leader(unit):
    for other_unit,leader in list_units_leaders:
        if other_unit == unit:
            return leader
def which_unit(leader):
    for unit,other_leader in list_units_leaders:
        if other_leader == leader:
            return unit
def which_realm(unit):
    return basic_data(unit)[1]

        
### Generally useful functions. ###
        
def sample_text_report(index,minus=50,plus=50):
    return sample_text(index, text_report, minus, plus)

def compartmentalize_text_report():
    index = find_index("Turn", text_report)
    index.append(find_index(" Victory!",text_report)[0]-8)
    len_index = len(index)
    #print(index)
    global number_of_turns
    number_of_turns = len_index-1
    return [text_report[:index[0]]]+[text_report[index[i]:index[i+1]] for i in range(len_index-1)]+[text_report[index[-1]:]]

compartmentalized = compartmentalize_text_report()
introduction = compartmentalized[0]
conclusion = compartmentalized[-1]
def lines(text):
    lines_text1 = text.splitlines()
    lines_text2 = []
    for line in lines_text1:
        index = find_index(".",line)
        for i in index:
            lit_str = line[i-2:i]
            if i < len(line)-2 and lit_str != "No" and lit_str != "vs":
                lines_text2.append(unindent(line[:i+1]))
                lines_text2.append(unindent(line[i+1:]))
            else: lines_text2.append(unindent(line))
        if index == []:
            lines_text2.append(unindent(line))
    return lines_text2

lines_introduction = lines(introduction)
lines_text = lines(text_report)

def extract_name(line):
    first_letter = 0
    intro_letter_found = False
    first_letter_found = False
    while not intro_letter_found:
        first_letter += 1
        if line[first_letter].isalpha():
            intro_letter_found = True
        
    while not first_letter_found:
        first_letter += 1
        if line[first_letter].isalpha():
            first_letter_found = True
    
    last_letter = 0
    i = -1
    
    while not (any([(realm in line[i:]) for realm in realms_present])) and i != -len(line):
        i += -1
    if i != -len(line):
        last_letter = i
    
    return line[first_letter:last_letter]

def participants_unitsleaders():
    i = 60
    lines_part = []
    while lines_introduction[i+1][0:5] != "Total":
        lines_part.append(lines_introduction[i])
        i += 1
    list_unitsleaders = [extract_name(line) for line in lines_part]
    return list_unitsleaders
list_unitsleaders = participants_unitsleaders()

nb_militia_units = 0
def extract_unit_leader(unitleader):
    global nb_militia_units
    separation = 0
    for (leader,_,_) in char_list:
        #print(leader)
        i = -1
        while unitleader[i:] != leader and i != -len(leader)-1:
            i += -1
        #print(i, len(leader))
        if i != -len(leader)-1:
            separation = i
            #print(separation)
    if separation == 0:
        index = find_index("(militia/guard unit)",unitleader)
        if index != []:
            nb_militia_units += 1
            return (unitleader[:index[0]],unitleader[index[0]:]+str(nb_militia_units))
        else:
            print("You have been chosen for a random recaptcha. Please separate the following string into the names of a unit and a character:",unitleader)
            print("(Just this once, you can copy/paste, and are in fact encouraged to do so.)")
            print("""(If there is no character name, type a *UNIQUE* name that is not "Unknown" that will be used to designate the leader of this unit.)""")
            unit = input("Unit: ")
            character = input("Character: ")
            return (unit,character)
    return (unitleader[:separation],unitleader[separation:])

list_units_leaders = [extract_unit_leader(unitleader) for unitleader in list_unitsleaders]
nb_units = len(list_units_leaders)

    
### More specific functions. ###


def weather_report():
    print(sentence_around(find_index("wind", introduction)[0],introduction))

def all_about(unit,turn = -1):
    if turn == -1:
        return [line for line in lines_text if unit in line]
    else:
        return [line for line in lines(compartmentalized[turn]) if unit in line]

def text_all_about(unit,turn = -1):
    return add(all_about(unit,turn))


    
def basic_data(unit):
    line_about = all_about(unit)[0]
    
    i = find_index(unit, line_about)[0] #i nous repère dans la ligne
    i += len(unit)
    leader = which_leader(unit)
    i += len(leader)
    try:
        i-=len(number_around(20,leader))
    except IndexError:
        pass
    
    def which_realm_aux(line_truncated): #truncated before i
        for realm in realms_present:
            if is_pattern(0,realm,line_truncated):
                return realm    
    realm = which_realm_aux(line_about[i:])
    i += len(realm)
    size = number_around(i,line_about)
    i += len(size)
    
    line_truncated = line_about[i:]
    unit_type = ""
    for potential_unit_type in unit_types:
        if potential_unit_type in line_truncated:
            unit_type = potential_unit_type
    i += len(unit_type)
    formation = ""
    for potential_unit_formation in unit_formations:
        if potential_unit_formation in line_truncated:
            formation = potential_unit_formation
    i+= len(formation)
    CS = number_around(i+3,line_about)
    return(leader, realm, size, unit_type, formation, CS)

def disp_basic_data(unit):
    (leader, realm, size, unit_type, formation, CS) = basic_data(unit)
    print("Name:",unit,"\nLeader:",leader,"\nRealm:",realm,"\nType:",unit_type,"\nFormation:",formation,"\nSize:",size,"\nCS:",CS)
     
def hits(unit,turn = -1):
    unit_report = all_about(unit,turn)
    hits_scored = 0
    hits_taken = 0
    for event in unit_report:
        index = [i+6 for i in find_index("score",event)]
        for i in index:
            if is_before_index(unit, i, event):
                hits_scored += int(number_around(i, event))
            else:
                hits_taken += int(number_around(i, event))
    
        index = [i+8 for i in find_index("scoring",event)]
        for i in index:
            if unit in event[:len(unit)+2]:
                hits_scored += int(number_around(i, event))
            else:
                hits_taken += int(number_around(i, event))
    return hits_scored,hits_taken

def disp_hits(unit):
    hits_scored,hits_taken = hits(unit)
    print("Hits scored:",hits_scored,"\nHits_taken:",hits_taken)

def casualties(unit,turn = -1):
    unit_report = all_about(unit,turn)
    own_casualties = 0
    for event in unit_report:
        index = [i+12 for i in find_index("which cause",event)]
        for i in index:
            own_casualties += int(number_around(i,event))
    return own_casualties

def create_graph(turn):
    turn_lines = lines(compartmentalized[turn])
    graph = [[0,"",[],[]] for _ in range(nb_units)]
    #(tirs à distances, cible à distance, dégâts au corps-à-corps, cibles au corps-à-corps) pour cette unité
    for i in range(nb_units):
        unit = list_units_leaders[i][0]
        len_u = len(unit)
        for line in turn_lines:
            
            if line[:len_u] == unit:
                if "scoring" in line:
                    graph[i][0] = int(number_around(find_index("scoring", line)[0]+8, line))
                    for unit_attacked,_ in list_units_leaders:
                        if unit_attacked in line[len_u:]:
                            graph[i][1] = unit_attacked
                elif "score" in line:
                    graph[i][2].append(int(number_around(find_index("score", line)[0]+6, line)))
                    for unit_attacked,_ in list_units_leaders:
                        if unit_attacked in line[len_u:]:
                            graph[i][3].append(unit_attacked)
                        
    return graph

def casualties_caused_by(unit,turn = -1):
    i_unit = [i for i in range(nb_units) if list_units_leaders[i][0] == unit][0]
    
    if turn != -1:
        graph = create_graph(turn)
        graph_unit = graph[i_unit]
        unit_attacked_r = graph_unit[1]
        if unit_attacked_r != "":
            casualties_r = casualties(unit_attacked_r,turn)*(graph_unit[0]/hits(unit_attacked_r,turn)[1])
        else:
            casualties_r = 0
        casualties_cc = []
        for i in range(len(graph_unit[2])):
            unit_attacked_cc = graph_unit[3][i]
            #print(unit_attacked_cc,"attacked by",unit)
            casualties_cc.append(casualties(unit_attacked_cc,turn)*(graph_unit[2][i]/hits(unit_attacked_cc,turn)[1]))
        return casualties_r+sum(casualties_cc)
    else:
        return sum([casualties_caused_by(unit,i) for i in range(1,number_of_turns)])

def bragging_rights():
    
    list_casualties = [casualties_caused_by(unit) for unit,_ in list_units_leaders]
    max_cas,max_cas_i = find_max(list_casualties)
    print("Caused most casualties: (",round(max_cas,2),")",sep="")
    unit,leader = list_units_leaders[max_cas_i]
    print(unit,"led by",leader)

    list_hits_dealt = [hits(unit)[0] for unit,_ in list_units_leaders]
    max_hits_d,max_hits_d_i = find_max(list_hits_dealt)
    print("\nDealt most damage: (",max_hits_d," hits)",sep="")
    unit,leader = list_units_leaders[max_hits_d_i]
    print(unit,"led by",leader)

    list_hits_received_per_soldier = [hits(unit)[1]/(int(basic_data(unit)[2])) for unit,_ in list_units_leaders if int(basic_data(unit)[2])!=0]
    max_hits_r_per_s,max_hits_r_per_s_i = find_max(list_hits_received_per_soldier)
    print("\nBest meatshield: (",round(max_hits_r_per_s,2)," hits absorbed per soldier)",sep="")
    unit,leader = list_units_leaders[max_hits_r_per_s_i]
    print(unit,"led by",leader)

    list_max_hits_turn = [find_max([hits(unit,turn)[0] for unit,_ in list_units_leaders]) for turn in range(1,number_of_turns+1)]
    (max_hits,max_hits_i),turn = find_max(list_max_hits_turn) 
    print("\nMost damage in one turn: (",max_hits," hits at turn ",turn,")",sep="")
    unit,leader = list_units_leaders[max_hits_i]
    print(unit,"led by", leader)
    

def who_scattered():
    index = find_index("wiping",text_report)#+find_index("panicked flight", text_report)
    list_sentence = [sentence_around(i,text_report) for i in index]
    list_scattered = []
    for sentence in list_sentence:
        for unit in [units_leaders[0] for units_leaders in list_units_leaders]:
            if unit in sentence:
                list_scattered.append(unit)
    return list_scattered

def disp_scattered():
    print("\n\nScattered:")
    list_scattered = who_scattered()
    len_r = len(realms_present)
    scat_r = [[] for i in range(len_r)]
    #print(scat_r)
    for u_scattered in list_scattered:
        l = which_leader(u_scattered)
        r = which_realm(u_scattered)
        for i in range (len_r):
            if r == realms_present[i]:
                scat_r[i].append((u_scattered,l))
    for i in range (len_r):
        nb_scattered_r = len(scat_r[i])
        if nb_scattered_r > 0:
            print("\n\nFor ", realms_present[i], " (",nb_scattered_r,") ",":\n",sep = '')
            for u,l in scat_r[i]:
                print(u, "led by", l)
        else:
            print("\nNo",peoples_present[i],"unit scattered.")


def who_retreated():
    index = find_index("retreat",text_report)
    list_sentence = [sentence_around(i,text_report) for i in index]
    list_retreated = []
    for sentence in list_sentence:
        for unit in [units_leaders[0] for units_leaders in list_units_leaders]:
            if unit in sentence:
                list_retreated.append(unit)
    return list_retreated

def disp_retreated():
    print("\n\nRetreated:")
    list_retreated = who_retreated()
    len_r = len(realms_present)
    retr_r = [[] for i in range(len_r)]
    #print(scat_r)
    for u_retreated in list_retreated:
        l = which_leader(u_retreated)
        r = which_realm(u_retreated)
        for i in range (len_r):
            if r == realms_present[i]:
                retr_r[i].append((u_retreated,l))
    for i in range (len_r):
        nb_retreated_r = len(retr_r[i])
        if nb_retreated_r > 0:
            print("\n\nFor ", realms_present[i], " (",len(retr_r[i]),") ",":\n",sep = '')
            for u,l in retr_r[i]:
                print(u, "led by", l)
        else:
            print("\nNo",peoples_present[i],"unit retreated.")

def wounded():
    lines_wounded = remove_duplicates([line for line in lines_text if "wounded" in line or "killed" in line])
    list_normal_wounded = []
    list_serious_wounded = []
    list_dead = []
    for line in lines_wounded:
        for _,char in list_units_leaders:
            if char in line:
                #Add the last name
                if "seriously" in line:
                    list_serious_wounded.append(char)
                if "killed" in line:
                    list_dead.append(char)
                else:
                    list_normal_wounded.append(char)
    list_normal_wounded = remove_duplicates(list_normal_wounded)
    list_serious_wounded = remove_duplicates(list_serious_wounded)
    list_dead = remove_duplicates(list_dead)

    for n_wounded in list_normal_wounded:
        if n_wounded in list_serious_wounded or n_wounded in list_dead:
            list_normal_wounded.remove(n_wounded)
    for s_wounded in list_serious_wounded:
        if s_wounded in list_dead:
            list_serious_wounded.remove(s_wounded)
    return list_normal_wounded,list_serious_wounded,list_dead

def disp_wounded(realm = None):
    list_normal_wounded,list_serious_wounded,list_dead = wounded()
    lst_n_w,lst_s_w,lst_d = [],[],[]
    
    if realm != None:
        list_char = [(char,which_realm(which_unit(char))) for _,char in list_units_leaders]
        for n_wounded in list_normal_wounded:
            for char,r in list_char:
                if char == n_wounded and r == realm:
                    lst_n_w.append(char)
        for s_wounded in list_serious_wounded:
            for char,r in list_char:
                if char == s_wounded and r == realm:
                    lst_s_w.append(char)
        for dead in list_dead:
            for char,r in list_char:
                if char == dead and r == realm:
                    lst_d.remove(char)
    else:
        lst_n_w,lst_s_w,lst_d = list_normal_wounded,list_serious_wounded,list_dead
    len_n,len_s,len_d = len(lst_n_w),len(lst_s_w),len(lst_d)

    if len_n > 1:
        print("\nHave been wounded: (",len_n,")",sep = "")
        print_list(lst_n_w)
    elif len_n == 1:
        print("\nHas been wounded:")
        print(lst_n_w[0])

    if len_s > 1:
        print("\nHave been seriously wounded: (",len_s,")",sep = "")
        print_list(lst_s_w)
    elif len_s == 1:
        print("\nHas been seriously wounded:")
        print(lst_s_w[0])
    
    if len_d > 1:
        print("\nHave been killed: (",len_d,")",sep = "")
        print_list(lst_d)
    elif len_d == 1:
        print("\nHas been killed:")
        print(lst_d[0])
    if len_n+len_s+len_d == 0:
        print("\nNo one was wounded.")

def disp_total_hits():
    index = find_index("Total hits suffered",text_report)
    #print(index)
    text_list = [text_report[i+32:i+135] for i in index] #values found via trial and error
    #print(text_list)                                    #using print(text_list)
    number_list_list = []
    for sentence in text_list:
       number_list_list.append(nums_from_string.get_nums(sentence))

    #print (number_list_list)
    list_att = [number_list[0] for number_list in number_list_list]
    list_def = [number_list[3] for number_list in number_list_list]
    list_att_r = [number_list[2] for number_list in number_list_list]
    list_def_r = [number_list[5] for number_list in number_list_list]
    list_att_cc = [number_list[1] for number_list in number_list_list]
    list_def_cc = [number_list[4] for number_list in number_list_list]
    
    att = add(list_att)
    defe = add(list_def)
    att_r = add(list_att_r)
    def_r = add(list_def_r)
    att_cc = add(list_att_cc)
    def_cc = add(list_def_cc)

    if defe != 0:
        ratio_total = round(att/defe,2)
    else:
        ratio_total = "(No ratio)"
    if def_r != 0:
        ratio_r = round(att_r/def_r,2)
    else:
        ratio_r = "(No ratio)"
    if def_cc != 0:
        ratio_cc = round(att_cc/def_cc,2)
    else:
        ratio_cc = "(No ratio)"

    
    print("\nTotal hits suffered:", "\nAttackers:", att,"(",att_cc,"from close combat and", att_r,"from ranged)"
          "\nDefenders:", defe, "(", def_cc, "from close combat and", def_r, "from ranged)")
    print("\nRatio Att/Def:", "\nTotal:", ratio_total,
          "\n\nRanged:", ratio_r,
          " -- Close Combat:", ratio_cc)


def disp_total_casualties():
    index = find_index("Total casualties", text_report)
    text_list = [text_report[i:i+50] for i in index] #values found via trial and error
    #print(text_list)                                #using print(text_list)
    number_list_list = []
    for sentence in text_list:
        number_list_list.append(nums_from_string.get_nums(sentence))
    list_att = [number_list[0] for number_list in number_list_list]
    list_def = [number_list[1] for number_list in number_list_list]
    att = add(list_att)
    defe = add(list_def)
    ratio_total = round(att/defe,2)
    print("\nTotal casualties:", "\nAttackers :", att,
          "\nDefenders:", defe)
    print("\nRatio Att/Def:", "\nTotal :", ratio_total)

def who():
    return [[(unit,leader) for unit,leader in list_units_leaders if which_realm(unit) == realm] for realm in realms_present]
    
def disp_who():
    everyone = who()
    for i in range(len(realms_present)-1):
        if everyone[i] != []:
            print("\nFor ",realms_present[i],":\n",sep = '')
            for unit,leader in everyone[i]:
                print(unit,"led by",leader)
    if everyone[-1] != []:
        print("\nUnknown allegiance:\n")
        for unit,leader in everyone[-1]:
                print(unit,"led by",leader)

def start():
    print("\nNon_exhaustive list of available functions and variables:")
    print("\ntext_report","weather_report()","number_of_turns","disp_who()","disp_total_hits()","disp_total_casualties()","disp_scattered()","disp_retreated()","bragging_rights()",sep = "\n")
    print("\ndisp_wounded(realm = None)")
    print("\ndisp_hits(unit)")
    print("disp_basic_data(unit)")
    print("\nUnless specified otherwise, arguments for these functions are strings.")
    print("You can also use other functions, though they are more complicated and less instructive.")

### What the script can do so far : ###

# Global: #

#weather_report()
#disp_who()
#disp_total_hits()
#disp_total_casualties()
#disp_scattered()
#disp_retreated()

# Optional argument: #

#disp_wounded(realm = None)

# For a given unit: #

#disp_hits(unit)
#disp_basic_data(unit)

start()

#arch_hits_dealt,arch_hits_received,arch_cas,arch_nb,arch_CS = 0,0,0,0,0
#SF_hits_dealt,SF_hits_received,SF_cas,SF_nb,SF_CS = 0,0,0,0,0
#for unit,_ in list_units_leaders:
#    l,r,size_str,typ,formation,CS_str = basic_data(unit)
#    size = int(size_str)
#    CS = int(CS_str)
#    if typ == "Arch":
#        arch_hits_dealt += hits(unit)[0]
#        arch_hits_received += hits(unit)[1]
#        arch_nb += size
#        arch_CS += CS
#        arch_cas += casualties_caused_by(unit)
#    elif typ == "SF":
#        SF_hits_dealt += hits(unit)[0]
#        SF_hits_received += hits(unit)[1]
#        SF_nb += size
#        SF_CS += CS
#        SF_cas += casualties_caused_by(unit)
#
#arch_CS_per_s,SF_CS_per_s = arch_CS/arch_nb,SF_CS/SF_nb
#arch_hits_per_CS,SF_hits_per_CS = arch_hits_dealt/arch_CS,SF_hits_dealt/SF_CS
