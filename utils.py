
''' This module contains utility functions that are shared across other programs '''
import json
import time
import requests


class GeniusUtility():

    def __init__(self, host, key, file=None, refresh_interval=None):
        self._host = host
        self._key = key
        # Default to getting JSON from HTTP
        if file:
            self.GETJSON = self.getjsonfromfile
            print("Reading from file")
        else:
            self.GETJSON = self.getjsonfromhttp
            print("Reading from HTTP")
        self._refresh_interval = refresh_interval

    def getjsonfromhttp(self, identifier):
        """ gets the json from the supplied zone identifier """
        data = self.GETFULLJSON(identifier)
        if data != None:
            return data

        return None

    def GETURL(self, identifier):
        """ Build URL from config and identifier """
        return self._host + identifier

    def GETFULLJSON(self, identifier):
        """ gets the json from the supplied zone identifier """
        url = self.GETURL(identifier)
        try:
            headers = {'Authorization': 'Bearer ' + self._key}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return json.loads(response.text)

        except Exception as ex:
            print("Failed requests in getjsonfromhttp")
            print(ex)
            return None

    def getjsonfromfile(self, identifier):
        """ gets the json from the supplied zone identifier """
        filename = 'C:/Demos/hg/' + str(identifier) + '.json'
        try:
            with open(filename, 'r') as json_data:
                return json.load(json_data)['data']

        except IOError:
            return None

    def putjson(self, identifier, data):
        """ write the json from the supplied zone identifier """
        self.writejson(str(identifier) + '.json', data)

    def writejson(self, filename, data):
        """ write the json to the supplied filename """
        with open(filename, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True,
                      indent=4, ensure_ascii=False)

    def write_to_file(self, data):
        """ writes json data to file 'zonelist.json' """
        self.writejson('zonelist.json', data)

    def setzonetype(self, area):
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

    def checkgetattr(self, object, attribute, default):
        try:
            result = object[attribute]
            return result
        except KeyError:
            return default

    def getzonelist(self, wholehouse):
        ''' get the json data for the house '''
        roomlist = {}

        zones = wholehouse['mappings']
        # Find the zones
        for key, pair in sorted(zones.items()):
            pair = pair
            if key != '0':
                data = self.GETJSON(key)
                if data != None:
                    zone = {}
                    datapoints = data['datapoints']
                    for item in datapoints:
                        name = self.getpath(item['path'])
                        if name not in zone:
                            zone[name] = {}
                            node = list(filter(lambda x, lookup=name: x['addr'] == lookup,
                                               data['nodes']))[0]
                            zone[name]['lastseen'] = node['childValues']['lastComms']['val']

                        val = item['val']
                        addr = item['addr']
                        zone[name][addr] = val

                    zone = self.setzonetype(zone)
                    roomlist[data['strName']] = {'zone': zone, 'key': key, 'iPriority': data['iPriority'],
                                                 'bIsActive': data['bIsActive'],
                                                 'iMode': data['iMode'],
                                                 'iBoostTimeRemaining': data['iBoostTimeRemaining'],
                                                 'objFootprint': self.checkgetattr(data, 'objFootprint', None),
                                                 'objTimer': self.checkgetattr(data, 'objTimer', None),
                                                 'bOutRequestHeat': data['bOutRequestHeat']}

        return roomlist

    def getvalue(self, key, node):
        """ returns the value using the key in the supplied node.
        If the key is not present 'unknown' is returned """
        if key in node['childValues']:
            return node['childValues'][key]['val']
        return "unknown"

    def getpath(self, path):
        """ returns the last part of the supplied path """
        pathlist = path.split('/')
        return pathlist[len(pathlist) - 1]

    def convertzonelist(self, datalist, wholehouse):
        """ converts zonelist into arrays to be firebase friendly when binding to polymer """
        result = {'timestamp': int(time.time()), 'strTime': wholehouse['strTime'],
                  'weatherData': wholehouse['weatherData'],
                  'tmBoilerDaily': wholehouse['tmBoilerDaily'],
                  'tmBoilerWeekly': wholehouse['tmBoilerWeekly'],
                  'interval': self._refresh_interval, 'zones': [], 'nodes': {}}
        node_list = {}
        for zone in datalist.items():
            node_short_list = []
            zone_name, nodes = zone
            for node in nodes['zone'].items():
                node_id, readings = node
                node_short_list.append(
                    {'node_id': node_id, 'node_type': readings['type']})
                node_list[node_id] = readings

            result['zones'].append({'name': zone_name, 'bIsActive': nodes['bIsActive'],
                                    'iMode': nodes['iMode'],
                                    'iBoostTimeRemaining': nodes['iBoostTimeRemaining'],
                                    'objFootprint': ['objFootprint'],
                                    'bOutRequestHeat': nodes['bOutRequestHeat'],
                                    'iPriority': nodes['iPriority'], 'objTimer': nodes['objTimer'],
                                    'nodes': sorted(node_short_list, key=lambda x: x['node_type'], reverse=True)})

        result['nodes'] = node_list
        # Sort the zones based on priority
        result['zones'] = sorted(result['zones'], key=lambda x: x['iPriority'])
        return result

    def GET_TEMPERATURE(self, zone_id):
        zone = self.GETJSON(zone_id)
        mode = zone['iMode']
        current_temperature = None
        set_temperature = None
        for device in zone['datapoints']:
            if device['addr'] == 'HEATING_1':
                set_temperature = device['val']
            elif device['addr'] == 'TEMPERATURE':
                current_temperature = device['val']

        return current_temperature, set_temperature, mode

    def GET_MODE(self, mode):
        # Mode_Off: 1,
        # Mode_Timer: 2,
        # Mode_Footprint: 4,
        # Mode_Away: 8,
        # Mode_Boost: 16,
        # Mode_Early: 32,
        # Mode_Test: 64,
        # Mode_Linked: 128,
        # Mode_Other: 256
        mode_map = {1: "off", 2: "timer", 4: "footprint",
                    8: "away", 16: "boost", 32: "early", }

        return mode_map.get(mode, "off")

    def SOCKET_ON(self, id, seconds):
        data_to_send = '{"iMode":16,"iBoostTimeRemaining":' + \
            str(seconds) + '}'
        path = self.GETURL(id)
        # HG_HEATING_SOCKET = HG_URL + "22" + HG_SIG
        print(data_to_send)
        print(path)
        # requests.put(HG_HEATING_SOCKET, data=ON_DATA)
        # requests.put()

    def SOCKET_OFF(self, id):
        self.SOCKET_ON(id, 0)

    def CLEAR_TIMER(self, id):
        path = self.GETURL(id)
        # response = requests.options(path)
        message = self.GETFULLJSON(id)
        timer = message['ts']
        payload = {'error': 0,
                   'ts': timer,
                   'tm': message['tm'],
                   'data': {}
                   }

        for item in message['data']['objTimer']:
            if item['iTm'] != 0:
                message['data']['objTimer'].remove(item)

        for item in message['data']['objTimer']:
            if item['iTm'] != 0:
                message['data']['objTimer'].remove(item)

        for item in message['data']['objTimer']:
            if item['iTm'] != 0:
                message['data']['objTimer'].remove(item)

        print(message)
        print(payload)
        response = requests.options(path)
        # print(path, response)
        response.headers['Access-Control-Request-Method'] = 'PATCH'
        response = requests.patch(path, data=json.dumps(
            payload), headers=response.headers)
        print(path, response)
        response = requests.options(path)
        # print(path, response)
        response.headers['Access-Control-Request-Method'] = 'GET'
        response = requests.get(path, data=json.dumps(
            message), headers=response.headers)
        print(path, response)
