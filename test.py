import json 
import requests 
from cachecontrol import CacheControl

link = 'https://www.thebluealliance.com/api/v3'

def getRequest(r):
    response = session.get(link + r)
    return json.loads(response.text)


# if you are just running locally you can replace key with the string of the key
env_key_file = open("key.txt", "r")
key = env_key_file.readline().strip()

# add session header
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})

#######################

teams_at_capt = getRequest('/event/2025capt/teams')
print(teams_at_capt)