''' program to email when a battery is low (below THRESHOLD in config file) '''
import utils


# List to hold results
ZONES = utils.GETFULLJSON(0)['data']['mappings']
# Find the zones
for value in ZONES.items():
    data = utils.GETFULLJSON(value[0])
    if data != {}:
        utils.putjson(value[0], data)
