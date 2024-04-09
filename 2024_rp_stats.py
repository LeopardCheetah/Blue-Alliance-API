import json 
import requests 
from cachecontrol import CacheControl

link = 'https://www.thebluealliance.com/api/v3'

# note that the response is always in list format
# depending on the content of the thing ur requesting, the elements in that list can either be dictionaries or strings
def getRequest(r):

    response = session.get(link + r)
    # return the text version but after json format => list of dicts if requesting teams
    return json.loads(response.text)



'''
# if importing from archiv folder
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = script_dir[:-6]


f = open(rel_path+"secrets.txt", "r")
'''


f = open("secrets.txt", "r")
key = f.readline().strip()

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})


#####################
####################
###################

# NO CHAMPS/CMPTX YET


####################

'''
print('\nEvents parsed:\n')


request1 = getRequest('/events/2024')

events = [[] for _ in range(7)]

for event_dict in request1:


    week = event_dict["week"]
    key = event_dict["key"]

    if week is None and event_dict["parent_event_key"] is not None:
        events[0].append(key)
        continue
    
    if week is None:
        continue

    week += 1

    events[week].append(key)

events[0].append('2023cmptx') # einstein field

# all events are now grouped by week
# events[0] - champs
# events[k] - regionals/district events on week k 



# NOTE: I drop events[0] here since champs isn't out and nothing is out from it
events = events[1:]




rp_data = []

# changed 7s to 6s -- see ***
for week in range(6):#***
    rp_data.append(list())
    for event in events[week]:
        ls = [0]*13
        ls[12] = event
        rp_data[week].append(ls)

# woo now theres one for each event


for week_index in range(6): #***


    for event in range(len(events[week_index])):

        # event is a string and it is the event id
        
        request = getRequest(f'/event/{events[week_index][event]}/matches')
        # request = getRequest(f'/event/2024cabe/matches')

        # this is now a massive dictionary of just every match that ever happened

        print(events[week_index][event])

        match_count = 0
        for match in request:
            # ok now we can dig into each individual
            red_rp = -1
            blue_rp = -1

            try:
                blue_rp = match["score_breakdown"]["blue"]["rp"]
            except:
                continue

            match_count += 1
            red_rp = match["score_breakdown"]["red"]["rp"]

            if red_rp + blue_rp < 2:
                ############3
                ############
                #########3##

                # for now im gonna skip this


                continue
                # gotta manually calculate the rp then
                blue_rp = 0
                red_rp = 0

                # technically u need 6 links in champs but im going to gloss over that rq
                # also im not gonna worry about the co-op grid since im lazy :/
                if len(match["score_breakdown"]["blue"]["links"]) > 4:
                    blue_rp += 1
                
                if len(match["score_breakdown"]["red"]["links"]) > 4:
                    red_rp += 1

                if match["winning_alliance"] == 'blue':
                    blue_rp += 2
                
                if match["winning_alliance"] == 'red':
                    red_rp += 2

                if match["winning_alliance"] == '':
                    red_rp += 1
                    blue_rp += 1

                if match["score_breakdown"]["red"]["totalChargeStationPoints"] > 25:
                    red_rp += 1
                
                if match["score_breakdown"]["blue"]["totalChargeStationPoints"] > 25:
                    blue_rp += 1

            # rps are now "good numbers"
            if blue_rp > red_rp:
                red_rp, blue_rp = blue_rp, red_rp
            
            # now red_rp >= blue_rp for all
            # 1-1, 2-0, 2-1, 2-2, 3-0, 3-1, 3-2, 4-0, 4-1, 4-2

            rp_total = 10*red_rp + blue_rp
            rp_list_indexing = [11, 20, 21, 22, 30, 31, 32, 33, 40, 41, 42]

            rp_data[week_index][event][rp_list_indexing.index(rp_total)] += 1    
        rp_data[week_index][event][11] = match_count
'''

