# how do i make a key be secret this is so hard

import json # parser
import requests 
# http requests
# let's pretend i have this package
from cachecontrol import CacheControl
# this is supposed to help or something 
# look here https://github.com/frc1418/tbapy/blob/master/tbapy/main.py


link = 'https://www.thebluealliance.com/api/v3'


def getRequest(message, request):
    print('\n\n'+message)
    response = session.get(link + request)
    return response



# totally not copied hahahahahhah
# not too sre what this does, there's something about thread safety but i honestly just use this to send get requests
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': input('What is your api key thing?\n')})

'''
get('server status', '/status')
'''


# 2023 casj => svr 2023
# 2023 cafr => cvr 2023
dump = getRequest('', '/event/2023casj/teams/simple')
dump_svr = dump.text

dump_ls = json.loads(dump_svr)
# actually a list of dicts
teams_ls = []
for team_dict in dump_ls:
    teams_ls.append(int(team_dict['team_number']))

teams_ls.sort()
print('teams going to svr (2023):\n', teams_ls, end ='')


dump = getRequest('', '/event/2023cafr/teams/simple')
cvr_teams = json.loads(dump.text)
cvr_team_ls = []

for p in cvr_teams:
    cvr_team_ls.append(int(p['team_number']))

cvr_team_ls.sort()
print('teams going to cvr (2023):')
print(cvr_team_ls)

print('\n\n')

for i in cvr_team_ls:
    if i in teams_ls:
        print(i)
