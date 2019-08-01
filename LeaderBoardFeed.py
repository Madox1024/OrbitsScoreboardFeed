import json
import os
import time

from XMLParser import get_leader_board

refresh_rate = 0.5


def mod_time():
    result = os.path.getmtime('Testresults.xml')  # use current.xml
    return result


def gen_json():
    with open('leaderboard.json', 'w') as json_file:
        json.dump(get_leader_board(), json_file)


def start_leader_board_feed():
    mod_time_old = mod_time()
    while True:
        if mod_time() != mod_time_old:
            gen_json()
            mod_time_old = mod_time()
        time.sleep(refresh_rate)
