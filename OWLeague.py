import mouse
import time
import webbrowser
import datetime

#print(mouse.get_position())
''''''
match_time = input('Enter time of match in format "xx:xx": ')
if len(match_time) == 4:
    match_time = '0'+match_time
match_time = match_time + ':00'
curr_time = str(datetime.datetime.now())[11:19]
print(f'Time is currently: {curr_time}')

a = datetime.time(int(curr_time[:2]), int(curr_time[3:5]), int(curr_time[6:8]))


# these two ifs convert to 48 hour time.
# if they are both less than 12 it means the match is on the same day
if int(curr_time[:2]) < 12 & int(match_time[:2]) >= 12:
    new_currTime = str(int(curr_time[:2])+12)
    curr_time = new_currTime + ':' + curr_time[3:]
    print(f'curr_time to 48hr: {curr_time}')
# if they are both less than 12 it means the match is on the same day
if int(match_time[:2]) < 12 & int(curr_time[:2]) >= 12:
    new_matchTime = str(int(match_time[:2]) + 24)
    match_time = new_matchTime + ':' + match_time[3:]
    print(f'match_time to 48hr: {match_time}')

hourDiff = int(match_time[:2]) - int(curr_time[:2])
if hourDiff < 0:
    hourDiff = 0

minDiff = int(match_time[3:5]) - int(curr_time[3:5])
if minDiff < 0:
    minDiff = abs(60 + minDiff)
    hourDiff -= 1


secDiff = int(match_time[6:8]) - int(curr_time[6:8])
if secDiff < 0:
    secDiff = abs(60 + secDiff)
    minDiff -= 1


timeDiff = datetime.time(hourDiff, minDiff, secDiff)
print(f'Match is in {timeDiff} ')

timeDiff_sec = (hourDiff * 3600) + (minDiff * 60) + secDiff
print(f'Match is in {timeDiff_sec} seconds')

while True:
    curr_time = str(datetime.datetime.now())[11:19]
    print(f'comparing {match_time[:5]} and {curr_time[:5]}')
    if match_time[:5] in curr_time[:5]:

        print(f"\nTime is currently: {curr_time[:5]}, which means It's Overwatch time baby!~~~~\n ")
        time.sleep(1)
        webbrowser.open('http://overwatchleague.com')
        time.sleep(4)
        # move mouse to refresh button coords
        #mouse.move(-1088, -519, absolute=True, duration=0.2)
        #print(f'Refresh button coords: {mouse.get_position()}')
        # left click on refresh
        #mouse.click('left')
        #time.sleep(1)
        # move mouse to play button coords
        mouse.move(-730, 348, absolute=True, duration=0.2)
        time.sleep(1)
        #print(f'Play button coords: {mouse.get_position()}')
        # left click on play
        mouse.click('left')
        time.sleep(2)
        print('\n~~~Overwatch League now playing~~~')
        break
    else:
        print(f'sleeping for {timeDiff_sec} seconds')
        time.sleep(timeDiff_sec)
