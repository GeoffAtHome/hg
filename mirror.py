''' This module gets the json data from the heat genius house controller
 and publishes to firebase '''
import time
import json
import requests
import config
from firebase import firebase


# Payload to get status - this is just a guess but appears to work.
GET_STATUS = '{"iMode":0}'

def getvalue(key, node):
    """ returns the value using the key in the supplied node.
    If the key is not present 'unknown' is returned """
    if key in node['childValues']:
        return node['childValues'][key]['val']
    return "unknown"


def getjson(identifier):
    """ gets the json from the supplied zone identifier """
    url = config.HG_URL + ":1223/v2/zone/" + str(identifier) +"?sig=" + config.HG_SIG
    response = requests.put(url, data=GET_STATUS)
    if response.status_code == 200:
        return json.loads(response.text)['data']

    return {}


def getpath(path):
    """ returns the last part of the supplied path """
    pathlist = path.split('/')
    return pathlist[len(pathlist)-1]


def setzonetype(area):
    """ sets the device type for the devices found in the supplied zone """
    for item in area:
        if item != 'lastseen':
            device = area[item]
            devicetype = 'unknown'
            if 'HEATING_1' in device:
                devicetype = 'Radiator valve'
            elif 'TEMPERATURE' in device:
                devicetype = 'Sensor'
            elif 'SwitchBinary' in device:
                devicetype = 'Switch'

            area[item]['type'] = devicetype

    return area


def getzonelist(wholehouse):
    ''' get the json data for the house '''
    roomlist = {}

    zones = wholehouse['mappings']
    # Find the zones
    for value in zones.items():
        data = getjson(value[0])
        if data != {}:
            zone = {}
            datapoints = data['datapoints']
            for item in datapoints:
                name = getpath(item['path'])
                if name not in zone:
                    zone[name] = {}
                    node = list(filter(lambda x, lookup=name: x['addr'] == lookup,
                                       data['nodes']))[0]
                    zone[name]['lastseen'] = node['childValues']['lastComms']['val']

                val = item['val']
                addr = item['addr']
                zone[name][addr] = val

            roomlist[data['strName']] = setzonetype(zone)

    return roomlist


def write_to_file(data):
    """ writes json data to file 'zonelist.json' """
    with open('zonelist.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

def convertzonelist(datalist, wholehouse):
    """ converts zonelist into arrays to be firebase friendly when binding to polymer """
    result = {'timestamp': int(time.time()), 'strTime': wholehouse['strTime'],
              'weatherData': wholehouse['weatherData'],
              'tmBoilerDaily': wholehouse['tmBoilerDaily'],
              'tmBoilerWeekly': wholehouse['tmBoilerWeekly'],
              'interval': config.REFRESH_INTERVAL, 'zones': [], 'nodes': {}}
    node_list = {}
    for zone in datalist.items():
        node_short_list = []
        zone_name, nodes = zone
        for node in nodes.items():
            node_id, readings = node
            node_short_list.append({'node_id': node_id, 'node_type': readings['type']})
            node_list[node_id] = readings

        result['zones'].append({'name': zone_name,
                                'nodes': sorted(node_short_list,
                                                key=lambda x: x['node_type'], reverse=True)})

    result['nodes'] = node_list
    return result


# connect to firebase
AUTH = firebase.FirebaseAuthentication(config.FIREBASE_PASSWORD, config.FIREBASE_USER)
USER = AUTH.get_user()
FIRE = firebase.FirebaseApplication(config.FIREBASE_URL, None)
firebase.authentication = AUTH

# Loop collecting the data
while True:
    # Get the data
    WHOLEHOUSE = getjson(0)
    ZONE_LIST = getzonelist(WHOLEHOUSE)

    # Write data to file
    write_to_file(ZONE_LIST)

    # Converts into arrays
    DATA = convertzonelist(ZONE_LIST, WHOLEHOUSE)

    # Write to Firebase
    FIRE.put('/', 'data', DATA)

    # wait for next interval
    time.sleep(config.REFRESH_INTERVAL)
