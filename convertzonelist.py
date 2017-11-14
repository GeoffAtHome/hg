''' test program to converts hg json data to arrays to work better with firebase '''
import time
import json
import config


def getjson(identifier):
    """ gets the json from the supplied zone identifier """
    filename = str(identifier) + '.json'
    try:
        with open(filename, 'r') as json_data:
            return json.load(json_data)['data']

    except IOError:
        return {}


def readzonelist():
    """ gets the json from the supplied zone identifier """
    try:
        with open('zonelist.json', 'r') as json_data:
            return json.load(json_data)

    except IOError:
        return {}

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


WHOLEHOUSE = getjson(0)
ZONE_LIST = readzonelist()
DATA = convertzonelist(ZONE_LIST, WHOLEHOUSE)

print(DATA)
