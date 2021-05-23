import sys
import mouse
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import clipboard


def set_browsers():    # set up browsers to be used with webbrowser library
    ff_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    webbrowser.register('Firefox', None, webbrowser.GenericBrowser(ff_path))

    edge_path = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
    webbrowser.register('Edge', None, webbrowser.BackgroundBrowser(edge_path))

    brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
    webbrowser.register('Brave', None, webbrowser.GenericBrowser(brave_path))

    # print('tryorder:', webbrowser._tryorder)    # use this to print list of usable browsers


def open_in(browser):  # this function opens the stream in the browser parameter. The browser MUST be defined above!!!
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

    new_URL = clipboard.paste()  # new_URL will be copied into clipboard
    # print('newURL:', newURL)
    new_browser = webbrowser.get(browser)
    new_browser.open(new_URL)
    print(f'\n~~~Overwatch League now playing on {browser}~~~')


def find_time_diff(match_time, curr_time):    # returns time difference between match and curr time in full time and in seconds
    hour_diff = int(match_time[:2]) - int(curr_time[:2])
    if hour_diff < 0:
        hour_diff = 0

    min_diff = int(match_time[3:5]) - int(curr_time[3:5])
    if min_diff < 0:
        min_diff = abs(60 + min_diff)
        hour_diff -= 1

    sec_diff = int(match_time[6:8]) - int(curr_time[6:8])
    if sec_diff < 0:
        sec_diff = abs(60 + sec_diff)
        min_diff -= 1

    if min_diff <= 0:
        min_diff = 0
    time_diff = datetime.time(hour_diff, min_diff, sec_diff)
    print(f'Match is in {time_diff}')

    time_diff_sec = (hour_diff * 3600) + (min_diff * 60) + sec_diff
    # print(f'Match is in {time_diff_sec} seconds')    # for debugging
    return time_diff, time_diff_sec


def main():
    match_time = ''
    # print(mouse.get_position())   # prints current mouse position, used to tweak the clicking commands.

    while ':' not in match_time:    # input validation
        match_time = input('Enter time of match in 24hr time format "xx:xx": ')

    if len(match_time) == 4:    # validation for time in AM not including leading 0 (ex. 2:00AM)
        match_time = '0'+match_time

    match_time = match_time + ':00'    # add seconds to match time
    curr_time = str(datetime.datetime.now())[11:19]    # get current time
    print(f'Time is currently: {curr_time}')

    # a = datetime.time(int(curr_time[:2]), int(curr_time[3:5]), int(curr_time[6:8]))  # see datetime docs

    new_match_time = match_time  # set this as a default value (match is same day)

    ''' If the match is in the morning of the next day, we need to use "48 hr time"
    # We add 24 hours to the match_time given so that the subtraction of new_match_time - curr_time is accurate instead of negative.
    # Example using current time 11:00PM and match time 1:00AM:'''
    #   match_time[:2] = 01          curr_time[:2] = 23
    if int(match_time[:2]) < 12 and int(curr_time[:2]) >= 12:
        new_match_time = str(int(match_time[:2]) + 24)   # 01 + 24 = 25
        new_match_time = new_match_time + ':' + match_time[3:]
        print(f'new match time to 48hr: {new_match_time}')  # new match time to 48hr: 25:00:00

    first = True    # first run in loop variable
    time_diff, time_diff_sec = find_time_diff(new_match_time, curr_time)    # if it is the first run in while loop, use new match time in 48hr time

    while True:
        curr_time = str(datetime.datetime.now())[11:19]    # get current time to compare to
        # print(f'comparing {match_time[:5]} and {curr_time[:5]}')

        if not first:    # if it is the second time, the comparison was wrong so use the current time
            time_diff, time_diff_sec = find_time_diff(match_time, match_time)    # get the new time diff (should not be needed, but added for safety)

        if match_time[:5] in curr_time[:5]:    # if the match time is IN current time it means within the minute. Change to [:4] for within 10 minutes.
            print(f"\nTime is currently: {curr_time[:5]}, which means It's Overwatch time baby!~~~~\n ")
            url = 'https://www.youtube.com/c/overwatchleague'    # this links to the Overwatch League's YouTube channel
            ff = webbrowser.get('Firefox')    # get the firefox browser
            ff.open(url)    # open the url in firefox
            time.sleep(4)    # sleep for 4 seconds to allow load time
            mouse.move(524, 950, absolute=True, duration=0.2)    # move mouse to upcoming live stream button coords
            # print(f'Upcoming live stream coords: {mouse.get_position()}')
            mouse.click('left')    # open stream
            time.sleep(1)
            print('\n~~~Overwatch League now playing on Firefox~~~')

            # optional: add multiple browsers with the same url (multiple accounts).
            open_in('Edge')
            open_in('Brave')
            time.sleep(1)
            break

        else:
            print(f'sleeping for {str(time_diff)[:2]} hour(s), {str(time_diff)[3:5]} mins, and {str(time_diff)[6:]} seconds')
            time.sleep(time_diff_sec)    # sleep until game time
            first = False    # not the first iteration in the loop

    sys.exit(0)    # exit the code


if __name__ == "__main__":
    main()
