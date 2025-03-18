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






# we in 2025 now


env_key_file = open("key.txt", "r") # todo: switch to .env packages
key = env_key_file.readline().strip()

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})

#######################



'''


event_list = getRequest('/events/2025')

w1_event_codes = []

for _event in event_list:
    # _event is a dict describing each event
    # see 2025_json_format.txt for some more information


    _event_week = _event["week"]
    _event_key = _event["key"]
    _event_type = _event["event_type_string"]


    # weeks are 0 indexes
    # week 1 events --> event_week = 0
    if (_event_type == "Regional" or _event_type == "District") and _event_week == 2:
        w1_event_codes.append(_event_key)
    
    # finish adding all w1 event codes on here



# start getting rp data
w1_rp_data = [0]*21 # 21st index for total matches
total_match_count = 0

for _event_key in w1_event_codes:

    # _event_key is a string and it is the event id (e.g. caoc)
    
    _event_match_info = getRequest(f'/event/{_event_key}/matches')
    # request = getRequest(f'/event/2024cabe/matches')

    # this is now a massive dictionary of just every match that ever happened

    _match_count = 0


    for _match in _event_match_info:
        # ok now we can dig into each individual match

        red_rp = -1
        blue_rp = -1


        if _match["comp_level"] != 'qm':
            continue # filter out all the non-qualifcation matches

        try:
            blue_rp = _match["score_breakdown"]["blue"]["rp"]
            red_rp = _match["score_breakdown"]["red"]["rp"]
        except:
            print('aaahh')
            print()
            print(_match, _event_match_info)
            continue

        _match_count += 1

        ######

        # rps are now "good numbers"
        if blue_rp > red_rp:
            red_rp, blue_rp = blue_rp, red_rp
        
        # now red_rp >= blue_rp for all
        #  x   x    x   3-0, 4-0, 5-0, 6-0
        #  x  1-1, 2-1, 3-1, 4-1, 5-1, 6-1
        #  x   x   2-2, 3-2, 4-2, 5-2, 6-2
        #  x   x    x   3-3, 4-3, 5-3, 6-3
        #  x   x    x    x   4-4,  x    x  --- 4-4 is when both get auto/coral/barge rp but tie (1 + 3 / 1 + 3)



        # todo: go from here
        rp_total = 10*red_rp + blue_rp
        rp_list_indexing = [11, 21, 22, 30, 31, 32, 33, 40, 41, 42, 43, 44, 50, 51, 52, 53, 60, 61, 62, 63]



        if rp_total == 63:
            print(_match["key"], '63')
        if rp_total == 43:
            print(_match["key"], '43')
        
        if rp_total == 22:
            print(_match["key"], '22')
        if rp_total == 33:
            print(_match["key"], '33')
        if rp_total == 44:
            print(_match["key"], '44')


        w1_rp_data[rp_list_indexing.index(rp_total)] += 1    

    total_match_count += _match_count

    # print(_event_key, w1_rp_data) -- to get a week by week update

w1_rp_data[20] = total_match_count

print()
print(w1_rp_data)
quit()




'''



################### start heatmap collection




w1_rp_data = [5, 5, 1, 214, 109, 24, 0, 386, 269, 68, 0, 0, 250, 271, 95, 1, 42, 41, 15, 2] # remove the total match count statistic
w2_rp_data = [4, 0, 1, 336, 159, 17, 1, 486, 303, 79, 1, 0, 296, 243, 67, 5, 44, 58, 27, 3]
w3_rp_data = [5, 11, 7, 262, 163, 35, 1, 484, 354, 119, 1, 0, 356, 388, 184, 12, 104, 117, 58, 12]

total_rp_data = list()
total_rp_data.append(w1_rp_data)
total_rp_data.append(w2_rp_data)
total_rp_data.append(w3_rp_data)


# add leading zeroes
for _ in range(7 - len(total_rp_data)):
    total_rp_data.append([0]*20)

total_rp_data = total_rp_data[::-1]

# great rp_data is ready!!!
# now i need to do some data analysis with it


import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so
# seaborn

total_rp_data_grid = sns.heatmap(total_rp_data, cmap = "crest", linewidths=0.5, annot=True, fmt='.4g', xticklabels=['1-1', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2', '4-3', '4-4', '5-0', '5-1', '5-2', '5-3', '6-0', '6-1', '6-2', '6-3'], yticklabels=["Champs", "Week 6", "Week 5", "Week 4", "Week 3", "Week 2", "Week 1"])


total_rp_data_grid.set(xlabel='Qual RP Scores', ylabel='')
plt.show()



# get normalized rp
normalized_total_rp_data = list()

for _i in range(7):
    # 7 weeks
    normalized_total_rp_data.append([0]*20)
    if sum(total_rp_data[_i]) == 0:
        # there's literally nothing in the list
        continue
    
    for _j in range(20):
        # length 20 list
        normalized_total_rp_data[_i][_j] = 100*round(total_rp_data[_i][_j]/sum(total_rp_data[_i]), 4)
        # turn into percentages
        # rounding normalizes data



normalized_rp_data_grid = sns.heatmap(normalized_total_rp_data, vmin = 0, vmax = 25, cmap = "crest", linewidths=0.5, annot=True, fmt='.4g', xticklabels=['1-1', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2', '4-3', '4-4', '5-0', '5-1', '5-2', '5-3', '6-0', '6-1', '6-2', '6-3'], yticklabels=["Champs", "Week 6", "Week 5", "Week 4", "Week 3", "Week 2", "Week 1"])


normalized_rp_data_grid.set(xlabel='Normalized Qual RP Scores', ylabel='')
plt.show()