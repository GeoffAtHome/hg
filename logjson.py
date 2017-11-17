''' program to email when a battery is low (below THRESHOLD in config file) '''
import utils


# List to hold results
ZONES = utils.GETJSON(0)['data']['mappings']
# Find the zones
for value in ZONES.items():
    data = utils.GETJSON(value[0])
    if data != {}:
        utils.putjson(value[0], data)
