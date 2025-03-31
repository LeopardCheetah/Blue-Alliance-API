import json 
import requests 
from cachecontrol import CacheControl

link = 'https://www.thebluealliance.com/api/v3'



# note that the response is always in list format
# depending on the content of the thing ur requesting, the elements in that list can either be dictionaries or strings
def getRequest(r):

    response = session.get(link + r)
    # return the text version but after json format => list of dicts if requesting teams
    return json.loads(response.text)






# we in 2025 now


env_key_file = open("key.txt", "r") # todo: switch to .env packages
key = env_key_file.readline().strip()

# request header, basically prelimnary information about a request before its sent (sender basically)
session = CacheControl(requests.Session())
session.headers.update({'X-TBA-Auth-Key': key})

#######################




# time to look for other stats!!!!
# the fun ones


event_list = getRequest('/events/2025')

event_codes = []

for _event in event_list:
    # _event is a dict describing each event
    # see 2025_json_format.txt for some more information


    _event_week = _event["week"]
    _event_key = _event["key"]
    _event_type = _event["event_type_string"]


    # weeks are 0 indexed
    # week 1 events --> event_week = 0
    # only allow w1/w2 events to be queried
    if (_event_type == "Regional" or _event_type == "District") and _event_week in [i for i in range(5)]:
        event_codes.append(_event_key)
    



total_match_count = 0
non_qm_match_count = 0
red_qm_wins = 0
red_non_qm_wins = 0
ties = 0
ties_non_qm = 0
non_qm_ties_keys = []

highest_tie_score = -1
highest_tie_key = ''
lowest_tie_score = 300
lowest_tie_key = ''
# from this, we can get blue qm wins (= total qm - red qm => total match - non qm match - red qm)

# only look at qms
red_coop_count = 0
blue_coop_count = 0
coop_count = 0 

for _event_key in event_codes:

    # _event_key is a string and it is the event id (e.g. caoc)
    
    _event_match_info = getRequest(f'/event/{_event_key}/matches')
    # request = getRequest(f'/event/2024cabe/matches')

    # this is now a massive dictionary of just every match that ever happened

    
    

    for _match in _event_match_info:
        # ok now we can dig into each individual match


        _is_qm = True

        if _match["comp_level"] != 'qm':
            # treat these differently
            _is_qm = False
            non_qm_match_count += 1

        total_match_count += 1
        

        # did red or blue win more?

        if _match["winning_alliance"] is None:
            # is tba has not finished this qm (looking at you talahassee regional)
            continue

        try:
            if _match["score_breakdown"]["red"]["totalPoints"] is None:
                continue 
        except:
            continue
        
        if _match["winning_alliance"] == "red":
            if _is_qm:
                red_qm_wins += 1
            else:
                red_non_qm_wins += 1
        else:
            if _match["score_breakdown"]["red"]["totalPoints"] == _match["score_breakdown"]["blue"]["totalPoints"]:
                # tie!
                if highest_tie_score < _match["score_breakdown"]["red"]["totalPoints"]:
                    highest_tie_score = _match["score_breakdown"]["red"]["totalPoints"]
                    highest_tie_key = _match["key"]

                if lowest_tie_score > _match["score_breakdown"]["red"]["totalPoints"]:
                    lowest_tie_score = _match["score_breakdown"]["red"]["totalPoints"]
                    lowest_tie_key = _match["key"]
                
                if _is_qm:
                    ties += 1
                else:
                    ties_non_qm += 1
                    non_qm_ties_keys.append(_match["key"])


        # what's co-op looking like?
        # only look at qms
        if _match["score_breakdown"]["blue"]["wallAlgaeCount"] > 1 and _is_qm:
            blue_coop_count += 1
        
        if _match["score_breakdown"]["red"]["wallAlgaeCount"] > 1 and _is_qm:
            red_coop_count += 1
        
        if _match["score_breakdown"]["blue"]["wallAlgaeCount"] > 1 and _match["score_breakdown"]["red"]["wallAlgaeCount"] > 1 and _is_qm:
            coop_count += 1


qm_match_count = total_match_count - non_qm_match_count

print()
print()
print(f"Total match count: {total_match_count}")
print(f"Total Qual and Non-Qual match count: {qm_match_count}, {non_qm_match_count}")
print(f"Number of wins for the red alliance (qual and non qual): {red_qm_wins} ({100*(red_qm_wins/(qm_match_count)):.2f}%) | {red_non_qm_wins} ({100*(red_non_qm_wins/non_qm_match_count):.2f}%)")
print(f"Number of ties (qual and non qual): {ties} ({100*(ties/(qm_match_count)):.2f}%) | {ties_non_qm} ({100*(ties_non_qm/non_qm_match_count):.2f}%)")
print(f"Highest and lowest scoring tie (and key): {highest_tie_score} ({highest_tie_key}) | {lowest_tie_score} ({lowest_tie_key})")
print(f"Keys of all playoff ties: {non_qm_ties_keys}")
print()

# coop
print(f"Co-op percentage (globally): {coop_count}/{qm_match_count} ({100*(coop_count/qm_match_count):.2f}%)")
print(f"Matches where one side co-oped but the other didn't: {red_coop_count + blue_coop_count - 2*coop_count}/{qm_match_count} ({100*((red_coop_count + blue_coop_count - 2*coop_count)/qm_match_count):.2f}%)")
print()
print()



