
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


################################33



# gets teams from sfr that are going to a w1 comp

dump = getRequest('/event/2024casf/teams/simple')
print(dump, type(dump))
ls = []
for team_dict in dump:
    print(team_dict, type(team_dict))
    team_num = team_dict['team_number']
    more_events = getRequest(f'/team/frc{team_num}/events/2024')
    # dict list
    m = 1
    for event in more_events:
        m = min(m, int(event['week']))
    if m < 1:
        ls.append(team_num)
print(ls) 



'''

dump = getRequest('/event/2024cafr/teams/simple')

ls = []
for team_dict in dump:
    team_num = team_dict['team_number']

    more_events = getRequest(f'/team/frc{team_num}/events/2024')


    m = 3
    for event in more_events:
        # worlds is null
        name = []
        try:
            if int(event['week']) < 3:
                m = min(m, int(event['week']))
                name.append(event['name'])
        except:
            pass

    if m < 3:
        ls.append((team_num, name))

ls.sort()
print(ls) 
'''