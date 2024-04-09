
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

event_key = '2024cafr' 

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


'''
matches (list of list) format:

[
    [
        int:match number
        [-1, -1, -1] --> red alliance
        [-1, -1, -1] --> blue alliance
    ],
    ....
]
'''

qm_num = len(matches)

# part 1

print('1-----------------')
for i in range(qm_num):
    print()
    print(i+1)
    print()

print('--------------------------')
print()
print()


# part 2
print('2---------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][1][0])
print('--------------------------')
print()
print()


print('3---------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][1][1])
print('--------------------------')
print()
print()



print('4--------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][1][2])
print('--------------------------')
print()
print()



print('5---------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][2][0])
print('--------------------------')
print()
print()




print('6---------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][2][1])
print('--------------------------')
print()
print()




print('7---------------------')
for i in range(qm_num):
    print()
    print()
    print(matches[i][2][2])
print('--------------------------')
print()
print()