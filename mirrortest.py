''' This module gets the json data from the heat genius house controller
 and publishes to firebase '''
import config
import utils


# Switch to read JSON from file
gu = utils.GeniusUtility(config.HG_URL, config.HG_SIG,
                         True, config.REFRESH_INTERVAL)

# Get the data
whole_house = gu.GETJSON(0)
zone_list = gu.getzonelist(whole_house)

device_list = []

for zone in zone_list:
    devices = zone_list[zone]['zone']
    mode = zone_list[zone]['iMode']
    key = zone_list[zone]['key']
    current_temperature = None
    target_temperature = None

    for device in devices.items():
        device_id, device_raw = device
        device_type = device_raw['type']
        if device_type == 'Sensor':
            current_temperature = device_raw['TEMPERATURE']
        elif device_type == 'Radiator valve':
            target_temperature = device_raw['HEATING_1']

    if current_temperature and target_temperature:
        print(zone, current_temperature, target_temperature)
        device_list.append(key)


for id in device_list:
    print(id)
    current_temperature, set_temperature, mode = gu.GET_TEMPERATURE(id)
    print(id, current_temperature, set_temperature, mode)
