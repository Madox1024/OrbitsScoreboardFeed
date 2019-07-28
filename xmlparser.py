import xml.etree.ElementTree as ET

tree = ET.parse('Testresults.xml')  # use 'current.xml' not results
root = tree.getroot()
# VB ^ You can delete this now, right?


def get_stint_info():
    stint_tree = ET.parse('Testresults.xml')  # use 'current.xml' not results
    # VB Should definitely change all these methods to take the filename as a parameter
    stint_root = stint_tree.getroot()
    stint_info = {}
    for result in stint_root.iter('result'):
        team_dict = {}  # rewite as a literal
        team_dict['last_time_line'] = result.get('lasttimeline')
        if result.get('totaltime') == '':
            team_dict['total_time'] = '00:00:00.000'
        else:
            team_dict['total_time'] = result.get('totaltime')
        stint_info[result.get('no')] = team_dict
    return stint_info


def get_leader_board():
    leader_board_tree = ET.parse('Testresults.xml')  # use 'current.xml' not results
    leader_board_root = leader_board_tree.getroot()
    leader_board = []
    for result in leader_board_root.iter('result'):
        team_dict = {}  # rewite as a literal
        team_dict['position'] = result.get('position')
        team_dict['car_number'] = result.get('no')
        team_dict['team_name'] = result.get('firstname')
        # add more fields
        leader_board.append(team_dict)
    return leader_board


def get_race_data():
    race_data_tree = ET.parse('Testresults.xml')  # use 'current.xml' not results
    race_data_root = race_data_tree.getroot()
    labels = race_data_root.findall('label')
    race_data = {}
    for label in labels:
        race_data[label.get('type')] = label.text
    return race_data
