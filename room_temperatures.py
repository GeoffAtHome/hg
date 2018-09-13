''' program to email when a battery is low (below THRESHOLD in config file) '''
import json
import requests
import config


def getjson(identifier):
    """ gets the json from the supplied zone identifier """
    url = config.HG_URL + identifier
    try:
        headers = {'Authorization': 'Bearer ' + config.HG_SIG}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.text)

    except Exception as ex:
        print("Failed requests in getjsonfromhttp")
        print(ex)
        return None


# List to hold results
DEVICE_LIST = []
ZONES = getjson('/zones')
# Find the zones
for zone in ZONES:
    if 'temperature' in zone:
        temperature = zone['temperature']
        room = zone['name']
        zone_id = zone['id']
        text = str(zone_id) + ": temperature in " + \
            room + " is " + str(temperature)
        DEVICE_LIST.append(text)

# Print sorted list
DEVICE_LIST = sorted(DEVICE_LIST, key=lambda x: int(x.split(':')[0]))
for result in DEVICE_LIST:
    print(result)
