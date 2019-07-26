import xml.etree.ElementTree as ET

tree = ET.parse('Testresults.xml')  # use 'current.xml' not results
root = tree.getroot()


def get_leader_board():
    leader_board = []
    for result in root.iter('result'):
        team_dict = {}  # rewite as a literal
        team_dict['position'] = result.get('position')
        team_dict['car_number'] = result.get('no')
        team_dict['team_name'] = result.get('firstname')
        # add more fields
        leader_board.append(team_dict)
    return leader_board


def get_race_data():
    labels = root.findall('label')
    race_data = {}
    for label in labels:
        race_data[label.get('type')] = label.text
    return race_data
