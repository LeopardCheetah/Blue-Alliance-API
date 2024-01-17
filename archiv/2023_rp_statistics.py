import json 
import requests 
from cachecontrol import CacheControl

link = 'https://www.thebluealliance.com/api/v3'
print('\nEvents parsed:\n')



# note that the response is always in list format
# depending on the content of the thing ur requesting, the elements in that list can either be dictionaries or strings
def getRequest(r):

    response = session.get(link + r)
    # return the text version but after json format => list of dicts if requesting teams
    return json.loads(response.text)



session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': 'archived :/'})





'''
goal:
> figure out how many 4-2 (rp wise) matches there were - then break them down by each event/each week 

> hiearchy:

[year (game)]
[week]
[event]
[match]


todos:
- get all events
- sort them in order of weeks
- get there matches and filter out the non 4-2 rp matches (or we could see the trend of winning/losing matches over time and stuff)
'''


request1 = getRequest('/events/2023')

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



rp_data = []


for week in range(7):
    rp_data.append(list())
    for event in events[week]:
        ls = [0]*13
        ls[12] = event
        rp_data[week].append(ls)

# woo now theres one for each event


for week_index in range(7):


    for event in range(len(events[week_index])):
        # event is a string and it is the event id
        
        request = getRequest(f'/event/{events[week_index][event]}/matches')
        
        
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
    



# great rp_data is ready!!!
# now i need to do some data analysis with it

import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so
# seaborn to the rescue lol

condensed_rp_data = [[0]*12 for _ in range(7)]
for week_ind in range(len(rp_data)):
    for event in rp_data[week_ind]:
        # this is now the 12 point list 

        for index in range(12):
            condensed_rp_data[week_ind][index] += event[index]

final_rp_data = [[] for _ in range(7)]

for index in range(7):
    final_rp_data[index] = condensed_rp_data[index][:len(condensed_rp_data[index]) - 1]



user_in = input('\nWould you like the data to be normalized or raw?\n>> ')

if user_in.strip() == 'raw':
    final_rp_data.append(final_rp_data[0])
    final_rp_data = final_rp_data[1:]
    final_rp_data = final_rp_data[::-1]
    axis = sns.heatmap(final_rp_data, cmap="crest", linewidths=0.5, annot=True, fmt='.3g', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Worlds', '     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])
    axis.set(xlabel='Ranking Point scores', ylabel='')
    plt.show()
else:
    # normalization
    for i in range(len(final_rp_data)):
        for j in range(len(final_rp_data[0])):
            final_rp_data[i][j] /= condensed_rp_data[i][11]
        
    final_rp_data.append(final_rp_data[0])
    final_rp_data = final_rp_data[1:]
    final_rp_data = final_rp_data[::-1]

    axis = sns.heatmap(final_rp_data, cmap="crest", linewidths=0.5, annot=True, vmin=0, vmax=1, fmt='.2%', xticklabels=['1-1', '2-0', '2-1', '2-2', '3-0', '3-1', '3-2', '3-3', '4-0', '4-1', '4-2'], yticklabels=['     Worlds', '     Week 6', '     Week 5', '     Week 4', '     Week 3', '     Week 2', '     Week 1'])
    axis.set(xlabel='Ranking Point scores', ylabel='')
    
    cbar = axis.collections[0].colorbar
    cbar.set_ticks([0, .25, .5, .75, 1])
    cbar.set_ticklabels(['0%', '25%', '50%', '75%', '100%'])
    
    plt.show()