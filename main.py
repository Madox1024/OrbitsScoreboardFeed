import json
import os
import time

from xmlparser import get_leader_board

refresh_rate = 0.5


def mod_time():
    result = os.path.getmtime('current.xml')  # use current.xml
    return result


def gen_json():
    with open('leaderboard.json', 'w') as json_file:
        json.dump(get_leader_board(), json_file)


mod_time_old = mod_time()
while True:
    if mod_time() != mod_time_old:
        gen_json()
        mod_time_old = mod_time()
        print("leaderboard.json Updated")
    time.sleep(refresh_rate)
