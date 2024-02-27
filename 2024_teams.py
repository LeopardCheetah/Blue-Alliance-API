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
    r = get_stats(ls)
    print(title)
    print(f"Low: {r[0]}, High: {r[1]}, Median: {r[2]}")
    print(f"Average Value: {r[3]}, Standard Deviation: {r[4]}")
    print()
    print()
    return None



#################################################################

dump = getRequest('/event/2024isde1/matches')

amp_counts = []
speaker_counts = []
c = 0


## Note: 
## Bottom two parameters are ONLY for section 4 (see below)
ties = 0
a = 0
## 



for match in dump:

    m = match # preserving old code
    s = m["score_breakdown"]


    # investigate teleop amp counts
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

# analysis time
# amp_counts: [blue auto count, blue teleop, red auto, red teleop]
# speaker_counts: [blue auto, blue teleop (unamplified), blue amplified] + red
# c total matches




#####################################################################################


'''
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




# 5. Average number of notes in auton
auton_scored = []
for i in range(c):
    auton_scored.append(amp_counts[i][0] + speaker_counts[i][0]) # blue alliance auton
    auton_scored.append(amp_counts[i][2] + speaker_counts[i][3]) # red alliance auton

print_stats(auton_scored, "Average num of notes scored in autonomous")

'''



# figure out avg points
# avg robots climbed per match