# precompiled
rp_data = [[[1, 46, 3, 0, 21, 1, 0, 0, 0, 0, 0, 87, '2024bcvi'], [2, 46, 4, 0, 18, 2, 0, 0, 1, 1, 0, 89, '2024brbr'], [0, 29, 2, 0, 28, 10, 0, 0, 4, 2, 0, 90, '2024caph'], [0, 29, 3, 1, 26, 5, 0, 0, 10, 3, 0, 93, '2024casj'], [0, 25, 2, 0, 25, 6, 0, 0, 7, 1, 0, 82, '2024cthar'], [0, 37, 2, 0, 26, 5, 0, 0, 6, 2, 0, 94, '2024flwp'], [0, 34, 2, 0, 20, 2, 0, 0, 4, 2, 0, 79, '2024inmis'], [0, 27, 1, 0, 17, 6, 1, 0, 8, 2, 0, 78, '2024isde1'], [0, 22, 7, 0, 21, 5, 0, 0, 4, 1, 0, 75, '2024isde2'], [1, 7, 2, 0, 21, 11, 1, 0, 10, 5, 0, 73, '2024isde3'], [1, 47, 4, 0, 20, 1, 0, 0, 1, 0, 0, 89, '2024mibat'], [0, 38, 1, 0, 20, 4, 0, 0, 3, 2, 0, 84, '2024miber'], [0, 41, 3, 0, 22, 4, 0, 0, 9, 1, 0, 95, '2024mibkn'], [1, 37, 6, 0, 26, 7, 0, 0, 2, 1, 0, 95, '2024miket'], [1, 36, 1, 0, 32, 2, 0, 0, 4, 0, 0, 92, '2024mimil'], [2, 34, 4, 1, 25, 8, 1, 0, 5, 3, 0, 98, '2024mndu'], [1, 37, 4, 0, 29, 6, 0, 0, 3, 3, 0, 98, '2024mndu2'], [1, 49, 2, 0, 18, 2, 0, 0, 1, 1, 0, 89, '2024mxmo'], [0, 43, 0, 0, 14, 1, 0, 0, 1, 1, 0, 75, '2024ncwak'], [2, 22, 1, 0, 26, 6, 2, 0, 9, 2, 0, 85, '2024nhgrs'], [0, 41, 2, 0, 21, 2, 0, 0, 2, 0, 0, 85, '2024njfla'], [1, 38, 1, 0, 20, 0, 0, 0, 2, 0, 0, 77, '2024orore'], [1, 21, 1, 0, 34, 8, 1, 0, 3, 6, 0, 90, '2024paca'], [1, 25, 0, 0, 25, 7, 1, 0, 6, 1, 0, 81, '2024pahat'], [1, 42, 3, 1, 23, 3, 0, 0, 1, 0, 0, 89, '2024qcmo'], [1, 34, 5, 0, 13, 5, 0, 0, 3, 0, 0, 76, '2024tnkn'], [1, 55, 3, 0, 18, 2, 0, 0, 1, 0, 0, 95, '2024txkat'], [1, 42, 1, 0, 25, 4, 1, 0, 2, 2, 0, 93, '2024txwac'], [2, 43, 5, 0, 30, 4, 0, 0, 7, 1, 0, 107, '2024utwv'], [0, 37, 1, 1, 11, 3, 0, 0, 4, 1, 0, 73, '2024vaash'], [0, 30, 3, 0, 29, 4, 0, 0, 1, 0, 0, 82, '2024vabla'], [1, 32, 3, 0, 18, 10, 0, 0, 3, 1, 0, 84, '2024wasno']], [[0, 22, 2, 0, 21, 7, 0, 0, 3, 1, 0, 71, '2024arli'], [0, 22, 2, 0, 28, 10, 1, 0, 8, 1, 0, 87, '2024casf'], [1, 32, 3, 1, 22, 15, 0, 0, 4, 2, 0, 95, '2024cave'], [0, 12, 1, 0, 32, 15, 0, 0, 1, 3, 0, 80, '2024ctwat'], [1, 57, 1, 0, 12, 1, 0, 0, 0, 0, 0, 87, '2024gadal'], [0, 8, 5, 1, 17, 18, 2, 0, 7, 6, 0, 80, '2024isde4'], [1, 16, 3, 0, 29, 11, 1, 0, 5, 6, 0, 87, '2024mabri'], [0, 44, 2, 0, 20, 6, 0, 0, 4, 2, 0, 93, '2024mibel'], [1, 42, 3, 0, 26, 4, 0, 0, 2, 0, 0, 94, '2024mibro'], [0, 48, 4, 0, 20, 1, 0, 0, 2, 1, 0, 91, '2024miesc'], [0, 50, 3, 0, 18, 6, 0, 0, 2, 1, 0, 95, '2024mike2'], [0, 29, 3, 0, 40, 3, 0, 0, 3, 0, 0, 93, '2024milac'], [1, 27, 1, 1, 34, 6, 2, 0, 4, 0, 0, 91, '2024misjo'], [2, 25, 2, 0, 22, 10, 1, 0, 8, 2, 0, 87, '2024mose'], [1, 36, 2, 0, 17, 3, 0, 0, 0, 1, 0, 75, '2024ncpem'], [1, 24, 2, 0, 36, 10, 2, 0, 7, 2, 0, 99, '2024ndgf'], [4, 26, 2, 0, 18, 2, 0, 0, 2, 0, 0, 70, '2024njall'], [0, 32, 3, 0, 14, 5, 0, 0, 0, 0, 0, 69, '2024njtab'], [2, 45, 1, 0, 23, 2, 0, 0, 6, 1, 0, 95, '2024nysu'], [2, 26, 10, 0, 22, 4, 0, 0, 6, 2, 0, 87, '2024oktu'], [0, 17, 1, 0, 27, 7, 2, 0, 6, 7, 1, 83, '2024onnew'], [0, 40, 3, 0, 12, 0, 0, 0, 2, 1, 0, 73, '2024onsca'], [0, 22, 0, 0, 23, 2, 2, 0, 1, 3, 1, 69, '2024orsal'], [1, 40, 5, 0, 17, 1, 0, 0, 0, 0, 0, 79, '2024scand'], [0, 54, 1, 0, 20, 1, 0, 0, 1, 0, 0, 92, '2024tuis'], [1, 33, 2, 0, 28, 7, 0, 0, 4, 2, 0, 92, '2024tuis2'], [2, 67, 2, 0, 10, 2, 0, 0, 1, 0, 0, 99, '2024txbel'], [0, 26, 5, 1, 20, 3, 0, 0, 3, 0, 0, 74, '2024txpla'], [0, 26, 0, 0, 15, 2, 0, 0, 2, 1, 0, 61, '2024vapor'], [3, 34, 3, 0, 24, 4, 1, 0, 1, 0, 0, 86, '2024waahs']], [[0, 38, 2, 0, 28, 5, 0, 0, 4, 2, 0, 94, '2024ausc'], [0, 32, 1, 0, 23, 8, 3, 0, 8, 1, 0, 92, '2024azva'], [1, 23, 1, 0, 20, 8, 1, 0, 12, 9, 1, 91, '2024cada'], [1, 25, 4, 0, 24, 4, 0, 0, 8, 7, 1, 89, '2024cala'], [0, 40, 6, 0, 23, 2, 0, 0, 2, 1, 0, 89, '2024flta'], [0, 30, 2, 0, 25, 2, 0, 0, 1, 0, 0, 76, '2024gagwi'], [0, 13, 1, 0, 19, 16, 1, 0, 7, 11, 2, 85, '2024ilpe'], [0, 22, 3, 0, 28, 9, 0, 0, 5, 1, 0, 84, '2024incol'], [0, 22, 0, 1, 28, 10, 0, 0, 7, 4, 0, 88, '2024ksla'], [0, 20, 1, 0, 26, 10, 1, 0, 10, 3, 1, 87, '2024marea'], [2, 41, 0, 0, 24, 4, 0, 0, 1, 0, 0, 88, '2024mdsev'], [0, 9, 0, 0, 18, 12, 1, 0, 14, 4, 0, 73, '2024melew'], [2, 27, 5, 0, 29, 7, 0, 0, 5, 8, 1, 99, '2024miann'], [2, 42, 4, 0, 24, 5, 0, 0, 2, 1, 0, 95, '2024midtr'], [2, 34, 7, 1, 31, 5, 0, 0, 4, 0, 0, 99, '2024milsu'], [0, 28, 2, 0, 33, 9, 1, 0, 6, 1, 0, 95, '2024mimus'], [2, 30, 4, 0, 29, 5, 0, 0, 9, 1, 0, 96, '2024mitvc'], [0, 25, 2, 0, 33, 8, 0, 0, 4, 2, 0, 89, '2024mslr'], [1, 28, 2, 1, 14, 4, 0, 0, 4, 0, 0, 69, '2024mxpu'], [0, 33, 3, 0, 16, 3, 0, 0, 1, 0, 0, 71, '2024ncash'], [1, 9, 0, 0, 32, 12, 1, 0, 16, 1, 0, 87, '2024njski'], [0, 19, 0, 0, 31, 16, 2, 0, 6, 4, 3, 96, '2024nyro'], [0, 17, 5, 1, 22, 5, 0, 0, 3, 1, 0, 69, '2024onbar'], [1, 18, 3, 0, 26, 5, 0, 0, 1, 0, 0, 69, '2024onosh'], [0, 3, 2, 0, 28, 11, 2, 0, 9, 3, 0, 73, '2024paphi'], [0, 14, 2, 0, 30, 6, 0, 0, 4, 0, 0, 71, '2024rikin'], [0, 10, 1, 0, 34, 9, 0, 0, 4, 4, 0, 77, '2024txfor'], [0, 48, 1, 0, 25, 4, 0, 0, 4, 0, 0, 97, '2024txsan'], [4, 20, 2, 0, 21, 6, 0, 0, 5, 2, 0, 75, '2024vagle'], [2, 13, 1, 1, 25, 13, 0, 0, 9, 6, 0, 85, '2024wabon'], [1, 15, 4, 0, 18, 8, 1, 0, 5, 4, 0, 71, '2024wayak'], [1, 21, 3, 1, 42, 13, 0, 0, 6, 3, 0, 105, '2024wimi']], [[0, 22, 2, 0, 33, 13, 0, 0, 1, 4, 1, 91, '2024azgl'], [0, 7, 1, 1, 29, 17, 1, 0, 8, 12, 2, 93, '2024cafr'], [1, 15, 2, 0, 31, 10, 1, 0, 6, 9, 2, 92, '2024casd'], [0, 16, 4, 1, 31, 15, 0, 0, 9, 6, 0, 97, '2024code'], [0, 28, 3, 0, 46, 6, 1, 0, 5, 3, 0, 108, '2024flor'], [2, 46, 4, 0, 21, 2, 0, 0, 1, 0, 0, 91, '2024gacar'], [0, 15, 0, 0, 29, 15, 1, 0, 11, 9, 0, 95, '2024iacf'], [1, 18, 2, 1, 31, 11, 2, 0, 8, 4, 1, 95, '2024idbo'], [1, 9, 5, 0, 21, 10, 0, 0, 15, 9, 0, 86, '2024inpla'], [0, 10, 5, 1, 18, 10, 5, 0, 17, 12, 5, 98, '2024iscmp'], [1, 14, 0, 0, 24, 20, 2, 0, 6, 7, 2, 91, '2024mabos'], [0, 4, 1, 0, 13, 21, 3, 0, 7, 22, 1, 87, '2024mawne'], [3, 17, 2, 0, 31, 7, 1, 0, 5, 2, 0, 83, '2024mdowi'], [0, 28, 3, 0, 35, 6, 0, 0, 7, 1, 0, 95, '2024milan'], [0, 19, 3, 0, 29, 11, 0, 0, 10, 7, 1, 96, '2024miliv'], [0, 26, 0, 0, 34, 11, 0, 0, 6, 3, 0, 96, '2024mimid'], [0, 17, 1, 0, 34, 17, 1, 0, 8, 5, 1, 99, '2024mitry'], [0, 15, 1, 1, 25, 20, 2, 0, 9, 9, 2, 99, '2024miwmi'], [1, 20, 4, 0, 29, 15, 1, 0, 14, 7, 1, 107, '2024mosl'], [0, 38, 3, 1, 27, 1, 1, 0, 3, 2, 0, 91, '2024mxto'], [1, 35, 3, 0, 17, 3, 0, 0, 1, 0, 0, 76, '2024ncmec'], [2, 42, 5, 0, 11, 5, 0, 0, 4, 1, 0, 86, '2024ncwa2'], [0, 21, 6, 0, 20, 10, 0, 0, 7, 0, 0, 79, '2024njwas'], [0, 13, 1, 1, 30, 19, 3, 0, 9, 6, 0, 97, '2024nyli2'], [2, 19, 3, 0, 24, 9, 2, 0, 8, 9, 1, 93, '2024nytr'], [1, 14, 1, 0, 22, 23, 3, 0, 11, 5, 0, 95, '2024ohcl'], [1, 19, 2, 0, 23, 7, 1, 0, 4, 6, 1, 80, '2024onnob'], [1, 26, 3, 0, 16, 4, 0, 0, 5, 1, 0, 71, '2024ontor'], [1, 12, 2, 0, 18, 16, 2, 0, 4, 5, 0, 75, '2024onwat'], [0, 22, 1, 1, 25, 9, 2, 0, 6, 6, 0, 88, '2024orwil'], [1, 14, 1, 0, 22, 12, 0, 0, 9, 8, 3, 85, '2024paben'], [1, 30, 3, 0, 24, 3, 0, 0, 2, 0, 0, 78, '2024sccha'], [0, 37, 3, 0, 28, 5, 1, 0, 4, 0, 0, 93, '2024tuhc'], [0, 39, 7, 0, 27, 1, 0, 0, 5, 1, 0, 95, '2024tuis3'], [0, 26, 6, 0, 44, 7, 0, 0, 2, 0, 1, 101, '2024txdal'], [0, 28, 1, 0, 19, 8, 0, 0, 6, 0, 0, 77, '2024txhou'], [1, 21, 3, 0, 25, 7, 0, 0, 9, 2, 0, 83, '2024vafal'], [0, 3, 1, 0, 21, 25, 1, 0, 5, 11, 1, 83, '2024wasam']], [[0, 11, 4, 0, 17, 10, 0, 0, 13, 10, 1, 81, '2024camb'], [0, 17, 2, 0, 27, 7, 1, 0, 7, 11, 0, 87, '2024caoc'], [0, 22, 3, 0, 26, 1, 0, 0, 6, 0, 0, 73, '2024gaalb'], [0, 8, 2, 1, 25, 21, 5, 0, 11, 11, 0, 99, '2024ilch'], [1, 18, 2, 0, 16, 8, 1, 0, 3, 3, 0, 67, '2024ineva'], [0, 12, 3, 0, 19, 15, 4, 1, 5, 13, 0, 88, '2024mawor'], [0, 38, 6, 0, 31, 4, 0, 0, 1, 0, 0, 95, '2024midet'], [1, 14, 2, 0, 23, 18, 1, 0, 11, 7, 1, 94, '2024miken'], [1, 20, 2, 0, 30, 12, 2, 0, 8, 3, 0, 94, '2024mimcc'], [1, 24, 2, 1, 31, 9, 2, 0, 5, 5, 0, 96, '2024mimtp'], [0, 28, 2, 1, 28, 5, 1, 0, 10, 3, 0, 94, '2024mitr2'], [1, 14, 4, 0, 21, 12, 2, 0, 12, 2, 2, 85, '2024nhdur'], [0, 19, 3, 0, 26, 14, 3, 0, 8, 2, 0, 89, '2024nvlv'], [0, 14, 1, 1, 19, 11, 1, 0, 15, 6, 2, 85, '2024onham'], [0, 19, 3, 0, 22, 10, 1, 0, 5, 2, 0, 77, '2024onwin'], [1, 44, 4, 0, 21, 1, 0, 0, 3, 2, 0, 91, '2024txama'], [2, 31, 6, 1, 21, 3, 0, 0, 6, 0, 0, 85, '2024txcle']], [[1, 18, 2, 0, 36, 12, 1, 0, 8, 1, 0, 94, '2024alhu'], [0, 9, 4, 0, 20, 20, 2, 0, 12, 7, 0, 91, '2024caav'], [0, 13, 2, 0, 17, 12, 2, 0, 25, 16, 3, 105, '2024cabe'], [1, 9, 1, 1, 22, 25, 7, 0, 17, 20, 5, 123, '2024chcmp'], [0, 13, 1, 0, 37, 25, 5, 0, 9, 9, 1, 115, '2024gacmp'], [0, 24, 0, 0, 19, 5, 1, 0, 15, 4, 0, 83, '2024hiho'], [0, 4, 1, 0, 12, 19, 7, 1, 13, 17, 2, 92, '2024incmp'], [0, 17, 1, 0, 24, 14, 0, 0, 12, 6, 3, 92, '2024lake'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, '2024micmp'], [0, 1, 2, 0, 12, 18, 9, 0, 12, 21, 5, 95, '2024micmp1'], [0, 0, 3, 1, 13, 23, 9, 1, 8, 17, 5, 95, '2024micmp2'], [0, 2, 2, 0, 6, 18, 12, 0, 6, 23, 11, 95, '2024micmp3'], [0, 1, 0, 0, 7, 27, 6, 0, 8, 19, 12, 96, '2024micmp4'], [0, 30, 2, 0, 37, 9, 0, 0, 11, 4, 0, 108, '2024mnmi'], [0, 13, 0, 0, 21, 17, 3, 0, 14, 18, 4, 105, '2024mnmi2'], [0, 11, 4, 0, 26, 19, 3, 0, 12, 9, 0, 99, '2024mokc'], [0, 4, 3, 1, 16, 30, 12, 0, 18, 28, 8, 136, '2024mrcmp'], [0, 13, 5, 1, 25, 17, 2, 0, 6, 11, 0, 95, '2024nccmp'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, '2024necmp'], [0, 3, 0, 1, 7, 20, 9, 0, 10, 38, 8, 112, '2024necmp1'], [0, 1, 1, 1, 6, 19, 5, 0, 21, 27, 15, 112, '2024necmp2'], [0, 27, 3, 0, 35, 7, 0, 0, 3, 2, 0, 92, '2024nyny'], [0, 8, 3, 1, 29, 23, 6, 0, 3, 15, 4, 107, '2024ohmv'], [0, 11, 1, 0, 33, 21, 2, 0, 5, 6, 1, 96, '2024okok'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, '2024oncmp'], [0, 22, 1, 0, 21, 24, 2, 0, 14, 11, 5, 115, '2024oncmp1'], [0, 17, 3, 0, 31, 17, 4, 0, 15, 11, 2, 115, '2024oncmp2'], [0, 2, 0, 0, 11, 31, 9, 0, 10, 29, 8, 116, '2024pncmp'], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, '2024txcmp'], [0, 10, 3, 0, 18, 15, 3, 0, 11, 22, 4, 102, '2024txcmp1'], [1, 7, 1, 1, 31, 12, 1, 0, 20, 8, 4, 101, '2024txcmp2'], [0, 12, 1, 0, 37, 20, 4, 0, 5, 11, 0, 105, '2024wila']]]


