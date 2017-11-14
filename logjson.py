''' program to email when a battery is low (below THRESHOLD in config file) '''
import json
import requests
import config

# Payload to get status - this is just a guess but appears to work.
GET_STATUS = '{"iMode":0}'

def getjson(identifier):
    """ gets the json from the supplied zone identifier """
    url = config.HG_URL + ":1223/v2/zone/" + str(identifier) +"?sig=" + config.HG_SIG
    response = requests.put(url, data=GET_STATUS)
    if response.status_code == 200:
        return json.loads(response.text)

    return {}


def putjson(identifier, data):
    """ gets the json from the supplied zone identifier """
    filename = str(identifier) + '.json'
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4,
                  ensure_ascii=False)



# List to hold results
ZONES = getjson(0)['data']['mappings']
# Find the zones
for value in ZONES.items():
    data = getjson(value[0])
    if data != {}:
        putjson(value[0], data)
