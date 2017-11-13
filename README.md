Python Genius
=============

A set of python scripts to help with your Genius heating hub. See https://www.geniushub.co.uk/ for details

How To Use
----------

### Configuration:

* Copy the provided `config-blank.py` file and save as `config.py`. Update the various setting in the config file to meeting you requirements.
* This should include the URL and credentials for your Genius hub and email address details.
* To use 

### Status.py

* Status.py when run will email you the nodes in your network when a battery is below the THRESHOLD set in the configuration.
* The reason for writing this is so that I can be emailed when the batteries require changing rather than finding out when something isn't working.
* The Genius hub does provide this information but I don't look at this often. My usage is once it is configured leave it alone. 
* If I need to override I tend to do this with Alex via IFTTT.
* Run `py status.py`
* I run with daily with a scheduler at around 04:00 everyday.

### Mirror.py
* Mirror.py publishes the Genius hub setting to Firebase.
* The reason for this is to get to the point where I can use push notifications for when the battery levels are low. 
* In addition, a dashboard can be written that will be more responsive that Genius hub. I find that at times this can take what seems like forever to load.
* This also adds resilience when when the the Genius servers are down.
* Run `py mirror.py`

#### Set up
* To use `mirror.py` a Firebase project needs to be created. Registration Firebase is free and I find it works well. 
* `firebase-rules.json` contains the rules that I currently use. These rules require authentication to write to the database but anyone can read. 
This file can be copied to the Database/Rules setting in the Firebase project portal (https://console.firebase.google.com/).

### Other files
* `mirrortest.py` developers testing for ensure the correct data is retrieved.
* `convertzonelist.py` developers testing to ensure json produced is fit for purpose with Firebase. Initial json produced worked but would not play well with Firebase/Polymer bindings. 
That is, updates on Firebase were not immediately reflected to Polymer.


