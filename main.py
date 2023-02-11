# how do i make a key be secret this is so hard

import os
import requests 
# http requests
# let's pretend i have this package
from cachecontrol import CacheControl
# this is supposed to help or something 
# look here https://github.com/frc1418/tbapy/blob/master/tbapy/main.py


link = 'https://www.thebluealliance.com/api/v3'

def printStuff(stuff):
    # treat this as a str obj
    print(stuff.text)
    print('\n\n\n')
    return

# totally not copied hahahahahhah
# not too sre what this does, there's something about thread safety but i honestly just use this to send get requests
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': input('What is your api key thing?\n')})

print('\n\nserver status:')
# get server status
response = session.get(link + '/status')
printStuff(response)
# wow i got a resposne

print('frc 840:')
response = session.get(link + '/team/frc840')
printStuff(response)

print('frc 254:')
response = session.get(link + '/team/frc254')
printStuff(response)


# use session.get(link + '/teams/[page]/keys') to get a list of keys
# it should just be "frc" + team number