
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
    



