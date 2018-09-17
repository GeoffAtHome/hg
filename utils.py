
''' This module contains utility functions that are shared across other programs '''
import json
import requests

HG_URL = "https://my.geniushub.co.uk/v1"


class GeniusUtility():
    def __init__(self, key):
        # Save the key
        self._headers = {'Authorization': 'Bearer ' + key}

    def getjson(self, identifier):
        """ gets the json from the supplied zone identifier """
        url = HG_URL + identifier
        try:
            response = requests.get(url, headers=self._headers)

            if response.status_code == 200:
                return json.loads(response.text)

        except Exception as ex:
            print("Failed requests in getjson")
            print(ex)
            return None

    def putjson(self, identifier, data):
        """ puts the json data to the supplied zone identifier """
        url = HG_URL + identifier
        try:
            response = requests.put(url, headers=self._headers, json=data)
            return response.status_code == 200

        except Exception as ex:
            print("Failed requests in putjson")
            print(ex)
            return False
