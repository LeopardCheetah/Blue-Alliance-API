
import json
import requests 
from cachecontrol import CacheControl



link = 'https://www.thebluealliance.com/api/v3'

def getRequest(r):
    response = session.get(link + r)
    return json.loads(response.text)



f = open("secrets.txt", "r")
key = f.readline().strip()

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})
print()
print()


################################

event_key = '2024casf' # casf -- san fran, cafr -- fresno
lookahead_num = 3 # how many matches you want to look ahead



# gets teams from sfr that are going to a w1 comp

dump = getRequest(f'/event/{event_key}/matches/simple')

matches = [] # massive list

for match in dump:
    red_team_key = match['alliances']['red']['team_keys']
    red_teams = []

    for i in red_team_key:
        red_teams.append(int(i[3:]))
    

    blue_team_key = match['alliances']['blue']['team_keys']
    blue_teams = []

    for i in blue_team_key:
        blue_teams.append(int(i[3:]))

    # up to here i can basically parse it so that
    # it has the teams in each match in the corresponding lists
    
    if match['comp_level'] != 'qm':
        continue

    matches.append([match["match_number"], red_teams, blue_teams])

matches.sort() # now we're in order and back in business


def find_team_matches(team_num):
    # find all their matches
    ls = []

    for i in range(len(matches)):
        if team_num in matches[i][1] or team_num in matches[i][2]:
            ls.append(i+1)
    
    return ls


to_watch = [[] for _ in range(len(matches) + 1)]



# ok now let's find teams that we're against :/
our_matches = find_team_matches(840)

print(our_matches)
for match_num in our_matches:
    # find opponents
    # scrape

    # figure out which side we're on
    
    opps = []

    if 840 in matches[match_num-1][1]:
        opps = matches[match_num-1][2].copy()
    else:
        opps = matches[match_num-1][1].copy()

    # ok now find their comp matches 


    for opp in opps:
        ls = find_team_matches(opp)[::-1]
        
        for m in range(len(ls)):
            if ls[m] > match_num:
                continue
            
            if ls[m] == match_num:
                try:
                    for j in range(3):
                        if opp in to_watch[ls[m+1+j]]:
                            continue
                        to_watch[ls[m+1+j]].append(opp)
                
                except:
                    break
            
            break

for i in range(len(to_watch)):
    print(i, '\t', to_watch[i])
            

