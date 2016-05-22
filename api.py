"""Wrappers for calls to the Airtable API.

Use the AirtableAPI class to handle all requests to the API.

Example:

"""

import pandas
import logging
import os
import requests
import yaml

logger = logging.getLogger(__name__)

CONFIG_FILE = "config.yaml"
API_KEY = None


def init():
    """Initialize the API_KEY from the config file.
    You must specify the API_KEY manually using the credentials from your
    own account.
    """
    global API_KEY
    try:
        with open(CONFIG_FILE) as fh:
            CONFIG = yaml.load(fh)
    except IOError:
        logger.error("Config file must be config.yaml, and valid yaml file.")

    try:
        API_KEY = CONFIG['API_KEY']
    except KeyError:
        logger.error("Key 'API_KEY' must exist in config.yaml.")

init()


class AirtableAPI():
    BASE_URL = "https://api.airtable.com/v0/appumMekpYH175W7f/"

    """Class for managing calls to the Reference Manager Airtable API."""
    def __init__(self, api_key=API_KEY):
        """
        Parameter
        ---------
        API_KEY : str
            API Key to authenticate with your Airtable API.
        """
        self.api_key = api_key
        self._headers = {"Authorization": "Bearer {}".format(self.api_key)}

    def get(self, table, query_kwargs={}):
        params = {}
        r = requests.get(
            os.path.join(self.BASE_URL, table),
            headers=self._headers,
            params=params)
        return r.json()


class ReferencesAPI(AirtableAPI):
    def __init__(self, api_key=API_KEY):
        super(ReferencesAPI, self).__init__(api_key)
        self.table = "References"

    def get(self, query_kwargs={}):
        return super(ReferencesAPI, self).get(self.table, query_kwargs)

    def 
