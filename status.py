''' program to email when a battery is low (below THRESHOLD in config file) '''
import json
import smtplib
import requests
import config

# Payload to get status - this is just a guess but appears to work.
GET_STATUS = '{"iMode":0}'

def my_getjson(identifier):
    """ gets the json from the supplied zone identifier """
    url = config.HG_URL + ":1223/v2/zone/" + str(identifier) +"?sig=" + config.HG_SIG
    response = requests.put(url, data=GET_STATUS)
    if response.status_code == 200:
        return json.loads(response.text)['data']

    return {}


# List to hold results
DEVICE_LIST = []
BAD_LIST = []
ZONES = getjson(0)['mappings']
# Find the zones
for value in ZONES.items():
    data = getjson(value[0])
    if data != {}:
        room = data['strName']
        nodes = data['nodes']
        for node in nodes:
            node_id = node['addr']
            if 'Battery' in node['childValues']:
                if 'LUMINANCE' in node['childValues']:
                    device = "Room Sensor"
                elif 'HEATING_1' in node['childValues']:
                    device = "Radiator Valve"
                else:
                    device = "Unknown device"

                text = node_id + ": " + device + " in " + room
                level = node['childValues']['Battery']['val']
                text = text + " Battery level: " + str(level)
                DEVICE_LIST.append(text)
                if level < config.THRESHOLD:
                    BAD_LIST.append(text)

# Print sorted list
DEVICE_LIST = sorted(DEVICE_LIST, key=lambda x: int(x.split(':')[0]))
for result in DEVICE_LIST:
    print(result)

# Email bad list
if len(BAD_LIST) > 0:
    BAD_LIST = sorted(BAD_LIST, key=lambda x: int(x.split(':')[0]))
    print("Sending message")
    # Build message to send
    MSG = "\r\n".join(["From: " + config.FROM_ADDRESS, "To: " + config.TO_ADDRESS,
                       "Subject: Heat Genius batteries are low", "", ""])
    MSG += "\r\n".join(BAD_LIST)
    try:
        SERVER = smtplib.SMTP('smtp.gmail.com:587')
        SERVER.ehlo()
        SERVER.starttls()
        SERVER.login(config.USER_NAME, config.PASSWORD)
        SERVER.sendmail(config.FROM_ADDRESS, config.TO_ADDRESS, MSG)
        SERVER.quit()
        print("Message send")
    except IOError:
        print("Something went wrong")
