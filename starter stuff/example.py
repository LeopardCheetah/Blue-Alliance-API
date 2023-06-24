# example file 

import json # parser
import requests 
# http requests
# let's pretend i have this package
from cachecontrol import CacheControl
# this is supposed to help or something 
# look here https://github.com/frc1418/tbapy/blob/master/tbapy/main.py


link = 'https://www.thebluealliance.com/api/v3'

def getRequest(r):
    response = session.get(link + r)
    # return the text version but after json format => list of dicts if requesting teams
    return json.loads(response.text)

# notes: cvr - cafr, svr - casj

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': 'key'})


dump = getRequest('', '/event/2023cafr/teams/simple')

teams_ls = []
for team_dict in dump:
    # so basically in dump_ls, each team is like an element 
    # of the list and then in each item in the list has info on the team
    # like it would be [{100 info}, {101 info}, {102 info}, etc.]
    # team_number is just one element that has like the team number in it
    teams_ls.append(int(team_dict['team_number']))


