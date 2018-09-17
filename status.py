''' program to email when a battery is low (below THRESHOLD in config file) '''
import smtplib
import json
import requests
import config
import utils

# Load the utils
gu = utils.GeniusUtility(config.HG_SIG)

# List to hold results
DEVICE_LIST = []
BAD_LIST = []

# Find the devices with batteries
devices = filter(
    lambda device: 'batteryLevel' in device['state'], gu.getjson('/devices'))

for value in devices:
    room = value['assignedZones'][0]['name']
    devicetype = value['type']
    node_id = value['id']
    if 'batteryLevel' in value['state']:
        text = node_id + ": " + devicetype + " in " + room
        level = value['state']['batteryLevel']
        text = text + " Battery level: " + str(level)
        DEVICE_LIST.append(text)
        if level < config.THRESHOLD:
            BAD_LIST.append(text)

# Print sorted list
DEVICE_LIST = sorted(DEVICE_LIST, key=lambda x: int(x.split(':')[0]))
for result in DEVICE_LIST:
    print(result)

# Email bad list
if BAD_LIST:
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
