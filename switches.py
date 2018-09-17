''' program to email when a battery is low (below THRESHOLD in config file) '''
import json
import requests
import config
import utils

# Load the utils
gu = utils.GeniusUtility(config.HG_SIG)

# Get rooms with switches
switches = filter(lambda zone: zone['type']
                  == 'on / off', gu.getjson('/zones'))

# Build up the text
DEVICE_LIST = map(lambda switch: str(switch['id']) + ": switch " +
                  switch['name'] + " is " + switch['mode'], switches)

# Print list
for result in DEVICE_LIST:
    print(result)
