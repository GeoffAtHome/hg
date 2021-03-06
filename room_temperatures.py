''' program to email when a battery is low (below THRESHOLD in config file) '''
import json
import requests
import config
import utils

# Load the utils
gu = utils.GeniusUtility(config.HG_SIG)

# Get the rooms with temperatures
rooms = filter(lambda zone: 'temperature' in zone, gu.getjson('/zones'))

# Build up the text
DEVICE_LIST = map(lambda room: str(
    room['id']) + ": temperature in " + room['name'] + " is " + str(room['temperature']), rooms)

# Print list
for result in DEVICE_LIST:
    print(result)
