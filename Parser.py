import csv
import xml.etree.ElementTree as ET

from Util import calc_millisec

xml = 'current.xml'  # use 'current.xml' not results


def get_stint_info():
    stint_tree = ET.parse(xml)
    stint_root = stint_tree.getroot()
    stint_info = {}
    for result in stint_root.iter('result'):
        team_dict = {'last_time_line': result.get('lasttimeline'),
                     'car_number': result.get('no')
                     }
        if result.get('totaltime') == '':
            team_dict['total_time'] = '00:00:00.000'
        else:
            team_dict['total_time'] = result.get('totaltime')
        stint_info[result.get('regnumber')] = team_dict
    return stint_info


def get_leader_board():
    leader_board_tree = ET.parse(xml)
    leader_board_root = leader_board_tree.getroot()
    leader_board = {}
    for result in leader_board_root.iter('result'):
        team_dict = {
            'car_num': result.get('no'),
            'position': result.get('position'),
            'team_name': result.get('firstname'),
            'avg_lap_time': result.get('averagetime'),
            'last_time': result.get('lasttime'),
            'total_time': result.get('totaltime')
            # add more fields
        }
        leader_board[result.get('regnumber')] = team_dict
    return leader_board


def get_race_data():
    race_data_tree = ET.parse(xml)
    race_data_root = race_data_tree.getroot()
    labels = race_data_root.findall('label')
    race_data = {}
    for label in labels:
        race_data[label.get('type')] = label.text
    return race_data


def get_last_pit_lap():
    pit_lap_tree = ET.parse(xml)
    pit_lap_root = pit_lap_tree.getroot()
    pit_lap_info = {}
    for result in pit_lap_root.iter('result'):
        team_dict = {
            'last_pit_lap': result.get('lastpitstop')
        }
        pit_lap_info[result.get('no')] = team_dict
    return pit_lap_info


def parse_lap_times():
    with open('CurrentLapTimes') as lap_times_csv:
        lap_times_obj = csv.reader(lap_times_csv)
        lap_times_dict = {}
        for row in lap_times_obj:
            if len(row[0]) > 10:
                car_number_stripped = row[0][:3].strip()
                car_number = car_number_stripped.strip(" -")

            elif row[-1] != 'Speed':
                if car_number in lap_times_dict:
                    lap_times_dict[car_number][row[1]] = row[0]
                else:
                    lap_times_dict[car_number] = {}
                    lap_times_dict[car_number][row[1]] = row[0]
    return lap_times_dict


def get_last_pit_dict():
    race_data = get_race_data()
    last_pit_lap = get_last_pit_lap()
    lap_times = parse_lap_times()

    current_time = calc_millisec(race_data['timeofday'])  # must add '.000' b/c race_data doesn't include ms
    race_time = calc_millisec(race_data['racetime'])
    race_time_diff = abs(current_time - race_time)

    last_pit_laps = {}
    for team in last_pit_lap:
        last_pit_laps[team] = last_pit_lap[team]['last_pit_lap']  # populating last_pit_laps w/ {car_num: lastpitlap #}

    team_last_pit_dict = {}
    for car in last_pit_laps:
        if car not in lap_times:
            team_last_pit_dict[car] = "0"  # LapTimes.csv drops cars w/ no passings, must avoid key error

        elif current_time >= race_time:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # fetching respective lap times
            team_last_pit_dict[car] = last_pit_tod - race_time_diff           # using car number and selecting last pit

        else:
            last_pit_tod = calc_millisec(lap_times[car][last_pit_laps[car]])  # this accounts for races that
            team_last_pit_dict[car] = last_pit_tod + race_time_diff                  # run past 23:59:59 (TOD)

    return team_last_pit_dict
