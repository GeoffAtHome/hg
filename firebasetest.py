import pyrebase
import config

fireconfig = {
    "apiKey": config.FIREBASE_API_KEY,
    "authDomain": config.FIREBASE_AUTH_DOMAIN,
    "databaseURL": config.FIREBASE_DATABASE_URL,
    "storageBucket": config.FIREBASE_STORAGE_BUCKET
}

firebase = pyrebase.initialize_app(fireconfig)

# Get a reference to the auth service
auth = firebase.auth()

# Log the user in
user = auth.sign_in_with_email_and_password(config.FIREBASE_USER, config.FIREBASE_PASSWORD)

# Get a reference to the database service
db = firebase.database()

data = {"test": {"Test": "test ZZZZ data", "More": "more test data"}}
result = db.child("newnode").update(data, user['idToken'])
print(result)
