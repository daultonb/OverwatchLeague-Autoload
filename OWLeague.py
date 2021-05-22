import mouse
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import clipboard


#print(mouse.get_position())


ffpath = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None, webbrowser.GenericBrowser(ffpath))

edgepath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edgepath))

bravepath = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
webbrowser.register('brave', None, webbrowser.GenericBrowser(bravepath))

# use this to print list of usable browsers
#print('tryorder:', webbrowser._tryorder)


def openIn(browser):  # this function opens the stream in the browser parameter. The browser MUST be defined above!!!
    # move to the stream URL
    mouse.move(475, 52, absolute=True, duration=0.2)
    mouse.click('left')
    keyboard = Controller()

    # Select all of the url
    keyboard.press(Key.ctrl)
    keyboard.press('a')
    keyboard.release('a')
    time.sleep(1)
    # Copy
    keyboard.press('c')
    keyboard.release('c')
    keyboard.release(Key.ctrl)
    time.sleep(1)

    newURL = clipboard.paste()  # text will have the content of clipboard
    # print('newURL:', newURL)
    newBrowser = webbrowser.get(browser)
    newBrowser.open(newURL)
    print(f'\n~~~Overwatch League now playing on {browser}~~~')


''''''

match_time = ''
# input validation
while ':' not in match_time:
    match_time = input('Enter time of match in 24hr time format "xx:xx": ')

# validation for time in AM (ex. 2:00AM)
if len(match_time) == 4:
    match_time = '0'+match_time

match_time = match_time + ':00'  # add seconds
curr_time = str(datetime.datetime.now())[11:19]
print(f'Time is currently: {curr_time}')

a = datetime.time(int(curr_time[:2]), int(curr_time[3:5]), int(curr_time[6:8]))  # see datetime docs

# these two ifs convert to 48 hour time. This is useful if the game is at 1:00AM and it is currently 11:00PM.
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

if minDiff <= 0:
    minDiff = 0
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
        url = 'https://www.youtube.com/c/overwatchleague'

        ff = webbrowser.get('firefox')
        ff.open(url)

        time.sleep(4)
        # move mouse to upcoming live stream button coords
        mouse.move(524, 950, absolute=True, duration=0.2)
        # print(f'Upcoming live stream coords: {mouse.get_position()}')
        # left click on stream
        mouse.click('left')
        time.sleep(1)
        print('\n~~~Overwatch League now playing on Firefox~~~')

        # optional: add multiple browsers with the same url (multiple accounts).
        openIn('edge')
        openIn('brave')
        time.sleep(2)
        break

    else:
        print(f'sleeping for {timeDiff_sec} seconds')
        time.sleep(timeDiff_sec)
