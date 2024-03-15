
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


'''
# gets teams from sfr that are going to a w1 comp

dump = getRequest('/event/2024casf/teams/simple')

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
# gets teams from sfr that are going to a w1 comp

dump = getRequest('/event/2024cafr/teams/simple')

ls = []
event_name = []
for team_dict in dump:
    team_num = team_dict['team_number']
    more_events = getRequest(f'/team/frc{team_num}/events/2024')
    # dict list
    m = 4


    names = []

    for event in more_events:
        if event['event_code'] == 'cmptx':
            continue
        m = min(m, int(event['week']))
        names.append((int(event['week']), event['short_name']))

    names.sort()

    for n in names:
        if n[0] < 3:
            ls.append(team_num)
            event_name.append(n[1]) 


# formatting
print()
for i in range(len(ls)):
    print(str(ls[i]) + ' ' + event_name[i])