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

CONFIG_FILE = os.path.join(os.path.dirname(__file__),
                           os.pardir, "config.yaml")
API_KEY = None
BASE_URL = None


def init():
    """Initialize the API_KEY from the config file.
    You must specify the API_KEY manually using the credentials from your
    own account.
    """
    global API_KEY, BASE_URL
    try:
        with open(CONFIG_FILE) as fh:
            CONFIG = yaml.load(fh)
    except IOError:
        logger.error("Config file must be config.yaml, and valid yaml file.")

    try:
        API_KEY = CONFIG['API_KEY']
        BASE_URL = CONFIG['BASE_URL']
    except KeyError:
        logger.error("config.yaml must contain keys 'API_KEY' & 'BASE_URL'.")

init()


class AirtableAPI(object):
    TABLE = None

    """Class for managing calls to the Reference Manager Airtable API."""
    def __init__(self, api_key=API_KEY, base_url=BASE_URL):
        """
        Parameter
        ---------
        API_KEY : str
            API Key to authenticate with your Airtable API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self._headers = {"Authorization": "Bearer {}".format(self.api_key)}

    def get(self, query_kwargs={}):
        return self.get_table(self.TABLE, query_kwargs)

    def get_table(self, table, query_kwargs={}):
        if table is None:
            return
        params = {}
        r = requests.get(
            os.path.join(self.base_url, table),
            headers=self._headers,
            params=params)
        return r.json()

    def to_df(self):
        """Convert the airtable base into a dataframe.

        Parameters
        ----------
        simple : bool
            If True, filters out columns which have reference data.
        """
        records = self.get()['records']
        index = [x['id'] for x in records]
        fields = [x['fields'] for x in records]
        return pandas.DataFrame(fields, index=index)


class ReferencesAPI(AirtableAPI):
    TABLE = "References"

    def __init__(self, api_key=API_KEY):
        super(ReferencesAPI, self).__init__(api_key)

    def stats(self):
        """Print stats on your references table."""
        pass

    def to_bibtex(self, filename):
        """Build a bibtex file from the references."""


class AuthorsAPI(AirtableAPI):
    TABLE = "Authors"

    def __init__(self, api_key=API_KEY):
        super(AuthorsAPI, self).__init__(api_key)
        self.table = "References"

    def stats(self):
        """Print stats on your references table."""
        pass
