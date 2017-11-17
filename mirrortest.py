''' This module gets the json data from the heat genius house controller
 and publishes to firebase '''
import time
import config
import pyrebase
import utils

# connect to firebase
FIRE_CONFIG = {
    "apiKey": config.FIREBASE_API_KEY,
    "authDomain": config.FIREBASE_AUTH_DOMAIN,
    "databaseURL": config.FIREBASE_DATABASE_URL,
    "storageBucket": config.FIREBASE_STORAGE_BUCKET
}

FIREBASE = pyrebase.initialize_app(FIRE_CONFIG)

# Get a reference to the auth service
AUTH = FIREBASE.auth()

# Log the user in
USER = AUTH.sign_in_with_email_and_password(config.FIREBASE_USER, config.FIREBASE_PASSWORD)

# Get a reference to the database service
DATABASE = FIREBASE.database()

# Calculate the number of time required before a 1 hour token expiry (go for half-life)
REFRESH_LOOP = 60 * 60 / (config.REFRESH_INTERVAL * 2)
PASSES_TO_NEXT_REFRESH = REFRESH_LOOP

# Switch to read JSON from file
utils.GETJSON = utils.getjsonfromfile

# Loop collecting the data
while True:
    # Get the data
    WHOLEHOUSE = utils.GETJSON(0)
    ZONE_LIST = utils.getzonelist(WHOLEHOUSE)

    # Write data to file
    utils.write_to_file(ZONE_LIST)

    # Converts into arrays
    DATA = utils.convertzonelist(ZONE_LIST, WHOLEHOUSE)

    # before the 1 hour expiry:
    PASSES_TO_NEXT_REFRESH -= 1
    if PASSES_TO_NEXT_REFRESH <= 0:
        USER = AUTH.refresh(USER['refreshToken'])
        PASSES_TO_NEXT_REFRESH = REFRESH_LOOP

    # Write to Firebase
    DATABASE.child("data").update(DATA, USER['idToken'])

    # wait for next interval
    time.sleep(config.REFRESH_INTERVAL)
