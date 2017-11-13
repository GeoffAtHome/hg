''' test program to converts hg json data to arrays to work better with firebase '''
import time
import json
import config


def readzonelist():
    """ gets the json from the supplied zone identifier """
    try:
        with open('zonelist.json', 'r') as json_data:
            return json.load(json_data)

    except IOError:
        return {}

def convertzonelist(datalist):
    """ converts zonelist into arrays to be firebase friendly when binding to polymer """
    result = {'timestamp': int(time.time()), 'zones': [], 'interval': config.REFRESH_INTERVAL}
    for room in datalist.items():
        devices = []
        for device in room[1].items():
            readings = []
            devicetype = ''
            for reading in device[1].items():
                if 'type' in reading:
                    devicetype = reading[1]
                else:
                    readings.append(reading)

            devices.append({"readings": readings, "devicetype": devicetype, "device": device[0]})

        result['zones'].append({'name': room[0], 'devices': devices})

    return result


ZONELIST = readzonelist()
DATA = convertzonelist(ZONELIST)

print(DATA)
