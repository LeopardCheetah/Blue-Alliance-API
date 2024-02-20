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




#################################################################



dump = getRequest('/event/2024week0/matches')
bad_match_ids = ['_qm2', '_qm3', 'f1m1', 'f1m2', 'f1m3'] # f1, f2, f3 don't exist on TBA and qm2 and qm3 have incorrect data

amp_counts = []
speaker_counts = []
c = 0

for match in dump:

    if match['key'][-4:] in bad_match_ids:
        continue

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


# analysis time
# amp_counts: [blue auto count, blue teleop, red auto, red teleop]
# speaker_counts: [blue auto, blue teleop (unamplified), blue amplified] + red
# c total matches



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

note_comparison.sort()
print(note_comparison)
print("average teleop - auto note count: ", sum(note_comparison)/c)
print()
print()





# 2. compare amp vs speaker
amp_v_speaker = []
for i in range(c):
    amp = sum(amp_counts[i])
    speaker = sum(speaker_counts[i])

    amp_v_speaker.append(speaker - amp)

amp_v_speaker.sort()
print(amp_v_speaker)
print("avg num of notes scored more in speaker than in amp: ", sum(amp_v_speaker)/c)
print()
print()





# 3. total notes scored per match
total_notes = []
for i in range(c):
    total_notes.append(sum(amp_counts[i]) + sum(speaker_counts[i]))

total_notes.sort()
print(total_notes)
print('avg num of notes/match scored:', sum(total_notes)/c)
print()
print()
'''
