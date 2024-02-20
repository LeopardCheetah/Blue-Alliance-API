'''
goal: 
- figure out which teams that are going to our w1 are also going to our w2
- also figure the same thing out for w4
- see which teams we have in common from w2 -> w4
'''

import json
import requests 
from cachecontrol import CacheControl



link = 'https://www.thebluealliance.com/api/v3'

def getRequest(r):
    response = session.get(link + r)
    return json.loads(response.text)


f = open("secrets.txt", "r") # to replace with wherever u store your secrets
key = f.readline().strip()

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})



dump = getRequest('/event/2024week0/matches')
bad_matches = [0, 1, 2, 4, 5] # f1, f2, f3 don't exist on TBA and qm2 and qm3 have incorrect data

c = 0
a = 0

for match in range(len(dump)):
    # access using dump[match]
    if match in bad_matches:
        continue

    m = dump[match]

    blue_auto = int(dump[match]["score_breakdown"]["blue"]["autoPoints"])
    red_auto = int(dump[match]["score_breakdown"]["red"]["autoPoints"])

    winner = dump[match]["winning_alliance"]

    c += 1
    if winner == 'blue' and blue_auto > red_auto:
        a += 1
        continue

    if winner == 'red' and red_auto > blue_auto:
        a += 1
        continue
    
    print(dump[match]['key'])

print(a, c, a/c)

    
    

