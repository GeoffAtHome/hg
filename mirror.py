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
USER = AUTH.sign_in_with_email_and_password(
    config.FIREBASE_USER, config.FIREBASE_PASSWORD)

# Get a reference to the database service
DATABASE = FIREBASE.database()

# Calculate the number of time required before a 1 hour token expiry (go for half-life)
REFRESH_LOOP = 60 * 60 / (config.REFRESH_INTERVAL * 2)
PASSES_TO_NEXT_REFRESH = REFRESH_LOOP

# Count the readings
COUNT = 0

# Get the root info
print(time.asctime(), "START:")
WHOLEHOUSE = utils.GETJSON(0)

# Loop collecting the data
while True:
    try:
        # Get the data
        print(time.asctime(), "READING:")
        ZONE_LIST = utils.getzonelist(WHOLEHOUSE)

        # Converts into arrays
        print(time.asctime(), "CONVERTING:")
        DATA = utils.convertzonelist(ZONE_LIST, WHOLEHOUSE)

        # before the 1 hour expiry:
        PASSES_TO_NEXT_REFRESH -= 1
        if PASSES_TO_NEXT_REFRESH <= 0:
            USER = AUTH.refresh(USER['refreshToken'])
            PASSES_TO_NEXT_REFRESH = REFRESH_LOOP

        # Write to Firebase
        print(time.asctime(), "SAVING:")
        DATABASE.child("data").update(DATA, USER['idToken'])
        COUNT += 1
        print(time.asctime(), COUNT)

    except Exception as ex:
        print(ex)

    # wait for next interval
    time.sleep(config.REFRESH_INTERVAL)
