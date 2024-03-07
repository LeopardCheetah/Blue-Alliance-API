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
print()
print() 



def get_stats(ls):
    ls.sort()
    mean = sum(ls)/len(ls)

    # round the mean
    mean *= 100
    mean = int(mean)
    mean /= 100


    mid = -1

    if len(ls) % 2 == 0:
        mid = (ls[len(ls)//2] + ls[len(ls)//2 - 1])/2
    else:
        mid = ls[len(ls)//2]

    min_val = min(ls)
    max_val = max(ls)

    
    std_dev = int((sum([(i - mean)**2 for i in ls])/(len(ls) - 1))**0.5)

    # return min, max, median, avg, std.dev
    return [min_val, max_val, mid, mean, std_dev]

def print_stats(ls, title):
    print()
    r = get_stats(ls)
    print(title)
    print(f"Low: {r[0]}, High: {r[1]}, Median: {r[2]}")
    print(f"Average Value: {r[3]}, Standard Deviation: {r[4]}")
    print()
    return None



#################################################################


# loop over all events
# figure out which ones you need!
event_list = ['2024bcvi']





# for O(1) amortization all w1 keys will be listed here
# note that THIS IS NOT ALL W1 EVENTS -- TBA cant find some 


event_list = ['2024bcvi', '2024brbr', '2024caph', '2024casj', '2024cthar', '2024flwp', '2024inmis', '2024isde1', '2024isde2', '2024isde3', '2024mibat', '2024miber', '2024mibkn', '2024miket', '2024mimil', '2024mndu', '2024mndu2', '2024mxmo', '2024ncwak', '2024nhgrs', '2024njfla', '2024orore', '2024paca', '2024pahat', '2024qcmo', '2024tnkn', '2024txkat', '2024txwac', '2024utwv', '2024vaash', '2024vabla', '2024wasno']


'''
# get all week 1 events
# comment this out if you don't want this!

all_event_keys = getRequest('/events/2024/keys')

# uhm this is sorta wasteful but i dont wanna check in the comp so yeah
# there's probably a way to refactor everything for less requests but ehhhhh

event_list = []

for e in all_event_keys:
    r = getRequest(f'/event/{e}')

    # ok so the index is off by 1
    if r['week'] == 0:
        event_list.append(e)


print(event_list)
'''
########################################################################





# statistics stuff

amp_counts = []
speaker_counts = []
c = 0
qual_c = 0


# NOTE: this list has length 2n
# Classification scheme: [blue score, red score, ...]
scores = []


## Note: 
## Bottom two parameters are ONLY for section 4 (see below)
ties = 0
a = 0
## 


# Used for Section 7, rp
rp = []
rp_2 = []


melody_rp = [] # these will either be 0s or 1s
ensemble_rp = [] 


# 10
# robots climb?
robot_climb = []


# 11 
# coop
co_op_pressed = [] # 1/0 dependent on if alliance presses
co_op_matches = [] # was there a co-op press in the game
co_op_achieved = [] # did they ultimately get the pt





print('exec start')
print()

for event_key in event_list:

    dump = getRequest(f'/event/{event_key}/matches')

    print('getting data for event', event_key)

    for match in dump:

        m = match # preserving old code
        s = m["score_breakdown"]



        # ok so
        # f1m3 might not exist if teams just win the first 2/3
        # to counter this im gonna put this in a try except loop
        # if it fails just gonna skip

        try:
            dummy = s["blue"]["adjustPoints"]
        except:
            continue # circle back to next match


        # increment number of matches
        c += 1 

        blue_amp_auto = s["blue"]["autoAmpNoteCount"]
        blue_amp = s["blue"]["teleopAmpNoteCount"]

        red_amp_auto = s["red"]["autoAmpNoteCount"]
        red_amp = s["red"]["teleopAmpNoteCount"]
        
        # encode using (blue, red)

        amp_counts.append([blue_amp_auto, blue_amp, red_amp_auto, red_amp])

        b_sp_a = s["blue"]["autoSpeakerNoteCount"]
        r_sp_a = s["red"]["autoSpeakerNoteCount"]

        b_sp_t = s["blue"]["teleopSpeakerNoteCount"]
        r_sp_t = s["red"]["teleopSpeakerNoteCount"]
        
        b_sp = s["blue"]["teleopSpeakerNoteAmplifiedCount"]
        r_sp = s["red"]["teleopSpeakerNoteAmplifiedCount"]

        speaker_counts.append([b_sp_a, b_sp_t, b_sp, r_sp_a, r_sp_t, r_sp])


        blue_rp = s["blue"]["rp"]
        red_rp = s["red"]["rp"]
        rp.append(blue_rp)
        rp.append(red_rp)

        rp_2.append(blue_rp+red_rp)
        
        
        ###############################################

        if m["comp_level"] == 'qm':
            ## 9
            ## look for ensemble/note rps
            # only append 0/1, only look in quals
            qual_c += 1


            # ok yes since this is a bit swtich there are more effieicnt ways to do this
            if s["blue"]["melodyBonusAchieved"]:
                melody_rp.append(1)
            else:
                melody_rp.append(0)


            if s["red"]["melodyBonusAchieved"]:
                melody_rp.append(1)
            else:
                melody_rp.append(0)
            


            # ensemble
            if s['blue']['endGameTotalStagePoints'] >= 10:
                ensemble_rp.append(1)
            else:
                ensemble_rp.append(0)
            
            if s['red']['endGameTotalStagePoints'] >= 10:
                ensemble_rp.append(1)
            else:
                ensemble_rp.append(0)

            




            # 11, coop

            blue_co_op = s["blue"]["coopNotePlayed"]
            red_co_op = s["red"]["coopNotePlayed"]

            f = True
            if blue_co_op:
                co_op_pressed.append(1)
                co_op_matches.append(1)
                f = False
            else:
                co_op_pressed.append(0)
            
            
            if red_co_op:
                if f:
                    co_op_matches.append(1)
                    f = False
                
                co_op_pressed.append(1)
            else:
                co_op_pressed.append(0)
            
            if f:
                co_op_matches.append(0)
            
            # TODO: see if you can one liner this later
            if blue_co_op and red_co_op:
                co_op_achieved.append(1)
            else:
                co_op_achieved.append(0)
        


    ###########################################



        blue_score = s["blue"]["totalPoints"]
        red_score = s["red"]["totalPoints"]

        scores.append(blue_score)
        scores.append(red_score)



        blue_auto = int(match["score_breakdown"]["blue"]["autoPoints"])
        red_auto = int(match["score_breakdown"]["red"]["autoPoints"])

        winner = match["winning_alliance"]
        if winner == 'blue' and blue_auto > red_auto:
            a += 1
            continue

        if winner == 'red' and red_auto > blue_auto:
            a += 1
            continue
        
        if blue_auto == red_auto:
            ties += 1


        
        # 10, robot climb
        robot_num = s["blue"]["endGameOnStagePoints"] // 3 + s["red"]["endGameOnStagePoints"] // 3
        robot_climb.append(robot_num) 

        # compress them into a list of size n to even out the qualification shenanigans
        # beware of the doubling






# analysis time
# amp_counts: [blue auto count, blue teleop, red auto, red teleop]
# speaker_counts: [blue auto, blue teleop (unamplified), blue amplified] + red
# c total matches




#####################################################################################
print()
print()
print('----------------------Stats---------------------')
print()


# 1. compare how many notes were scored in teleop vs auto
note_comparison = []
for i in range(c):
    auto = amp_counts[i][0] + amp_counts[i][2]
    auto += speaker_counts[i][0] + amp_counts[i][3]

    # formula used here is 
    # sum of both lists == num of notes scored == teleop note number + auto note num
    # so just subtract auto note num

    teleop = sum(amp_counts[i]) + sum(speaker_counts[i]) - auto 

    note_comparison.append(teleop - auto)


print_stats(note_comparison, 'Teleop Note Count - Auto Note Count')




# 2. compare amp vs speaker
amp_v_speaker = []
for i in range(c):
    amp = sum(amp_counts[i])
    speaker = sum(speaker_counts[i])

    amp_v_speaker.append(speaker - amp)

print_stats(amp_v_speaker, "Speaker note count - Amp note count")





# 3. total notes scored per match
total_notes = []
for i in range(c):
    total_notes.append(sum(amp_counts[i]) + sum(speaker_counts[i]))

print_stats(total_notes, "Average number of notes per match")




# 4. correlation between winning in auto vs winning in the game
# also count ties!!!
print("Number of matches:", c)
print("Number of matches where auto lead won:", a)
print("Percentage:", str((int((a/c)*10000))/100)+'%') # hehe -- manual rounding
print("Number of auto ties:", ties)
print("Percentage of auto ties:", str((int((ties/c)*10000))/100)+'%')




# 5. Average number of notes in auton
auton_scored = []
for i in range(c):
    auton_scored.append(amp_counts[i][0] + speaker_counts[i][0]) # blue alliance auton
    auton_scored.append(amp_counts[i][2] + speaker_counts[i][3]) # red alliance auton

print_stats(auton_scored, "Average num of notes scored in autonomous")



# 6. Average scores
print_stats(scores, "Average points per alliance")



# 7. Average RPs
print_stats(rp, "Alliance RP statistics")



# 8. Average total RPs
print_stats(rp_2, "Total RP Statistics")


# 9. rp breakdown for each set
print_stats(melody_rp, "Melody RP Statistics (Quals)")
print_stats(ensemble_rp, "Ensemble RP Statistics (Quals)")



# 10. Average robots climbed
print_stats(robot_climb, "Total number of robots climbed (per match)")


# 11. co-op!!!
print_stats(co_op_matches, "Total number of matches that had co-op (Quals)")
print_stats(co_op_pressed, "Alliances that pressed co-op button (Quals)")
print_stats(co_op_achieved, "Matches that achieved co-op (Quals)")



print(f'Total number of matches looked at: {c}\nTotal number of quals looked at: {qual_c}')