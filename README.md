# OrbitsScoreboardFeed Work in progress

This script is designed to parse the .xml data feed from MyLaps's Orbits 4 Scoring software and extract useful information and functionality

.xml data feed is overwritten ~.5sec

Main.py:
Watches for changes to the xml data feed, when the xml is modified it genreates a json file with leaderboard info

xmlparser.py:
Take a wild guess... parses xml and generates dicts and lists to be used elsewhere

DriverStintCheck:
Tracks each team and monitors their stint time, if a team has over 2 hours since last pit it will trigger a warning msg.
Resets with pit times and triggers pit msg

AbnormalLapCheck.py
Unfinished! Tracks each team and checks for long laps( > 1 min over avg) missed laps ( > double avg lap time) or dropouts ( more than 10 mins off track)

util.py:
Utility functions
