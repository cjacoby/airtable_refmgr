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


def check_airtable_url_format(url):
    """Return true if url appears to be in a valid format."""
    return True


class Base(object):
    """Class for handling connections to an Airtable Base."""
    def __init__(self, api_key, base_url):
        """
        Parameter
        ---------
        api_key : str
            API Key to authenticate with your Airtable API.

        base_url : str
        """
        self.api_key = api_key
        self.base_url = base_url
        self._headers = {"Authorization": "Bearer {}".format(self.api_key)}

    @classmethod
    def from_config(cls, config_path):
        """Initialize the API_KEY from the config file.
        You must specify the API_KEY manually using the credentials from your
        own account.
        """
        try:
            with open(config_path) as fh:
                CONFIG = yaml.load(fh)
        except IOError:
            logger.error("Config file must be a valid yaml file.")
            raise

        try:
            api_key = CONFIG.get('api_key', CONFIG.get('API_KEY'))
            base_url = CONFIG.get('base_url', CONFIG.get('BASE_URL'))
        except KeyError:
            logger.error("config.yaml must contain keys "
                         "'API_KEY' & 'BASE_URL'.")
            raise
        return cls(api_key, base_url)

    def __repr__(self):
        # We don't show the api_key, 'cause we want it to stay
        # private-ish.
        return "{}(base_url='{}')".format(
            self.__class__.__name__,
            self.base_url)

    def __getitem__(self, table_name):
        """Return a Table by name.

        Parameters
        ----------
        table_name : str
        """
        return Table(self.api_key, self.base_url, table_name)

    def table(self, table_name):
        """Get a table by name."""
        return self[table_name]


class Table(Base):
    """Class for handling connections to specific
    Tables, by name.
    """
    def __init__(self, api_key, base_url, table_name):
        super(Table, self).__init__(api_key, base_url)
        self.name = table_name

    def __repr__(self):
        return "{}(table='{}', base_url='{}')".format(
            self.__class__.__name__,
            self.name,
            self.base_url)

    def get(self, query_kwargs={}):
        return self.get_table(self.name, query_kwargs)

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


# class ReferencesAPI(AirtableAPI):
#     TABLE = "References"

#     def __init__(self, api_key=API_KEY):
#         super(ReferencesAPI, self).__init__(api_key)

#     def stats(self):
#         """Print stats on your references table."""
#         pass

#     def to_bibtex(self, filename):
#         """Build a bibtex file from the references."""


# class AuthorsAPI(AirtableAPI):
#     TABLE = "Authors"

#     def __init__(self, api_key=API_KEY):
#         super(AuthorsAPI, self).__init__(api_key)
#         self.table = "References"

#     def stats(self):
#         """Print stats on your references table."""
#         pass
