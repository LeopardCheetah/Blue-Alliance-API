import json
import requests 
from cachecontrol import CacheControl



link = 'https://www.thebluealliance.com/api/v3'

def getRequest(r):
    response = session.get(link + r)
    return json.loads(response.text)


# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': 'key'})


dump = getRequest('/event/2023cafr/teams/simple')

teams_ls = []
for team_dict in dump:
    # so basically in dump_ls, each team is like an element 
    # of the list and then in each item in the list has info on the team
    # like it would be [{100 info}, {101 info}, {102 info}, etc.]
    # team_number is just one element that has like the team number in it
    teams_ls.append(int(team_dict['team_number']))


