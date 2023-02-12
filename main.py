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
    print('\n\n'+message+':')
    response = session.get(link + request)
    return response


def printStuff(stuff):
    # treat this as a str obj
    print(stuff.text)
    print('\n\n\n')
    return

# totally not copied hahahahahhah
# not too sre what this does, there's something about thread safety but i honestly just use this to send get requests
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': input('What is your api key thing?\n')})

'''
get('server status', '/status')
'''

'''
print('2022 keys:')
response = session.get(link + '/events/2022/keys')
printStuff(response)

print('2023 keys:')
response = session.get(link + '/events/2023/keys')
printStuff(response)
'''

'''
response = session.get(link + '/match/2022casj_qm49')
printStuff(response)
'''



dump = getRequest('team codes', '/event/2023casj/teams/simple')
dump = dump.text

dump_ls = json.loads(dump)
# actually a list of dicts
teams_ls = []
for team_dict in dump_ls:
    teams_ls.append(int(team_dict['team_number']))

teams_ls.sort()
print(teams_ls)