# great rp_data is ready!!!
# now i need to do some data analysis with it

# remember to move ur packages

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so
# seaborn to the rescue lol

condensed_rp_data = [[0]*12 for _ in range(6)] #***
for week_ind in range(len(rp_data)):
    for event in rp_data[week_ind]:
        # this is now the 12 point list 

        for index in range(12):
            condensed_rp_data[week_ind][index] += event[index]

final_rp_data = [[] for _ in range(6)] #***

for index in range(6): #***
    final_rp_data[index] = condensed_rp_data[index][:len(condensed_rp_data[index]) - 1]



# here -- i remove the champs label
# see commented out



print()
print()
print('raw')
print()


###***** 
### only use this when rotating champs to be the last week

# final_rp_data.append(final_rp_data[0])
# final_rp_data = final_rp_data[1:]

final_rp_data = final_rp_data[::-1]

# axis = sns.heatmap(final_rp_data, cmap="crest", linewidths=0.5, annot=True, fmt='.4g', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Worlds', '     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])

axis = sns.heatmap(final_rp_data, cmap="crest", linewidths=0.5, annot=True, fmt='.4g', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])

axis.set(xlabel='Ranking Point scores', ylabel='')
plt.show()




print()
print()
print('normalized')
print()

import copy

final_rp_normal = copy.deepcopy(condensed_rp_data)

# normalization

for i in range(len(final_rp_normal)):
    for j in range(len(final_rp_normal[0])):
        final_rp_normal[i][j] = final_rp_normal[i][j]/(sum(condensed_rp_data[i]) - condensed_rp_data[i][-1]) # that last part is subtracting the total again (this is so bad)
        

    
    final_rp_normal[i] = final_rp_normal[i][:-1] # delete total match numbers


# print(final_rp_normal)

###****
# see up top 
# also change to final_rp_normal

# final_rp_data.append(final_rp_data[0])
# final_rp_data = final_rp_data[1:]
final_rp_normal = final_rp_normal[::-1]

# axis = sns.heatmap(final_rp_normal, cmap="crest", linewidths=0.5, annot=True, vmin=0, vmax=1, fmt='.2%', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Worlds', '     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])

axis = sns.heatmap(final_rp_normal, cmap="crest", linewidths=0.5, annot=True, vmin=0, vmax=1, fmt='.2%', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])

axis.set(xlabel='Ranking Point scores', ylabel='')

cbar = axis.collections[0].colorbar
cbar.set_ticks([0, 0.33, 0.66, 1])
cbar.set_ticklabels(['0%', '33%', '66%', '100%'])

plt.show()