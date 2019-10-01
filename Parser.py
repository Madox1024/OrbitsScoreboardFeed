import csv
import time
import xml.etree.ElementTree as ET

from Util import calc_millisec


class XMLParser:

    def __init__(self):
        self.file_name = 'current.xml'
        self.parse_wait = 0.3

    def get_stint_info(self):
        try:
            stint_tree = ET.parse(self.file_name)
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
        except ET.ParseError:
            time.sleep(self.parse_wait)
            return self.get_stint_info()

    def get_leader_board(self):
        try:
            leader_board_tree = ET.parse(self.file_name)
            leader_board_root = leader_board_tree.getroot()
            leader_board = {}
            for result in leader_board_root.iter('result'):
                team_dict = {
                    'car_num': result.get('no'),
                    'position': result.get('position'),
                    'team_name': result.get('firstname'),
                    'best_lap_time': result.get('besttime'),
                    'last_time': result.get('lasttime'),
                    'total_time': result.get('totaltime')
                    # add more fields
                }
                if result.get('sincepit') == '':
                    team_dict['since_pit'] = 0
                else:
                    team_dict['since_pit'] = result.get('sincepit')
                leader_board[result.get('regnumber')] = team_dict
            return leader_board
        except ET.ParseError:
            time.sleep(self.parse_wait)
            return self.get_leader_board()

    def get_race_data(self):
        try:
            race_data_tree = ET.parse(self.file_name)
            race_data_root = race_data_tree.getroot()
            labels = race_data_root.findall('label')
            race_data = {}
            for label in labels:
                race_data[label.get('type')] = label.text
            return race_data
        except ET.ParseError:
            time.sleep(self.parse_wait)
            return self.get_race_data()


class CSVParser:

    def __init__(self, file_name):
        self.file_name = file_name

    def gen_last_pit_dict(self):
        if self.file_name != 'N/A':
            with open(self.file_name, 'r') as passings_csv:
                passings_obj = csv.reader(passings_csv)
                passings_dict = {}
                for passing in passings_obj:
                    try:
                        if 'P' in passing[3]:
                            if passing[1] in passings_dict:
                                if passings_dict[passing[1]] < calc_millisec(passing[7]):
                                    passings_dict[passing[1]] = calc_millisec(passing[7])
                            elif passing[1] != '':
                                passings_dict[passing[1]] = calc_millisec(passing[7])
                    except IndexError:
                        time.sleep(1)
                        return self.gen_last_pit_dict()
                return passings_dict
